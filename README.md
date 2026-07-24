
# Zero - Super Easy Build System

`Zero` is a C/C++ build system designed to be as `easy` as possible to use, without lacking any features. Written in python!

The only reason `Zero` exists is because I hate CMake syntax.

## Usage

First, create a `zerobuild.py` file in your project root and import `zero`

```python
from zero import *
```

Create a `Build` object named `build`.

```python
build = Build()
```

Configure the `build` object by specifying the compiler and the build directory.

```python
build.compiler = "gcc"
build.directory = "build" # or Path("build") also works!
```

To create an executable, create an `Executable` object! Specify the sources an arguments!

```python
main = Executable()
main.source = Source(
	"src/main.c",
	"src/utils.c" # or Path("src") / "utils.c" also works!
)
main.arguments = "-Wall", "-O3"
```

And you are done! Yes that's all.
Run the `zero` cli tool to make your executable.
```bash
zero make
```
A binary named `main` can now be found at `build/bin/main`

Read more in [docs](docs/docs.md).

## Installation

`Zero` is still in its infant stage, but you can install it through any pypi package manager. The package name is `zero-build`.
```bash
pip install zero-build
```
> [!WARNING]
> For Linux, You might have to use `--break-system-packages`. This is a workaround for now until I make packages for major Linux distributions.