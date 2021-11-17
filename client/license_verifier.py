# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: license_verifier.py
Author: sunch
Create Date: 2021/11/12 9:36 
-------------------------------------------------
"""

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from license_getter import GenLic
import datetime
import base64
import os


class Utils:
    @staticmethod
    def base64_decode(chars):
        return base64.decodebytes(chars)

    @staticmethod
    def rsa_decrypt(chars, pri_key):
        rsa_decrypt = PKCS1_OAEP.new(key=pri_key)
        return rsa_decrypt.decrypt(chars)

    @staticmethod
    def aes_decrypt(chars, aes_key, mode=AES.MODE_ECB):
        aes = AES.new(aes_key, mode)
        return aes.decrypt(chars)

    @staticmethod
    def format_license(chars):
        hw_info, due_time = chars.decode().split('\n')
        return hw_info.encode(), due_time[:19]


class VerifyLic:
    def __init__(self, lic_file, aes_key_file, rsa_key_file):
        self.lic_file = lic_file
        self.aes_key_file = aes_key_file
        self.rsa_key_file = rsa_key_file
        self.license = self.load_lic()
        self.rsa_pri_key = self.load_rsa_key()
        self.aes_key = self.load_aes_key()
        self.decrypted_aes_key = self.decrypt_aes_key()
        self.hw_info, self.due_time = self.decrypt_lic()

    def load_lic(self):
        if not os.path.exists(self.lic_file):
            return None
        return open(self.lic_file, 'rb').read()

    def load_rsa_key(self):
        if not os.path.exists(self.rsa_key_file):
            return None
        try:
            primary_key = open(self.rsa_key_file, 'rb').read()
            return RSA.import_key(primary_key)
        except Exception as e:
            print(e)
            return None

    def load_aes_key(self):
        if not os.path.exists(self.aes_key_file):
            return None
        return open(self.aes_key_file, 'rb').read()

    def decrypt_aes_key(self):
        if self.aes_key is None or self.rsa_pri_key is None:
            return None
        try:
            rsa_decrypted_key = Utils.rsa_decrypt(self.aes_key, self.rsa_pri_key)
            return Utils.base64_decode(rsa_decrypted_key)
        except Exception as e:
            print(e)
            return None

    def decrypt_lic(self):
        if self.decrypted_aes_key is None or self.license is None:
            return None
        try:
            base64_decoded_license = Utils.base64_decode(self.license)
            aes_decrypted_license = Utils.aes_decrypt(base64_decoded_license, self.decrypted_aes_key)
            return Utils.format_license(aes_decrypted_license)
        except Exception as e:
            print(e)
            return None

    def verify_hw_info(self):
        hw_info = GenLic.gen_license()
        return hw_info == self.hw_info

    def verify_due_time(self):
        try:
            now_time = datetime.datetime.now()
            due_time = datetime.datetime.strptime(self.due_time, '%Y-%m-%d %H:%M:%S')
            return now_time < due_time
        except Exception as e:
            print(e)
            return False

    def verify_license(self):
        return self.verify_hw_info() and self.verify_due_time()


def is_license_valid(lic_file, aes_key_file, rsa_key_file):
    # Files call this function must be compiled
    if not os.path.exists(lic_file) or not os.path.exists(aes_key_file) or not os.path.exists(rsa_key_file):
        return False
    verifier = VerifyLic(lic_file, aes_key_file, rsa_key_file)
    return verifier.verify_license()


if __name__ == '__main__':
    is_invalid = is_license_valid('./License.lic', './20211112_7ac36daa-6000-441c-a23a-098ba0d2df34_key.aes',
                                  './20211112_7ac36daa-6000-441c-a23a-098ba0d2df34_private.pem')
    print(is_invalid)
