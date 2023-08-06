from typing import *
import dataclasses
from dataclasses import dataclass

from cbutil import Path
from awrand import *

__all__ = ['make_path_info', 'PathInfo']

@dataclass
class PathInfo:
    root: Path = None
    core: Path = None    # for read-only data
    data: Path = None  # for persistent data
    cache: Path = None
    tmp: Path = None
    log: Path = None

    messey: Path = None  # for any temp files

    def clean_tmp(self):
        self.tmp.remove_sons()

    def make_tmp(self, suffix='', prefix=''):
        return self.messey / (prefix + make_id_str() + suffix)
    
    def create_path(self):
        for p in dataclasses.astuple(self):
            p: Path
            p.mkdir()

def make_path_info(root: Union[Path, str]):
    path = PathInfo(
        root = Path(root),
        core = root/'core',      # for read-only data
        data = root/'data',  # for persistent data
        cache = root/'cache',
        tmp = root/'tmp',
        messey = root/'tmp/messey',  # for any temp files
        log = root/'tmp/log'
    )
    return path


