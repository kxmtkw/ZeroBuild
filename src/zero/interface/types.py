from pathlib import Path
from typing import TypeAlias

from zero.interface.arguments import Flags, LiteralFlag

PathType: TypeAlias = Path | str
FlagType: TypeAlias = Flags | LiteralFlag | str