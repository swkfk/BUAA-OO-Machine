import asyncio
import shutil
import subprocess
import threading
import zipfile
from typing import Literal

from fastapi import WebSocket

import pyzipper

from core.cmd import Cmd
from core.fs import SOURCE_ROOT, JAVA_ROOT, GetPointListOfEnabledTimestamp, POINT_ROOT, GetPointTimestamp, COURSE_ROOT, \
    JsonLoader
from core.decryptor import StrDecryptor, FileDecryptor

RUN_TIMEOUT_SECS = 4


class JudgeCore:
    def __init__(self, ws: WebSocket, digest: str, sys_info: (str, int, int), passwd_info: (str, str)):
        self.ws = ws
        self.user, self.proj, self.unit = sys_info
        self.passwd_cipher, self.passwd_salt = passwd_info
        self.digest = digest
        self.zipped_file = SOURCE_ROOT / f"{digest}.zip"
        self.target_path = JAVA_ROOT / f"{digest}"
        self.status_path = self.target_path / "status"
        self.build_path = self.target_path / "class"
        self.source_path = self.target_path / "src"

        self.main_class = (SOURCE_ROOT / f"{digest}.entry").read_text()

    async def run(self):
        self._init_env()

        await self.ws.send_text("Submitted")
        # Unzip may fail
        if not await self._unzip():
            await self._set_ce()
            return
        # Compile
        ret = await self._compile()
        # Clear the java/.../src directory
        await self._clear_src()
        if ret == 0:
            await self._run_test()
        else:
            await self._set_ce()

    def _init_env(self):
        if self.target_path.exists():
            shutil.rmtree(self.target_path)

        self.build_path.mkdir(parents=True, exist_ok=False)
        self.source_path.mkdir(parents=False, exist_ok=False)

    async def _unzip(self):
        if self.passwd_cipher is not None and self.passwd_salt is not None:
            passwd = StrDecryptor(self.passwd_cipher, self.passwd_salt, self.user)
            b = self.zipped_file.read_bytes()
            self.zipped_file.write_bytes(FileDecryptor(bytearray(b), passwd))
        else:
            passwd = None

        try:
            zf = zipfile.ZipFile(self.zipped_file)
            zf.extractall(path=self.source_path)
            zf.close()

            if passwd is not None:
                zf = pyzipper.AESZipFile(self.zipped_file, "w", encryption=pyzipper.WZ_AES)
                zf.setpassword(passwd)
                for file in self.source_path.rglob("*"):
                    zf.write(file, arcname=file.relative_to(self.source_path))
                zf.close()

        except Exception as e:
            await self.ws.send_text("Err::CE")
            (self.target_path / "compile-msg.txt").write_text("Internal Server Error Caught:\n" + repr(e))
            return False

        await self.ws.send_text("Unzipped")
        return True

    async def _compile(self):
        # 1. List all java files
        lists = []
        for item in self.source_path.rglob("*.java"):
            lists.append(str(item))
        (self.target_path / "sources.list").write_text("\n".join(lists))
        # 2. Compile it!
        ret = await Cmd("javac") \
            .args(["-d", str(self.build_path)]) \
            .args(["-encoding", "utf-8"]) \
            .arg("-g") \
            .args(["-sourcepath", str(self.source_path)]) \
            .arg(f"@{self.target_path / 'sources.list'}") \
            .stderr((self.target_path / "compile-msg.txt").open("w")) \
            .wait()
        if ret != 0:
            await self.ws.send_text("Err::CE")
        else:
            await self.ws.send_text("Compiled")
        return ret

    async def _clear_src(self):
        shutil.rmtree(self.source_path)

    async def _run_test(self):
        # 1. Get all the input files needed
        lst: [int] = await GetPointListOfEnabledTimestamp(self.proj, self.unit)

        # 2. Run all of them
        rets = []
        for idx, timestamp in enumerate(lst):
            await self.ws.send_text(f"({idx + 1})")
            base_path = POINT_ROOT / str(timestamp)
            in_path = base_path / "stdin"
            out_path = base_path / "stdout" / self.user
            err_path = base_path / "stderr" / self.user
            ret_path = base_path / "return_value" / self.user
            try:
                ret = await Cmd("java") \
                    .arg(self.main_class) \
                    .args(["-cp", "."]) \
                    .cwd(str(self.build_path)) \
                    .stdin(open(in_path, "r")) \
                    .stdout(open(out_path, "w")) \
                    .stderr(open(err_path, "w")) \
                    .wait(RUN_TIMEOUT_SECS)
            except subprocess.TimeoutExpired:
                ret = f"<Time Limit Exceed: {RUN_TIMEOUT_SECS}s>"
            rets.append(ret)
            ret_path.write_text(str(ret))
        if any(rets):
            await self.ws.send_text("Err::RE")
        else:
            await self.ws.send_text("Done")

    async def _set_ce(self):
        lst: [int] = await GetPointListOfEnabledTimestamp(self.proj, self.unit)
        compile_msg = \
            (self.target_path / "compile-msg.txt").read_text().replace(f"database/java/{self.digest}/", "")
        for timestamp in lst:
            base_path = POINT_ROOT / str(timestamp)
            (base_path / "return_value" / self.user).write_text("<Compile Error>")
            (base_path / "stderr" / self.user).write_text(compile_msg)

    @staticmethod
    async def inc_test(proj: int, unit: int, point: int):
        timestamp = await GetPointTimestamp(proj, unit, point)
        base_path = POINT_ROOT / str(timestamp)
        submit_file = COURSE_ROOT / f"{proj}" / f"{unit}.submit.json"

        if not submit_file.exists():
            return

        submit_obj = await JsonLoader(submit_file)
        for user, digest in submit_obj.items():
            main_class = (SOURCE_ROOT / f"{digest}.entry").read_text()
            target_path = JAVA_ROOT / f"{digest}"

            if (target_path / "status" / "Err::CE").exists():
                continue

            try:
                ret = await Cmd("java") \
                    .arg(main_class) \
                    .args(["-cp", "."]) \
                    .cwd(str(target_path / "class")) \
                    .stdin(open(base_path / "stdin", "r")) \
                    .stdout(open(base_path / "stdout" / user, "w")) \
                    .stderr(open(base_path / "stderr" / user, "w")) \
                    .wait(RUN_TIMEOUT_SECS)
            except subprocess.TimeoutExpired:
                ret = f"<Time Limit Exceed: {RUN_TIMEOUT_SECS}s>"
            (base_path / "return_value" / user).write_text(str(ret))
