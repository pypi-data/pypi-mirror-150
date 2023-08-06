import sys
import asyncio
from cbutil import Path

from .path import make_path_info
from .proc import *

__all__ = ['ResContext']

class ResContext:
    def __init__(self, root:Path):
        pass
        if root is None:
            root = Path(sys.argv[0]).prnt
        self.path = path = make_path_info(root)
        path.create_path()

    async def run_cmd_async(self, cmd, cwd=None, env=None):
        if cwd is not None:
            Path(cwd).mkdir()
            cwd = str(cwd)

        if env is not None:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env
            )
        else:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

        stdout, stderr = await proc.communicate()
        return stdout, stderr


    async def run_shellscript_async(self, shellscript: str, cwd=None, env=None, tmp_file_path:Path=None):
        path = self.path
        if tmp_file_path is None:
            tmp_file_path = path.make_tmp(suffix='.bat')
        return await run_shellscript_async(shellscript, tmp_file_path, cwd, env)

    








