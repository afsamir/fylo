import base64
from datetime import datetime
import json
import sys
import hashlib
from Cryptodome.Cipher import AES


sys.path.append("../server")
from api import API


class Session:
    def __init__(self):
        self.username = None
        self.session_key = None

    def login(self, username, password):
        token = API.login(username, datetime.now())
        self.session_key = self.decrypt_token(token, password)
        self.username = username

    def decrypt_token(self, token, password):
        b64 = json.loads(token)
        json_k = ["nonce", "header", "ciphertext", "tag"]
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(
            hashlib.sha256(password.encode()).digest()[0:16],
            AES.MODE_EAX,
            nonce=jv["nonce"],
        )
        cipher.update(jv["header"])
        plaintext = cipher.decrypt_and_verify(jv["ciphertext"], jv["tag"])
        self.session_key = plaintext
        return plaintext
