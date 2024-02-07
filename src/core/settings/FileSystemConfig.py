import os

from src.core.settings.GlobalSettings import Globals


class FileSystemConfig:
    fs_config = Globals("file-system")

    def get_storage_path(self):
        return self.fs_config["storage"]

    def set_storage_path(self, path):
        self.fs_config["storage"] = path

    def get_src_path(self):
        return self.fs_config["src"]

    def set_src_path(self, path):
        self.fs_config["src"] = path

    @staticmethod
    def check_access(path):
        try:
            tmp_file = os.path.join(path, "__tmp__")
            f = open(tmp_file, "w")
            f.write(tmp_file)
            f.close()
            os.unlink(tmp_file)
        except Exception as e:
            print(repr(e))
            return False
        return True
