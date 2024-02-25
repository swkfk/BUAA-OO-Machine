import hashlib
import os.path
import tempfile


class TempFile:
    def __init__(self, suffix=""):
        # Ensure a name for the temporary file
        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)

    def obj(self):
        return self.temp_file

    def name(self):
        _, filename = os.path.split(self.temp_file.name)
        return filename

    def encrypt(self, passwd: str):
        b = bytearray(self.temp_file.read())
        self.temp_file.seek(os.SEEK_SET)
        key = hashlib.sha256((passwd * 2).encode()).digest()
        length = len(b)
        for i in range(length):
            b[i] = ((b[i] ^ key[(7 + 3 * i) % 32]) + i) % 256
        self.temp_file.write(b)
        self.temp_file.seek(os.SEEK_SET)

    def __del__(self):
        self.temp_file.close()
