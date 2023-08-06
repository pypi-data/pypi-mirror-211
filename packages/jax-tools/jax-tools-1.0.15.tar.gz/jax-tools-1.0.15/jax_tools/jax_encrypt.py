# -*- coding:utf-8 -*-
"""
JAX encryption service
"""
import os.path
import sys
import os
import secrets
import string

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.settings as st
from jax_tools.utils.encrypt import AESCipher
from jax_tools.utils.settings import JAX_KEY_FILE
from jax_tools.logger import logger


def confirm_encryption_key():
    """
    Confirm encryption key
    Returns:

    """
    if os.path.exists(JAX_KEY_FILE):
        encryption_key = open(JAX_KEY_FILE, 'r').read()
        if len(encryption_key) != 32:
            msg = 'encryption key length must be 32, please check file {} correct, or delete this file and try again.' \
                .format(JAX_KEY_FILE)
            print(msg)
            exit(1)
    else:
        # generate encryption key
        encryption_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        if os.path.exists(st.JAX_DATA_DIR) is False:
            os.mkdir(st.JAX_DATA_DIR)
        with open(JAX_KEY_FILE, 'w') as f:
            f.write(encryption_key)


# Confirm encryption key
confirm_encryption_key()

JAX_ENCRYPTION_KEY = open(st.JAX_KEY_FILE, 'r').read()
JAX_ENCRYPT = AESCipher(JAX_ENCRYPTION_KEY).encrypt
JAX_DECRYPT = AESCipher(JAX_ENCRYPTION_KEY).decrypt

if __name__ == '__main__':
    try:
        _plaintext = sys.argv[1]
        if _plaintext == '-d':
            print(JAX_DECRYPT(sys.argv[2]))
        else:
            print(JAX_ENCRYPT(_plaintext))
    except IndexError:
        logger.info('Please give a string for JAX encryption')
