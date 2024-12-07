from __future__ import annotations

import subprocess
from pathlib import Path


def get_video_path() -> Path:
    return Path(subprocess.check_output('xdg-user-dir VIDEOS'.split(' ')).decode().strip())


extension = 'irp'
