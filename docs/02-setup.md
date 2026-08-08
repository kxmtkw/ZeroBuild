
## Setup

### Installation
`Zero` is still in its infant stage, but you can install it through any pypi package manager. The package name is `zero-build`.
```bash
pip install zero-build
```
> [!WARNING]
> For Linux, You might have to use `--break-system-packages`. This is a workaround for now until I make packages for major Linux distributions.

### Configuration
Create a config script/file named `zerobuild.py` in the root of your project. This file will be used to configure the build system.


### Importing
It is recommened to import everything present in the zero module because it will make writing the configuration more easier.
```python
from zero import *
```