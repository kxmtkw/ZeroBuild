from typing import Literal

UsableCompilerType = str | Literal[
	"gcc", 
	"g++", 
	"clang", 
	"clang++",
	"msvc"
]

CompilerType = str | Literal[
	"gcc", 
	"g++", 
	"clang", 
	"clang++",
	"msvc",
	"inherit"
]

