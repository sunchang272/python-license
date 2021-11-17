# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: func.py
Author: sunch
Create Date: 2021/11/12 13:53 
-------------------------------------------------
"""
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from uuid import uuid4
import datetime
import hashlib
import random
import base64
import time
import os


data_folder = './data/'


class Utils:
    @staticmethod
    def rand_key(texture='', allowed_chars=None, length=16):
        """
        :param texture: Random key name
        :param allowed_chars: Key's dictionary
        :param length: Key's length
        :return: Random key
        """
        secret_key = hashlib.md5(bytes(''.join([texture]), encoding='UTF-8')).hexdigest()
        if secret_key is None:
            secret_key = "n&^-9#k*-6pwzsjt-qsc@s3$l46k(7e%f80e7gx^f#vouf3yvz"
        if allowed_chars is None:
            allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        random.seed(
            hashlib.sha256(
                ('%s%s%s' % (
                    random.getstate(),
                    time.time(),
                    secret_key)).encode('utf-8')
            ).digest())
        ret = ''.join(random.choice(allowed_chars) for i in range(length))
        return texture, ret

    @staticmethod
    def sha256_enc(chars):
        sha256 = hashlib.sha256()
        sha256.update(chars)
        return sha256.digest()

    @staticmethod
    def md5_enc(chars):
        md5 = hashlib.md5()
        md5.update(chars)
        return md5.digest()

    @staticmethod
    def base64_enc(chars):
        return base64.encodebytes(chars).strip(b'\n')

    @staticmethod
    def base64_decode(chars):
        return base64.decodebytes(chars)

    @staticmethod
    def rsa_enc(chars, key):
        # Instantiating PKCS1_OAEP object with the public key for encryption
        aes = PKCS1_OAEP.new(key=key)
        # Encrypting the message with the PKCS1_OAEP object
        return aes.encrypt(chars)

    @staticmethod
    def aes_enc(chars, key, mode=AES.MODE_ECB):
        # Init AES encryptor
        aes = AES.new(key, mode)
        # Encrypting the message
        return aes.encrypt(chars)

    @staticmethod
    def format_license(ori_lic, date):
        ori_lic_str = ori_lic.decode().strip('\n')
        return '{0}\n{1}'.format(ori_lic_str, date).encode()

    @staticmethod
    def add_to_16(chars):
        while len(chars) % 16 != 0:
            chars += b'\0'
        return chars


class GenKey:
    def __init__(self, key_name, key_value):
        self.key_name = key_name
        self.key_value = key_value

    @staticmethod
    def rand_key():
        key_name = str(uuid4())
        return Utils.rand_key(key_name)

    def save_keys(self, pri_key, pub_key, aes_key, ori_key):
        """
        :param pri_key: RSA private key
        :param pub_key: RSA public key
        :param aes_key: AES key after RSA
        :param ori_key: AES key before RSA
        :return: save result
        """
        # Save RSA keys
        # Writing down the private and public keys to 'pem' files
        date = datetime.datetime.now().strftime('%Y%m%d')
        save_path = os.path.join(data_folder, date).replace('\\', '/')
        os.makedirs(save_path, exist_ok=True)
        key_path = os.path.join(save_path, self.key_name).replace('\\', '/')
        if os.path.exists(key_path):
            return 'Key name exists'
        os.makedirs(key_path)
        private_key_name = '{0}_{1}_{2}.{3}'.format(date, self.key_name, 'private', 'pem')
        private_key_file = os.path.join(key_path, private_key_name).replace('\\', '/')
        public_key_name = '{0}_{1}_{2}.{3}'.format(date, self.key_name, 'public', 'pem')
        public_key_file = os.path.join(key_path, public_key_name).replace('\\', '/')
        with open(private_key_file, 'wb') as pr_writer:
            pr_writer.write(pri_key)
        with open(public_key_file, 'wb') as pu_writer:
            pu_writer.write(pub_key)

        # Save AES keys
        aes_key_name = '{0}_{1}_{2}.{3}'.format(date, self.key_name, 'key', 'aes')
        ori_key_name = '{0}_{1}_{2}.{3}'.format(date, self.key_name, 'key', 'ori')
        aes_key_path = os.path.join(key_path, aes_key_name)
        ori_key_path = os.path.join(key_path, ori_key_name)
        with open(aes_key_path, 'wb') as ak_writer:
            ak_writer.write(aes_key)
        with open(ori_key_path, 'wb') as ok_writer:
            ok_writer.write(ori_key)
        return 'Success, keys in {0}'.format(key_path)

    def gen_keys(self):
        # Generating private key (RsaKey object) of key length of 2048 bits
        private_key = RSA.generate(2048)
        # Generating the public key (RsaKey object) from the private key
        public_key = private_key.publickey()
        # Converting the RsaKey objects to string
        private_key_export = private_key.export_key()
        public_key_export = public_key.export_key()
        # Encrypt aes key
        # Str to bytes
        key_value = self.key_value.encode()
        # Base64 encode aes key
        base64_key = Utils.base64_enc(key_value)
        aes_key = Utils.rsa_enc(base64_key, public_key)
        return self.save_keys(private_key_export, public_key_export, aes_key, base64_key)


class EncLic:
    def __init__(self, key_file, lic_file, due_time):
        self.key_file = key_file
        self.lic_file = lic_file
        self.due_time = due_time
        self.lic = self.load_lic()
        self.key = self.load_key()

    def load_lic(self):
        if not os.path.exists(self.lic_file):
            return None
        return open(self.lic_file, 'rb').read()

    def load_key(self):
        if not os.path.exists(self.key_file):
            return None
        key = open(self.key_file, 'rb').read()
        key = Utils.base64_decode(key)
        if len(key) > 16:
            return None
        return key

    def enc_lic(self):
        if self.lic is None or self.key is None:
            return 'License file or key file invalid'
        ori_key = Utils.add_to_16(self.key)
        ori_lic = Utils.add_to_16(Utils.format_license(self.lic, self.due_time))
        aes_lic = Utils.aes_enc(ori_lic, ori_key)
        base64_aes_lic = Utils.base64_enc(aes_lic)
        out_lic_file = '{}.enc'.format(os.path.splitext(self.lic_file)[0])
        with open(out_lic_file, 'wb') as lic_writer:
            lic_writer.write(base64_aes_lic)
        return 'Success, license in {0}'.format(os.path.dirname(self.lic_file))


if __name__ == '__main__':
    # key_gen = GenKey('2222', '111')
    # sss = key_gen.gen_keys()
    # print(sss)
    lic_enc = EncLic(
        'data/20211112/7ac36daa-6000-441c-a23a-098ba0d2df34/20211112_7ac36daa-6000-441c-a23a-098ba0d2df34_key.ori'
        , './data/20211112/7ac36daa-6000-441c-a23a-098ba0d2df34/License.lic'
        , '2021-11-13 13:11:20')
    print(lic_enc.lic)
    print(lic_enc.key)
    print(lic_enc.enc_lic())
