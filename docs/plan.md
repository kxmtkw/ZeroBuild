# Feature Plan

## Must Have 

+ Libraries (Shared + Static) `Done`

+ Pre Compiled Libraries `Done`

+ Linking C libs with C++ libs and vice versa `Done`
	+ This currently fails because only a single compiler can be chosen.
		+ Either we select compiler per target.
		+ Or let the system pick g++ for C++ files automatically.

+ Arguments `Done`
	+ Per target `Done`

+ More Compilers
	+ MSVC, G++, Clang++ `In-Progress`
	+ Name Compilers to Compiler Drivers because that's more accurate.

+ Stale detection and avoiding recompilation `Done`

+ Multi OS support
	+ Linux `In-Progress`
	+ Windows
	+ MacOS


## Should have 
+ Multiple targets can depend on the same stuff.
	+ If they depend on the same library then thats trivial to handle, no worry.
	+ If they depend on the same source file (mid-level edge case), we create seperate nodes entirely to avoid arguments conflict.
		+ That means the object files must be sorted by target in the objects/

+ Threading/Multiprocessing compilation
	+ Requires converting the graph into a 1D array so the builder can multiprocess

+ Add more visitors.
	+ Cycle detectors `Done`
	+ Change detectors `Done`

+ Readable error messages
	+ Traceback upto the user script level
	+ Different and clear error types

+ Clearer and Prettier log messages. `In-Progress`
	+ use rich

+ Executable to run the build file automatically. `In-Progress`
	+ Could be faked by just running zero.py with specific arguments.
```bash
zero build # runs the zero.py file
zero build --fresh
zero run bin/main -- --debug
```
+ Also allow user arguments. 
```bash
zero build --debug
```

+ Allow the user to control the build system more.
	+ Allow the user to make custom CompilerDrivers to the build system. 

+ A CMAKE transpiler that turns the DAG into a `CMakeLists.txt` file.
	+ This is actually simpler than I thought. Just traverse the DAG and build the CMAKE file as we go.

## Could have

+ Live file watcher to instantly recompile.
	+ Requires watching every file node in the graph and triggering the build sequence once any file changes.
	+ Could wait for something like `n` changes.



