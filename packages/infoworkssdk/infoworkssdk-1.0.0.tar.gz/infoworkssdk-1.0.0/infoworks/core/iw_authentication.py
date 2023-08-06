#!/usr/bin/env python
import traceback

import requests
import logging
import infoworks.error
from infoworks.sdk import url_builder, local_configurations
from infoworks.sdk.utils import IWUtils
from Cryptodome.Cipher import AES
import base64
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256


def validate_bearer_token(protocol, ip, port, delegation_token):
    client_config = {"protocol": protocol, "ip": ip, "port": port}
    headers = {'Authorization': 'Bearer ' + delegation_token, 'Content-Type': 'application/json'}
    response = IWUtils.ejson_deserialize(
        requests.get(url_builder.validate_bearer_token_url(client_config), headers=headers, verify=False).content)
    if len(response.get("result", {})) > 0:
        return response.get("result")["is_valid"]
    else:
        return False


def get_bearer_token(protocol, ip, port, refresh_token, http_client=None):
    client_config = {"protocol": protocol, "ip": ip, "port": port}
    headers = {'Authorization': 'Basic ' + refresh_token, 'Content-Type': 'application/json'}
    if http_client is not None:
        response = http_client.get(url_builder.get_bearer_token_url(client_config), headers=headers,
                                   timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                   verify=False)
    else:
        response = requests.get(url_builder.get_bearer_token_url(client_config), headers=headers,
                                timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                verify=False)
    if response:
        delegation_token = response.json().get("result").get("authentication_token")
        return delegation_token
    else:
        traceback.print_stack()
        raise infoworks.error.AuthenticationError("Refresh token invalid")


def is_token_valid(client_config, http_client=None):
    try:
        if client_config['bearer_token'] is None:
            logging.info('Invalid Delegation token: ' + str(client_config['bearer_token']))
            return False
        if http_client is not None:
            result = http_client.get(
                url_builder.validate_bearer_token_url(client_config),
                timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                headers=IWUtils.get_default_header_for_v3(client_config['bearer_token']), verify=False
            )
        else:
            result = requests.get(
                url_builder.validate_bearer_token_url(client_config),
                timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                headers=IWUtils.get_default_header_for_v3(client_config['bearer_token']), verify=False
            )
        response = IWUtils.ejson_deserialize(result.content)
        logging.info('Response from rest api: ' + str(response))
        return response.get('result', {}).get('is_valid', False)
    except Exception as e:
        logging.error('Failed to check token validity: ' + str(e))
        return False


def aes_encrypt(data):
    password = "infoworks"  # get this from the  conf
    salt = get_random_bytes(16)
    iv = get_random_bytes(12)
    key = PBKDF2(password, salt, dkLen=256, count=65536, hmac_hash_module=SHA256)
    key = key[0:32]
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, auth_tag = cipher.encrypt_and_digest(bytes(data, 'utf-8'))
    return base64.b64encode(salt + iv + ciphertext + auth_tag).decode('utf-8')
