from enum import Enum
from typing import List, Optional
from typing_extensions import TypedDict


class CWDRelativeTo(str, Enum):
    CURRENT_SOURCE = "current_source"
    SOURCES_ROOT = "sources_root"
    CWD = "cwd"


RunTerminalOptions = TypedDict(
    "RunTerminalOptions",
    {
        "setup": str,
        "input": List[Optional[str]],
        "prompt-matchers": Optional[List[str]],
        "allow-exceptions": Optional[bool],
        "cwd": Optional[str],
        "cwd-relative-to": Optional[CWDRelativeTo],
        "disable-cache": Optional[bool],
        "echo": Optional[bool],
    },
    total=False,
)
