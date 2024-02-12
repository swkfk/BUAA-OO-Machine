import json
import os.path
from pathlib import Path

DB_ROOT = Path("database")
COURSE_ROOT = DB_ROOT / "course"
POINT_ROOT = DB_ROOT / "point"
USER_ROOT = DB_ROOT / "user"
SOURCE_ROOT = DB_ROOT / "source"


def ensure_directory():
    DB_ROOT.mkdir(exist_ok=True)
    COURSE_ROOT.mkdir(exist_ok=True)
    POINT_ROOT.mkdir(exist_ok=True)
    USER_ROOT.mkdir(exist_ok=True)
    SOURCE_ROOT.mkdir(exist_ok=True)


class _JsonFileCacher:
    def __init__(self):
        self._cache = {}
        self._cache_time = {}

    async def __call__(self, path):
        path = str(path)
        if path not in self._cache:
            self._cache[path] = None
            self._cache_time[path] = 0
        cur_time = os.path.getmtime(path)
        if cur_time > self._cache_time[path]:
            print(f"Update Cache for {path}")
            # Update the cache
            self._cache[path] = json.load(f := open(path, "r"))
            f.close()
            self._cache_time[path] = cur_time
        return self._cache[path]


JsonLoader = _JsonFileCacher()
