from enum import Enum
from typing import Any, Literal, TypeAlias, Union

from zero.compilers.types import UsableCompilerType

# written by ai :p because i am too lazy + i ain't writing this by hand


class Flags(str, Enum):
	"""
	Common compiler flags with inline documentation to help you out.
	"""

	# ==========================================
	# GCC / Clang Warnings & Diagnostics
	# ==========================================

	Wall = "-Wall"
	"""
	Enables a broad set of commonly useful compiler warnings.
	Supported by: GCC, Clang
	"""

	Wextra = "-Wextra"
	"""
	Enables extra warning flags not covered by -Wall (e.g. unused parameters).
	Supported by: GCC, Clang
	"""

	Wpedantic = "-Wpedantic"
	"""
	Issues all warnings demanded by strict ISO C and C++ standards.
	Supported by: GCC, Clang
	"""

	Werror = "-Werror"
	"""
	Treats all warnings as fatal compilation errors.
	Supported by: GCC, Clang
	"""

	Wshadow = "-Wshadow"
	"""
	Warns whenever a local variable shadows another variable, parameter, or global.
	Supported by: GCC, Clang
	"""

	Wconversion = "-Wconversion"
	"""
	Warns for implicit conversions that may alter a value or lose precision.
	Supported by: GCC, Clang
	"""

	Wnull_dereference = "-Wnull-dereference"
	"""
	Warns if a null pointer dereference is detected in code paths.
	Supported by: GCC, Clang
	"""

	Wdouble_promotion = "-Wdouble-promotion"
	"""
	Warns when a float is implicitly promoted to a double.
	Supported by: GCC, Clang
	"""

	Wformat_2 = "-Wformat=2"
	"""
	Enables strict format string checks (printf/scanf) against security risks.
	Supported by: GCC, Clang
	"""

	Wimplicit_fallthrough = "-Wimplicit-fallthrough"
	"""
	Warns when a switch case falls through without an explicit annotation or comment.
	Supported by: GCC, Clang
	"""

	Wno_unused_parameter = "-Wno-unused-parameter"
	"""
	Disables warnings for function parameters that are never used.
	Supported by: GCC, Clang
	"""

	Wno_unused_variable = "-Wno-unused-variable"
	"""
	Disables warnings for local variables that are declared but never used.
	Supported by: GCC, Clang
	"""

	Wno_unused_function = "-Wno-unused-function"
	"""
	Disables warnings for static functions defined but never called.
	Supported by: GCC, Clang
	"""

	Wno_missing_field_initializers = "-Wno-missing-field-initializers"
	"""
	Disables warnings if a structure initializer misses fields.
	Supported by: GCC, Clang
	"""

	# ==========================================
	# GCC / Clang Optimization
	# ==========================================

	O0 = "-O0"
	"""
	Disables optimizations. Fast compilation; best for interactive debugging.
	Supported by: GCC, Clang
	"""

	O1 = "-O1"
	"""
	Basic optimizations. Reduces code size and execution time without long build delays.
	Supported by: GCC, Clang
	"""

	O2 = "-O2"
	"""
	Moderate optimization. Recommended baseline for production builds.
	Supported by: GCC, Clang
	"""

	O3 = "-O3"
	"""
	Aggressive optimization. Enables autovectorization and heavy loop transformations.
	Supported by: GCC, Clang
	"""

	Os = "-Os"
	"""
	Optimizes for binary size by enabling all -O2 optimizations except those that increase size.
	Supported by: GCC, Clang
	"""

	Oz = "-Oz"
	"""
	Aggressively optimizes to shrink code size further than -Os.
	Supported by: Clang
	"""

	Ofast = "-Ofast"
	"""
	Disregard strict standard compliance for max speed (enables non-IEEE math optimizations).
	Supported by: GCC, Clang
	"""

	Og = "-Og"
	"""
	Optimizes experience for debugging. Enables optimizations that do not interfere with debugging.
	Supported by: GCC, Clang
	"""

	flto = "-flto"
	"""
	Enables Link-Time Optimization across translation units.
	Supported by: GCC, Clang
	"""

	fno_omit_frame_pointer = "-fno-omit-frame-pointer"
	"""
	Keeps the frame pointer in a register for clear call stacks during profiling and debugging.
	Supported by: GCC, Clang
	"""

	fstrict_aliasing = "-fstrict-aliasing"
	"""
	Allows the compiler to assume strict type-based aliasing rules for aggressive optimizations.
	Supported by: GCC, Clang
	"""

	# ==========================================
	# GCC / Clang Standards
	# ==========================================

	std_c89 = "-std=c89"
	"""
	Compiles code using the ANSI C / ISO C89 standard.
	Supported by: GCC, Clang
	"""

	std_c99 = "-std=c99"
	"""
	Compiles code using the ISO C99 standard.
	Supported by: GCC, Clang
	"""

	std_c11 = "-std=c11"
	"""
	Compiles code using the ISO C11 standard.
	Supported by: GCC, Clang
	"""

	std_c17 = "-std=c17"
	"""
	Compiles code using the ISO C17 standard.
	Supported by: GCC, Clang
	"""

	std_c2x = "-std=c2x"
	"""
	Compiles code using the draft ISO C23 standard.
	Supported by: GCC, Clang
	"""

	std_cpp11 = "-std=c++11"
	"""
	Compiles code using the ISO C++11 standard.
	Supported by: GCC, Clang
	"""

	std_cpp14 = "-std=c++14"
	"""
	Compiles code using the ISO C++14 standard.
	Supported by: GCC, Clang
	"""

	std_cpp17 = "-std=c++17"
	"""
	Compiles code using the ISO C++17 standard.
	Supported by: GCC, Clang
	"""

	std_cpp20 = "-std=c++20"
	"""
	Compiles code using the ISO C++20 standard.
	Supported by: GCC, Clang
	"""

	std_cpp23 = "-std=c++23"
	"""
	Compiles code using the draft ISO C++23 standard.
	Supported by: GCC, Clang
	"""

	# ==========================================
	# GCC / Clang Code Gen & Target Architecture
	# ==========================================

	fPIC = "-fPIC"
	"""
	Generates Position Independent Code suitable for shared libraries (.so / .dylib).
	Supported by: GCC, Clang
	"""

	fPIE = "-fPIE"
	"""
	Generates Position Independent Executable code to enable ASLR memory security.
	Supported by: GCC, Clang
	"""

	pipe = "-pipe"
	"""
	Uses pipes rather than temporary files for communication between build stages.
	Supported by: GCC, Clang
	"""

	march_native = "-march=native"
	"""
	Enables instructions supported by the host CPU executing the compilation.
	Supported by: GCC, Clang
	"""

	mtune_native = "-mtune=native"
	"""
	Tunes instruction scheduling for the host CPU without restricting architecture compatibility.
	Supported by: GCC, Clang
	"""

	fvisibility_hidden = "-fvisibility=hidden"
	"""
	Sets default symbol visibility to hidden; requires explicit exports in source code.
	Supported by: GCC, Clang
	"""

	# ==========================================
	# GCC / Clang Debugging & Instrumentation
	# ==========================================

	g = "-g"
	"""
	Generates default operating system debugging information.
	Supported by: GCC, Clang
	"""

	g3 = "-g3"
	"""
	Generates extra debug info, including macro definitions.
	Supported by: GCC, Clang
	"""

	fsanitize_address = "-fsanitize=address"
	"""
	Enables AddressSanitizer (ASan) to catch memory out-of-bounds access and use-after-free bugs.
	Supported by: GCC, Clang
	"""

	fsanitize_undefined = "-fsanitize=undefined"
	"""
	Enables UndefinedBehaviorSanitizer (UBSan) to catch invalid operations at runtime.
	Supported by: GCC, Clang
	"""

	fsanitize_thread = "-fsanitize=thread"
	"""
	Enables ThreadSanitizer (TSan) to detect data races between execution threads.
	Supported by: GCC, Clang
	"""

	fsanitize_leak = "-fsanitize=leak"
	"""
	Enables LeakSanitizer (LSan) to detect memory leaks.
	Supported by: GCC, Clang
	"""

	pthread = "-pthread"
	"""
	Defines macros and flags needed for POSIX thread support.
	Supported by: GCC, Clang
	"""

	# ==========================================
	# MSVC Flags (Windows)
	# ==========================================

	msvc_W0 = "/W0"
	"""
	Disables all compiler warnings.
	Supported by: MSVC
	"""

	msvc_W1 = "/W1"
	"""
	Enables severe warnings.
	Supported by: MSVC
	"""

	msvc_W2 = "/W2"
	"""
	Enables less severe warnings than level 1.
	Supported by: MSVC
	"""

	msvc_W3 = "/W3"
	"""
	Enables production-recommended warnings.
	Supported by: MSVC
	"""

	msvc_W4 = "/W4"
	"""
	Enables strict informational warnings.
	Supported by: MSVC
	"""

	msvc_Wall = "/Wall"
	"""
	Enables all warnings, including those disabled by default.
	Supported by: MSVC
	"""

	msvc_WX = "/WX"
	"""
	Treats all compiler warnings as fatal errors.
	Supported by: MSVC
	"""

	msvc_permissive_off = "/permissive-"
	"""
	Enables strict C++ standards conformance mode.
	Supported by: MSVC
	"""

	msvc_Od = "/Od"
	"""
	Disables code optimizations for faster compilation and easier debugging.
	Supported by: MSVC
	"""

	msvc_O1 = "/O1"
	"""
	Creates small code size binaries.
	Supported by: MSVC
	"""

	msvc_O2 = "/O2"
	"""
	Creates fast execution code binaries.
	Supported by: MSVC
	"""

	msvc_Ox = "/Ox"
	"""
	Enables maximum speed optimization options.
	Supported by: MSVC
	"""

	msvc_GL = "/GL"
	"""
	Enables Whole Program Optimization across compilation units.
	Supported by: MSVC
	"""

	msvc_Oi = "/Oi"
	"""
	Replaces function calls with intrinsic instructions for speed.
	Supported by: MSVC
	"""

	msvc_std_c11 = "/std:c11"
	"""
	Compiles code using the ISO C11 standard.
	Supported by: MSVC
	"""

	msvc_std_c17 = "/std:c17"
	"""
	Compiles code using the ISO C17 standard.
	Supported by: MSVC
	"""

	msvc_std_cpp14 = "/std:c++14"
	"""
	Compiles code using the ISO C++14 standard.
	Supported by: MSVC
	"""

	msvc_std_cpp17 = "/std:c++17"
	"""
	Compiles code using the ISO C++17 standard.
	Supported by: MSVC
	"""

	msvc_std_cpp20 = "/std:c++20"
	"""
	Compiles code using the ISO C++20 standard.
	Supported by: MSVC
	"""

	msvc_std_cpplatest = "/std:c++latest"
	"""
	Enables upcoming preview features from the latest draft C++ standard.
	Supported by: MSVC
	"""

	msvc_MD = "/MD"
	"""
	Links with the multithreaded dynamic C Runtime DLL (MSVCRT.lib).
	Supported by: MSVC
	"""

	msvc_MDd = "/MDd"
	"""
	Links with the debug multithreaded dynamic C Runtime DLL (MSVCRTD.lib).
	Supported by: MSVC
	"""

	msvc_MT = "/MT"
	"""
	Statically links the C Runtime library into the output executable (LIBCMT.lib).
	Supported by: MSVC
	"""

	msvc_MTd = "/MTd"
	"""
	Statically links the debug C Runtime library into the output executable (LIBCMTD.lib).
	Supported by: MSVC
	"""

	msvc_MP = "/MP"
	"""
	Compiles multiple source files concurrently using separate build processes.
	Supported by: MSVC
	"""

	msvc_Zi = "/Zi"
	"""
	Generates a Program Database (PDB) containing complete debug information.
	Supported by: MSVC
	"""

	msvc_Z7 = "/Z7"
	"""
	Embeds C 7.0-compatible debug information directly inside object files (.obj).
	Supported by: MSVC
	"""

	def __str__(self) -> str:
		return self.value


LiteralFlag: TypeAlias = Literal[
	# GCC / Clang Warnings & Diagnostics
	"-Wall",
	"-Wextra",
	"-Wpedantic",
	"-Werror",
	"-Wshadow",
	"-Wconversion",
	"-Wnull-dereference",
	"-Wdouble-promotion",
	"-Wformat=2",
	"-Wimplicit-fallthrough",
	"-Wno-unused-parameter",
	"-Wno-unused-variable",
	"-Wno-unused-function",
	"-Wno-missing-field-initializers",
	# GCC / Clang Optimization
	"-O0",
	"-O1",
	"-O2",
	"-O3",
	"-Os",
	"-Oz",
	"-Ofast",
	"-Og",
	"-flto",
	"-fno-omit-frame-pointer",
	"-fstrict-aliasing",
	# GCC / Clang Standards
	"-std=c89",
	"-std=c99",
	"-std=c11",
	"-std=c17",
	"-std=c2x",
	"-std=c++11",
	"-std=c++14",
	"-std=c++17",
	"-std=c++20",
	"-std=c++23",
	# GCC / Clang Code Gen & Target Architecture
	"-fPIC",
	"-fPIE",
	"-pipe",
	"-march=native",
	"-mtune=native",
	"-fvisibility=hidden",
	# GCC / Clang Debugging & Instrumentation
	"-g",
	"-g3",
	"-fsanitize=address",
	"-fsanitize=undefined",
	"-fsanitize=thread",
	"-fsanitize=leak",
	"-pthread",
	# MSVC Flags (Windows)
	"/W0",
	"/W1",
	"/W2",
	"/W3",
	"/W4",
	"/Wall",
	"/WX",
	"/permissive-",
	"/Od",
	"/O1",
	"/O2",
	"/Ox",
	"/GL",
	"/Oi",
	"/std:c11",
	"/std:c17",
	"/std:c++14",
	"/std:c++17",
	"/std:c++20",
	"/std:c++latest",
	"/MD",
	"/MDd",
	"/MT",
	"/MTd",
	"/MP",
	"/Zi",
	"/Z7",

]

def Macro(name: str, *, value: Any = None, compiler: UsableCompilerType = "gcc") -> str:
	"""
	Generate a macro flag. A compiler needs to be specified. Defaults to GCC / Clang based macro flags.
	"""

	match compiler:
		case "msvc":
			flag = "/D"
		case _:
			flag = "-D"

	return f"{flag}{name}{f'={value}' if value is not None else ''}"

	