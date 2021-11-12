# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: gen_license_linux.py.py
Author: sunch
Create Date: 2021/11/11 14:47 
-------------------------------------------------
"""


class GenLicLinux:
    """
    -------------------------------------------------
        1. 直接读取 /proc/cpuinfo 文件信息
        2. lscpu 或 lspci 读硬件信息
        3. ifconfig / ip link show 读网卡信息
        4. dmidecode，参考：https://www.cnblogs.com/gmhappy/p/11863968.html
        5. uuid1读最后的Mac地址
    -------------------------------------------------
    """
    def __init__(self):
        pass

    def get_cpu_id(self):
        pass
