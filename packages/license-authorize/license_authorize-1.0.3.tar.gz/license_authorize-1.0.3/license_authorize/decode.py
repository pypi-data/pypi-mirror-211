#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/5/19 15:33
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : decode.py
# @Descr   : decrypt
# @Software: PyCharm
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


# ------------------------decrypt------------------------
def decryption(text_encrypted_base64: str, private_key: bytes):
    # encode （bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64 decode
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # build private key object
    cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # decrypt（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, 0)
    # decode to string
    text_decrypted = text_decrypted.decode()
    return text_decrypted