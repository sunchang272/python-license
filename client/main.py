# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: main.py.py
Author: sunch
Create Date: 2021/11/12 13:57 
-------------------------------------------------
"""

"""
This file is just for tests
In real environments, files call these functions must be compiled
"""
from license_verifier import is_license_valid
from license_getter import get_license

if __name__ == '__main__':
    """
    1. Get private key and aes key from ../server
    2. Get License by get_license
    3. Encrypt License in ../server
    4. Call is_license_valid to verify License
    """
    get_license(out_path='./')
    is_license_valid(lic_file='./License.lic',
                     aes_key_file='./20211112_7ac36daa-6000-441c-a23a-098ba0d2df34_key.aes',
                     rsa_key_file='./20211112_7ac36daa-6000-441c-a23a-098ba0d2df34_private.pem')
