import hashlib
from hashlib import md5
from base64 import b64decode, urlsafe_b64decode


def StrDecryptor(cipher: str, salt: str, user: str) -> bytes:
    key = md5(f"{salt}&{md5(user.encode('utf-8')).hexdigest()}&{salt}".encode('utf-8')).digest()
    cipher_b = bytearray(urlsafe_b64decode(cipher))
    length = len(cipher_b)
    for i in range(length):
        cipher_b[i] ^= key[i % 16]
    for i in range(length - 1, 0, -1):
        cipher_b[i] ^= cipher_b[i - 1]
    return b64decode(cipher_b)


def FileDecryptor(b: bytearray, passwd: bytes) -> bytearray:
    key = hashlib.sha256(passwd * 2).digest()
    for i in range(len(b)):
        b[i] = ((b[i] - i) & 0xff) ^ key[(7 + 3 * i) & 0x1f]
    return b
