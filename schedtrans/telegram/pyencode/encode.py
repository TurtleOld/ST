import hashlib
import os


def encode_string(string):
    salt = os.urandom(16)
    bstring = string.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', bstring, salt, 10000)
    login = salt + key
    return salt, login


def check_login(salt, username):
    bstring = username.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', bstring, salt, 10000)
    return key
