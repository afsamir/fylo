import base64
import hashlib
import json
from random import choice
import string
from datetime import datetime
from dateutil import parser
from Cryptodome.Cipher import AES
import jwt
from exceptions import AuthException


class Encryption:
    def __init__(self) -> None:
        self.jwt_secret_key = "".join(choice(string.ascii_letters) for i in range(30))

    def encrypt_token(self, token, password):
        jwt_encoded_token = jwt.encode(token, self.jwt_secret_key)
        header = b"header"
        cipher = AES.new(
            hashlib.sha256(password.encode()).digest()[0:16],
            AES.MODE_EAX,
        )
        cipher.update(header)
        aes_encoded, tag = cipher.encrypt_and_digest(jwt_encoded_token)
        json_k = ["nonce", "header", "ciphertext", "tag"]
        json_v = [
            base64.b64encode(x).decode("utf-8")
            for x in [cipher.nonce, header, aes_encoded, tag]
        ]
        result = json.dumps(dict(zip(json_k, json_v)))
        return result

    def authenticate(self, token):
        decoded_token = self.verify_jwt(token)
        created_at = parser.parse(decoded_token["timestamp"])
        if (datetime.now() - created_at).total_seconds() > decoded_token["expire"]:
            raise AuthException()
        return decoded_token["id"]

    def verify_jwt(self, token):
        decoded_token = jwt.decode(
            token,
            self.jwt_secret_key,
        )
        return decoded_token
