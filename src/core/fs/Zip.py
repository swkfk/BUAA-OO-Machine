import os
from zipfile import ZipFile

from src.core.fs.TempFile import TempFile


def compress(path: str) -> TempFile:
    tf = TempFile(suffix=".zip")

    paths = []
    for root, _, files in os.walk(path):
        for filename in files:
            paths.append(os.path.join(root, filename))

    zf = ZipFile(tf.obj(), "w")
    for file in paths:
        zf.write(file, arcname=os.path.relpath(file, path))

    return tf
