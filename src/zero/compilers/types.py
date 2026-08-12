from typing import Literal

CompilerType = str | Literal[
	"gcc", 
	"g++", 
	"clang", 
	"clang++",
	"msvc",
	"inherit"
]