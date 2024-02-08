import tempfile


class TempFile:
    def __init__(self, suffix=""):
        self.temp_file = tempfile.TemporaryFile(suffix=suffix)

    def obj(self):
        return self.temp_file

    def __del__(self):
        self.temp_file.close()
