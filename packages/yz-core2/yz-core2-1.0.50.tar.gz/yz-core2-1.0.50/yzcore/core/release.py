#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: zhouwei
@date: 2023-5-18
@desc: 用于私有化部署的license解析
"""
from base64 import b64decode
try:
    from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipher
    from Crypto.PublicKey import RSA
    from Crypto.Util import number
except ImportError:
    PKCS1_v1_5_cipher, RSA, number = None, None, None


class RsaUtil(object):

    def __init__(self, public_key):
        self.public_key = RSA.importKey(public_key)

    def decrypt_by_public_key(self, decrypt_message):
        """使用公钥解密.
        :param decrypt_message: 需要解密的内容.
        解密之后的内容直接是字符串，不需要在进行转义
        """
        decrypt_result = b""
        max_length = self._get_max_length(self.public_key, False)
        decrypt_message = b64decode(decrypt_message)
        cipher = PKCS1_v1_5_cipher.new(self.public_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data.encode(encoding='utf-8'), '')
            decrypt_result += out_data
        return decrypt_result

    @staticmethod
    def _get_max_length(rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
        :param rsa_key: 钥匙.
        :param encrypt: 是否是加密.
        """
        block_size = number.size(rsa_key.n) / 8
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = block_size - reserve_size
        return maxlength
