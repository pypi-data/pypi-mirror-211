#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/5/19 14:48
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : _core.py
# @Descr   : _core
# @Software: PyCharm

__all__ = ['license_authorize']

from license_authorize.decode import decryption
import time
import os
import platform
import datetime


class LicenseAuthorize:

    def __init__(self):
        pass

    def __read_lic_file(self, lic_path):
        f = open(lic_path)
        line = f.readline()
        row = 0
        text_encrypted_base64 = ""
        private_key = ""
        is_over_half = False
        while line:
            row += 1
            if row > 6 and "------" not in line and is_over_half is False:
                text_encrypted_base64 += line.rstrip("\n")
            if row > 6 and "------" in line:
                is_over_half = True
            if row > 6 and is_over_half is True and "------" not in line and "#######" not in line:
                private_key += line.rstrip("\n")
            if row > 6 and is_over_half is True and "#######" in line:
                break
            line = f.readline()
        f.close()
        private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + private_key + "\n-----END RSA PRIVATE KEY-----"
        return text_encrypted_base64, private_key

    def verify_cpuId(self, license_cpu_id):
        # sys.platform.startswith（"win"）
        sysstr = platform.system()
        server_cpu_id = None
        if sysstr == "Windows":
            cmd = "wmic cpu get ProcessorId"
            output = os.popen(cmd, "r")
            info = output.readlines()
            # 读取第3行
            rowindex = 0
            for line in info:
                print(line.replace("\n", "").replace(" ", ""))
                if rowindex == 2:
                    server_cpu_id = line.replace("\n", "").replace(" ", "")
                    print(server_cpu_id)
                    break
                rowindex += 1
        elif sysstr == "Linux":
            cmd = "dmidecode -t processor | grep 'ID'"
            output = os.popen(cmd, "r")
            info = output.readlines()
            # 读取第一行
            for line in info:
                print(line.replace("\n", "").replace(" ", ""))
                server_cpu_id = line.replace("\n", "").replace(" ", "").split(":")[1]
                print(server_cpu_id)
                break
        if server_cpu_id is not None and server_cpu_id.upper() == license_cpu_id:
            return True
        else:
            return False

    def check_validity(self, client_time, lic_path):
        text_encrypted_base64, private_key = self.__read_lic_file(lic_path)
        text_decrypted = decryption(text_encrypted_base64, private_key.encode('utf-8'))
        license_cpuid = text_decrypted.split(",")[0]
        license_time = text_decrypted.split(",")[1]
        license_time_obj = datetime.datetime.strptime(license_time, "%Y-%m-%d %H:%M:%S")
        license_time = int(time.mktime(license_time_obj.timetuple()) * 1000)
        server_time = int(time.time() * 1000)
        if license_time >= client_time and license_time >= server_time and self.verify_cpuId(license_cpuid):
            return True
        else:
            return False


license_authorize = LicenseAuthorize()
