import asyncio
import shutil
import threading
import zipfile
from typing import Literal

from core.cmd import Cmd
from core.fs import SOURCE_ROOT, JAVA_ROOT, GetPointListOfTimestamp, POINT_ROOT


class JudgeCore:
    def __init__(self, digest: str, sys_info: (str, int, int)):
        self.user, self.proj, self.unit = sys_info
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
            await self._unzip(),
            await self._compile(),
            await self._run_test()

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

    def _add_status(self, status: Literal["Submitted", "Unzipped", "Compiled", "Done"]):
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
        Cmd("javac") \
            .args(["-d", str(self.build_path)]) \
            .args(["-encoding", "utf-8"]) \
            .arg("-g") \
            .args(["-sourcepath", str(self.source_path)]) \
            .arg(f"@{self.target_path / 'sources.list'}") \
            .wait()

        self._add_status("Compiled")

    async def _run_test(self):
        # 1. Get all the input files needed
        lst: [int] = await GetPointListOfTimestamp(self.proj, self.unit)

        # 2. Run all of them
        for timestamp in lst:
            base_path = POINT_ROOT / str(timestamp)
            in_path = base_path / "stdin"
            out_path = base_path / "stdout" / self.user
            Cmd("java") \
                .arg(self.main_class) \
                .args(["-cp", "."]) \
                .cwd(str(self.build_path)) \
                .stdin(open(in_path, "r")) \
                .stdout(open(out_path, "w")) \
                .wait()

        self._add_status("Done")
