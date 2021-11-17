# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: license_getter.py
Author: sunch
Create Date: 2021/11/12 9:36 
-------------------------------------------------
"""

import socket
import hashlib
import base64
import uuid
import os


class Utils:
    @staticmethod
    def get_mac_address():
        # ref: https://zhuanlan.zhihu.com/p/155951909
        mac = uuid.uuid1().hex[-12:]
        return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])

    @staticmethod
    def get_cpu_info():
        return os.popen('cat /proc/cpuinfo').read()

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_os_info():
        # For docker, the second position means the container id
        # The last position may be different either in same server
        return ' '.join(os.popen('uname -a').read().split(' ')[2:-1])

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


class GenLic:
    def __init__(self, out_path):
        self.out_path = out_path
        self.license = self.gen_license()

    @staticmethod
    def gen_license():
        try:
            ori_lic = Utils.get_mac_address().encode()
            return Utils.base64_enc(ori_lic)
        except Exception as e:
            print(e)
            return None

    def save_license(self):
        lic_path = os.path.join(self.out_path).replace('\\', '/')
        with open(lic_path, 'wb') as lic_writer:
            lic_writer.write(self.license)


def get_license(out_path):
    lic_gen = GenLic(out_path)
    lic_gen.save_license()


if __name__ == '__main__':
    get_license('./License.lic')
