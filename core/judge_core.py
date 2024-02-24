import asyncio
import shutil
import threading
import zipfile
from typing import Literal

from core.cmd import Cmd
from core.fs import SOURCE_ROOT, JAVA_ROOT, GetPointListOfTimestamp, POINT_ROOT, GetPointTimestamp, COURSE_ROOT, \
    JsonLoader


class JudgeCore:
    def __init__(self, digest: str, sys_info: (str, int, int)):
        self.user, self.proj, self.unit = sys_info
        self.digest = digest
        self.zipped_file = SOURCE_ROOT / f"{digest}.zip"
        self.target_path = JAVA_ROOT / f"{digest}"
        self.status_path = self.target_path / "status"
        self.build_path = self.target_path / "class"
        self.source_path = self.target_path / "src"

        self.main_class = (SOURCE_ROOT / f"{digest}.entry").read_text()

    def run(self):
        self._init_env()
        self._add_status("Submitted")

        async def worker():
            await self._unzip()
            ret = await self._compile()
            if ret == 0:
                await self._run_test()
            else:
                await self._set_ce()

        # With mass chaos! I hava a poor knowledge about async / await!
        def aux():
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            tasks = [
                worker()
            ]
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()

        # Maybe this will be slow!
        threading.Thread(target=aux).start()

    def _add_status(self, status: Literal["Submitted", "Unzipped", "Compiled", "Done", "Err::CE", "Err::RE"]):
        (self.status_path / status).touch(exist_ok=False)

    def _init_env(self):
        if self.target_path.exists():
            shutil.rmtree(self.target_path)

        self.status_path.mkdir(parents=True, exist_ok=False)
        self.build_path.mkdir(parents=False, exist_ok=False)
        self.source_path.mkdir(parents=False, exist_ok=False)

    async def _unzip(self):
        zf = zipfile.ZipFile(self.zipped_file)
        zf.extractall(path=self.source_path)
        zf.close()

        self._add_status("Unzipped")

    async def _compile(self):
        # 1. List all java files
        lists = []
        for item in self.source_path.rglob("*.java"):
            lists.append(str(item))
        (self.target_path / "sources.list").write_text("\n".join(lists))
        # 2. Compile it!
        ret = Cmd("javac") \
            .args(["-d", str(self.build_path)]) \
            .args(["-encoding", "utf-8"]) \
            .arg("-g") \
            .args(["-sourcepath", str(self.source_path)]) \
            .arg(f"@{self.target_path / 'sources.list'}") \
            .stderr((self.target_path / "compile-msg.txt").open("w")) \
            .wait()
        if ret != 0:
            self._add_status("Err::CE")
        else:
            self._add_status("Compiled")
        return ret

    async def _run_test(self):
        # 1. Get all the input files needed
        lst: [int] = await GetPointListOfTimestamp(self.proj, self.unit)

        # 2. Run all of them
        rets = []
        for timestamp in lst:
            base_path = POINT_ROOT / str(timestamp)
            in_path = base_path / "stdin"
            out_path = base_path / "stdout" / self.user
            err_path = base_path / "stderr" / self.user
            ret_path = base_path / "return_value" / self.user
            ret = Cmd("java") \
                .arg(self.main_class) \
                .args(["-cp", "."]) \
                .cwd(str(self.build_path)) \
                .stdin(open(in_path, "r")) \
                .stdout(open(out_path, "w")) \
                .stderr(open(err_path, "w")) \
                .wait()
            rets.append(ret)
            ret_path.write_text(str(ret))
        if any(rets):
            self._add_status("Err::RE")
        else:
            self._add_status("Done")

    async def _set_ce(self):
        lst: [int] = await GetPointListOfTimestamp(self.proj, self.unit)
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

            ret = Cmd("java") \
                .arg(main_class) \
                .args(["-cp", "."]) \
                .cwd(str(target_path / "class")) \
                .stdin(open(base_path / "stdin", "r")) \
                .stdout(open(base_path / "stdout" / user, "w")) \
                .stderr(open(base_path / "stderr" / user, "w")) \
                .wait()
            (base_path / "return_value" / user).write_text(str(ret))
