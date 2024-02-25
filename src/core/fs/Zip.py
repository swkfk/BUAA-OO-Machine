import os
from zipfile import ZipFile

from src.core.fs.TempFile import TempFile


def compress(path: str, passwd: str) -> TempFile:
    tf = TempFile(suffix=".zip")

    paths = []
    for root, _, files in os.walk(path):
        for filename in files:
            paths.append(os.path.join(root, filename))

    zf = ZipFile(tf.obj(), "w")
    for file in paths:
        zf.write(file, arcname=os.path.relpath(file, path))
    zf.close()
    tf.obj().seek(os.SEEK_SET)

    if passwd != "":
        tf.encrypt(passwd)

    return tf
