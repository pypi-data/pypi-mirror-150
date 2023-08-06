# coding: utf-8
# https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.FV5dWW&treeId=62&articleId=103740&docType=1
import json
import logging
from hashlib import md5
from typing import Optional, Union
from urllib.parse import urlencode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA1, SHA256
import base64
import OpenSSL

from django.utils import timezone

ALIPAY_GATEWAY = 'https://mapi.alipay.com/gateway.do?'
ALIPAY_OPENAPI_GATEWAY = 'https://openapi.alipay.com/gateway.do?'

ALIPAY_INPUT_CHARSET = "utf-8"
ALIPAY_SIGN_TYPE_MD5 = "MD5"
ALIPAY_SIGN_TYPE_RSA = "RSA"
ALIPAY_SIGN_TYPE_RSA2 = "RSA2"

GOODS_TYPE_VIRTUAL = 0
GOODS_TYPE_PHYSICAL = 1

log = logging.getLogger('alipay')


def encode_value(v):
    if isinstance(v, str):
        return v
    elif isinstance(v, int):
        return str(v)
    elif isinstance(v, float):
        return '{}'.format(round(v, 2))
    elif isinstance(v, list):
        return '^'.join([encode_value(x) for x in v])
    else:
        raise Exception("can't encode value: %s" % v)


def _build_sign_body(params):
    fields = [k for k, v in params.items()
              if k not in ('sign', 'sign_type') and v is not None]
    fields.sort()

    s = '&'.join(['{}={}'.format(k, encode_value(params[k])) for k in fields])
    return s


def create_sign(params, key, encoding=ALIPAY_INPUT_CHARSET, sign_type=ALIPAY_SIGN_TYPE_MD5):
    assert sign_type in (ALIPAY_SIGN_TYPE_MD5, ALIPAY_SIGN_TYPE_RSA)

    s = _build_sign_body(params)
    if sign_type == ALIPAY_SIGN_TYPE_RSA:
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA1.new(s.encode(encoding)))
        return base64.encodebytes(signature).decode().replace("\n", "")

    else:
        s = s + key
        return md5(s.encode(encoding)).hexdigest()


class Result(object):
    def __init__(self):
        # 关键参数 =============================================
        self.app_id = None
        self.sign_type = None
        self.sign = None
        self.out_trade_no = None
        self.trade_no = None
        self.trade_status = None
        self.seller_id = None
        self.seller_email = None
        self.buyer_email = None
        self.total_amount = None

        # 以下为非关键参数 ======================================
        self.notify_time = None
        self.notify_id = None
        self.notify_type = None
        self.subject = None
        self.payment_type = '1'
        self.buyer_id = None
        self.body = None
        self.extra_common_param = None

        # notify only
        self.gmt_create = None
        self.gmt_payment = None
        self.gmt_close = None
        self.refund_status = None
        self.gmt_refund = None
        self.price = None
        self.quantity = None
        self.discount = None
        self.is_total_fee_adjust = None
        self.use_coupon = None
        self.business_scene = None


class RefundResult:
    """
    https://opendocs.alipay.com/apis/028sm9
    code  String  是  -  网关返回码,详见文档      40004
    msg   String  是  -  网关返回码描述,详见文档  Business  Failed
    sign  String  是  -  签名,详见文档

    buyer_logon_id  String  必填  100  用户的登录id                  159****5620
    buyer_user_id   String  必填  28   买家在支付宝的用户id          2088101117955611
    fund_change     String  必填  1    本次退款是否发生了资金变化    Y
    refund_fee      Price   必填  11   退款总金额。                  指该笔交易累计已经退款成功的金额。               88.88
    store_name      String  选填  512  交易在支付时候的门店名称      望湘园联洋店
    send_back_fee   String  选填  11   本次商户实际退回金额。        说明：如需获取该值，需在入参query_options中传入  refund_detail_item_list。  1.8
    trade_no        String  必填  64   2013112011001004330000121536  支付宝交易号
    out_trade_no    String  必填  64   商户订单号                    6823789339978248
    """

    def __init__(self):
        self.code = None
        self.msg = None

        self.buyer_logon_id = None
        self.buyer_user_id = None
        self.fund_change = None
        self.gmt_refund_pay = None
        self.out_trade_no = None
        self.refund_fee = None
        self.send_back_fee = None
        self.trade_no = None

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> Optional['RefundResult']:
        params = response_dict['alipay_trade_refund_response']
        result = RefundResult()
        for k, v in params.items():
            setattr(result, k, v)
        return result

    def is_succeed(self):
        return self.msg == 'Success' and self.code == '10000'

    # 只有首次提交有变化
    def is_fund_changed(self):
        return self.fund_change == 'Y'


class AlipayCertClient:
    def __init__(self, app_id,
                 private_key_str,
                 public_key_str,
                 app_cert_str=None,
                 alipay_root_cert_str=None,
                 gateway=ALIPAY_OPENAPI_GATEWAY,
                 sign_type=ALIPAY_SIGN_TYPE_RSA2):
        self._private_key_str = private_key_str
        self._public_key_str = public_key_str

        # 公钥证书方式需要用到
        self._app_cert_str = app_cert_str
        self._alipay_root_cert_str = alipay_root_cert_str

        self.app_id = app_id
        self.gateway = gateway

        try:
            self.sign_key = RSA.importKey(private_key_str)
            self.public_key = RSA.importKey(public_key_str)
        except:
            self.sign_key = RSA.importKey(base64.b64decode(private_key_str))
            self.public_key = RSA.importKey(base64.b64decode(public_key_str))
        self.sign_type = sign_type

    @staticmethod
    def build_sign_body(params, ignore_fields):
        fields = [k for k, v in params.items() if k not in ignore_fields and v is not None]
        fields.sort()

        s = '&'.join(['{}={}'.format(k, encode_value(params[k])) for k in fields])
        return s

    @classmethod
    def create_sign(cls, params, key, sign_type: Union[ALIPAY_SIGN_TYPE_RSA, ALIPAY_SIGN_TYPE_RSA2]):
        s = cls.build_sign_body(params, ['sign'])

        signer = PKCS1_v1_5.new(key)
        if sign_type == ALIPAY_SIGN_TYPE_RSA:
            algorithm = SHA1
        else:
            algorithm = SHA256

        signature = signer.sign(algorithm.new(s.encode(ALIPAY_INPUT_CHARSET)))
        return base64.encodebytes(signature).decode().replace("\n", "")

    @staticmethod
    def get_cert_sn(cert_raw_str):
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_raw_str)
        try:
            sig_alg = cert.get_signature_algorithm()
            # print('sig_alg', sig_alg)
        except ValueError:
            return None

        if sig_alg not in (
                b'rsaEncryption',
                b'md2WithRSAEncryption',
                b'md5WithRSAEncryption',
                b'sha1WithRSAEncryption',
                b'sha256WithRSAEncryption',
                b'sha384WithRSAEncryption',
                b'sha512WithRSAEncryption'
        ): return None

        cert_issue = cert.get_issuer()
        name = 'CN={},OU={},O={},C={}'.format(cert_issue.CN, cert_issue.OU, cert_issue.O, cert_issue.C)
        string = name + str(cert.get_serial_number())
        return md5(string.encode()).hexdigest()

    @classmethod
    def get_root_cert_sn(cls, root_cert_raw_str):
        """
        根证书有多个\n\n分割的分证书，要用_连起来
        """
        root_cert_raw_str = root_cert_raw_str.replace('\r', '')
        cert_raw_str_list = [d for d in root_cert_raw_str.split('\n\n') if d]
        cert_sn_list = [cls.get_cert_sn(d) for d in cert_raw_str_list]
        cert_sn_list = [d for d in cert_sn_list if d]
        return '_'.join(cert_sn_list)

    @property
    def public_params(self):
        dt = timezone.make_naive(timezone.now())
        timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')

        params = {
            'app_id': self.app_id,
            'charset': ALIPAY_INPUT_CHARSET,
            'sign_type': ALIPAY_SIGN_TYPE_RSA2,
            'timestamp': timestamp_str,
            'version': '1.0',

        }
        if self._app_cert_str:
            app_cert_sn = self.get_cert_sn(self._app_cert_str)
            alipay_root_cert_sn = self.get_root_cert_sn(self._alipay_root_cert_str)
            params.update({
                'app_cert_sn': app_cert_sn,
                'alipay_root_cert_sn': alipay_root_cert_sn,
            })
        return params

    def create_pay_url(self, out_trade_no, subject, total_amount, notify_url, return_url):
        biz_content = {
            'out_trade_no': out_trade_no,
            'total_amount': total_amount,
            'subject': subject,
            'product_code': 'FAST_INSTANT_TRADE_PAY',
        }
        params = self.public_params
        params.update({
            'method': 'alipay.trade.page.pay',
            'notify_url': notify_url,
            'return_url': return_url,
            'biz_content': json.dumps(biz_content),
        })

        params['sign'] = self.create_sign(params, self.sign_key, self.sign_type)

        query = urlencode(params)
        url = self.gateway + query
        return url

    def create_refund_url(self, out_trade_no, refund_out_trade_no, amount, reason=''):
        biz_content = {
            'out_trade_no': out_trade_no,
            'refund_amount': amount,
            'refund_reason': reason,
            'out_request_no': refund_out_trade_no,  # 部分退款必选
        }

        params = self.public_params
        params.update({
            'method': 'alipay.trade.refund',
            'biz_content': json.dumps(biz_content),
        })

        params['sign'] = self.create_sign(params, self.sign_key, self.sign_type)

        query = urlencode(params)
        url = self.gateway + query
        return url

    def get_verified_result(self, arguments):
        assert isinstance(arguments, dict)

        raw_content = self.build_sign_body(arguments, ['sign', 'sign_type'])
        if arguments['sign_type'] == ALIPAY_SIGN_TYPE_RSA:
            digest = SHA1.new()
        else:
            digest = SHA256.new()

        digest.update(raw_content.encode(ALIPAY_INPUT_CHARSET))

        signer = PKCS1_v1_5.new(self.public_key)
        assert bool(signer.verify(digest, base64.decodebytes(arguments['sign'].encode(ALIPAY_INPUT_CHARSET))))

        result = Result()
        for k, v in arguments.items():
            setattr(result, k, v)
        return result


if __name__ == '__main__':
    pass
