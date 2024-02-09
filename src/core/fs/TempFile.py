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

    def __del__(self):
        self.temp_file.close()
