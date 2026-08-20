__version__ = "v1.4.2"

# Main API classes
from pathlib import Path

from zero.interface.build import Build
from zero.interface.source import Source
from zero.interface.executable import Executable
from zero.interface.static_lib import StaticLibrary
from zero.interface.shared_lib import SharedLibrary
from zero.interface.precomp_lib import PreCompiledLibrary
from zero.interface.glob import FileGlob
from zero.interface.system import System
from zero.interface.internals import Internals
from zero.interface.arguments import Flags, Macro
from zero.interface.user_options import UserOptions

__all__ = [
	"Path",
	"Build",
	"Source",
	"Executable",
	"StaticLibrary",
	"SharedLibrary",
	"PreCompiledLibrary",
	"FileGlob",
	"System",
	"Internals",
	"Flags",
	"UserOptions",
	"Macro"
]