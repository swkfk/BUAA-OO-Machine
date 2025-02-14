import json
import os.path
import tempfile
from pathlib import Path
from zipfile import ZipFile

DB_ROOT = Path("database")
COURSE_ROOT = DB_ROOT / "course"
POINT_ROOT = DB_ROOT / "point"
USER_ROOT = DB_ROOT / "user"
SOURCE_ROOT = DB_ROOT / "source"
JAVA_ROOT = DB_ROOT / "java"


def ensure_directory():
    DB_ROOT.mkdir(exist_ok=True)
    COURSE_ROOT.mkdir(exist_ok=True)
    POINT_ROOT.mkdir(exist_ok=True)
    USER_ROOT.mkdir(exist_ok=True)
    SOURCE_ROOT.mkdir(exist_ok=True)
    JAVA_ROOT.mkdir(exist_ok=True)


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
            # Update the cache
            self._cache[path] = json.load(f := open(path, "r"))
            f.close()
            self._cache_time[path] = cur_time
        return self._cache[path]


JsonLoader = _JsonFileCacher()


async def GetPointTimestamp(proj: int, unit: int, point: int):
    unit_file = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_file)
    return unit_obj[point]["timestamp"]


async def GetPointListOfEnabledTimestamp(proj: int, unit: int):
    unit_file = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_file)
    return [obj["timestamp"] for obj in unit_obj if not obj.get('disabled', False)]


async def SetPointEnable(proj: int, unit: int, point: int, disabled: True):
    unit_file = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_file)
    unit_obj[point]["disabled"] = disabled
    json.dump(unit_obj, open(unit_file, "w"))

async def SetPointDesc(proj: int, unit: int, point: int, desc: str):
    unit_file = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_file)
    unit_obj[point]["desc"] = desc
    json.dump(unit_obj, open(unit_file, "w"))

async def GetPointEnable(proj: int, unit: int, point: int):
    unit_file = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_file)
    return not ("disabled" in unit_obj[point] and unit_obj[point]["disabled"])


async def ZipOutputs(path: str):
    tf = tempfile.NamedTemporaryFile(suffix=".zip")
    zf = ZipFile(tf, "w")

    for file in Path(path).glob("*"):
        if file.name.startswith("__TEMP__"):
            continue
        zf.write(file, arcname=file.relative_to(path))
    zf.close()
    tf.seek(os.SEEK_SET)
    return tf
