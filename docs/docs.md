
# Zero - Docs

## Setup

### Installation
Install via the python package `zero-build`.

### Config File
Create a file named `zerobuild.py` in the root of your project. This file will configure the build system.

### Importing
It is recommened to import everything present in the zero module because it will make writing the configuration more easier.
```python
from zero import *
```

## Core API

Zero exposes the following main classes to write the build system.

### Build
This class specifies the general behavior of the build system. The variable to which the `Build()` instance is assigned should be named `build`.
```py
build = Build()
build.compiler = "gcc"
build.directory = "build"
```

> [!NOTE]
> Zero is compatible with python pathlib's `Path` object. So you can also specify the directory as `build.directory = Path("build")`.
> This is useful because:
> - It allows cross platform configuration files to be read more easily
> - It allows you to specify a common directory once.


### Source
A class to specify a group of source files. Can be reused for multiple targets.
```py
source = Source("main.c", "utils.c", ...)
```

### Executable
This class can be use to build an executable. All executables are compiled to `build/bin`.
```py
main = Executable()
main.source = Source("main.c")
main.arguments = "-O3", "-Wall"
main.headers.private = "include" 
```
This will make an exectuable file:
- Located in `build/bin` with the name `main`
- Is compiled from source file `main.c`
- Is compiled with the compiler flags: `-O3` and `-Wall`
- With `include` as the directory where the compiler looks for headers.

You can also assign a custom compiler to `any target` using:
```py
main.compiler = "g++"
```

> [!TIP]
> If you like to add hyphens (`-`) in your executable (which would not be possible in python because hyphens cannot be included in variable names), you can override the name via:
> ```py
> main.name = "main-with-hyphen"
> ```
> `NOTE`: It is now you're responsibility to avoid name conflicts as zero does not handle conflicts for custom names.

### Libraries

#### Target Libraries
Both static and shared libraies can be created with zero. Almost all of the API for these classes is similar to that of `Executable` with a few changes.
```py
static = StaticLibrary()
static.source = ... # Source()
static.arguments = ... # Arguments
static.name = ... # Custom name
static.compiler = ... # Custom compiler

shared = SharedLibrary()
# All other attributes same.
```
These libraries add one more feature concerning headers:
```py
library.header.public = ...
```
This includes the directory(s) in which the compiler looks for headers when targets are linked against this library.

#### Linking
All targets can be linked with libraries via the `.link()` method.
```py
main.link(library)
```

#### Pre-Compiled Libraries
Pre-Compiled libaries can also be linked against.
```py
library = PreCompiledLibrary("path/to/lib")
library.headers.public = "path/to/lib/public/headers"

main.link(library)
```

### Multiple Languages/Compilers

As discussed above, any compiler can be specified for a target as long as it is supported by the system.
```py
build.compiler = "gcc"

target.compiler = "g++"
```
The target `target` is compiled with the `g++` compiler instead of inheriting from the `build` object's compiler.

> [!NOTE]
> For now only some c/c++ compilers are supported but in the future I will:
> 1. Add more compilers for different languages
> 2. Allow the user to build their own compiler class and using it instead of the builtin compilers!

### Side Notes

1. You might have noticed `main.arguments = "-O3", "-Wall"`, this works because in python, any two standalone expressions seperated by a comma will turn into a `Tuple`. So the above expression is really just `main.arguments = ("-O3", "-Wall")`. If you prefer to be explicit you can write the tuple brackets as well.


## CLI

The package comes with a cli tool called `zero` which you can use to actually trigger the build system.

### Make
Start the build using the make command.
```bash
zero make
```
This will make all targets present inside `zerobuild.py`.

To only make custom target(s), specify its name (either the variable name or the custom name in case of hyphens):
```bash
zero make target1 target2
```

To make a fresh build, ignorin stale file detection:
```bash
zero make --fresh
```

### Run
As all executables are compiled to `build/bin`, it can become annoying running `./build/bin/main`, you can run the executable directly:
```bash
zero run main
```
To pass arguments to `main`, just put them after the executable name.
```bash
zero run main --debug --file "file.txt" 
```

`run` will also build the exectuable if it is found but not compiled. You can also compile a fresh build by passing the --fresh flag `TO run` as:
```bash
zero run --fresh main --debug --file "file.txt"
```
If you pass it after the executable name, it will be parsed as an argument to `main`.


