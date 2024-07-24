from hashlib import md5
from base64 import b64encode, urlsafe_b64encode


def Encipher(plain: str, salt: str, user: str) -> str:
    key = md5(f"{salt}&{md5(user.encode('utf-8')).hexdigest()}&{salt}".encode('utf-8')).digest()
    plain_b = bytearray(b64encode(plain.encode("utf-8")))
    length = len(plain_b)
    for i in range(1, length):
        plain_b[i] ^= plain_b[i - 1]
    for i in range(length):
        plain_b[i] ^= key[i % 16]
    return urlsafe_b64encode(plain_b).decode()

