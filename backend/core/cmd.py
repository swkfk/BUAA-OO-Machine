import asyncio
import subprocess
import sys
import time

if sys.version_info[1] < 11:
    from typing_extensions import Self
else:
    from typing import Self
from typing import IO


class Cmd:
    def __init__(self, executable: str):
        self._args = [executable]
        self._stdin = sys.stdin
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self._cwd = None
        self._process = None

    def arg(self, arg: str) -> Self:
        self._args.append(arg)
        return self

    def args(self, args: [str]) -> Self:
        self._args.extend(args)
        return self

    def stdin(self, stdin: IO) -> Self:
        self._stdin = stdin
        return self

    def stdout(self, stdout: IO) -> Self:
        self._stdout = stdout
        return self

    def stderr(self, stderr: IO) -> Self:
        self._stderr = stderr
        return self

    def cwd(self, new: str) -> Self:
        self._cwd = new
        return self

    def run(self):
        self._process = subprocess.Popen(
            args=self._args,
            stdin=self._stdin,
            stdout=self._stdout,
            stderr=self._stderr,
            cwd=self._cwd
        )

    async def wait(self, timeout_secs: int = None) -> int:
        if self._process is None:
            self.run()
        if timeout_secs is None:
            return self._process.wait()
        for _ in range(timeout_secs * 10):
            await asyncio.sleep(0.105)
            ret = self._process.poll()
            if ret is not None:
                return ret
        self._process.kill()
        raise subprocess.TimeoutExpired("java", timeout_secs)

    def __del__(self):
        try:
            if self._process is not None:
                self._process.wait(1)
        except subprocess.TimeoutExpired:
            self._process.kill()
