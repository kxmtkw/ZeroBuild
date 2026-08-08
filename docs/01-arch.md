
## Architecture

*Zero* is a build system, not a meta build system. It handles dependency resolution to compilation and linking by itself.

### Design Goal
The sole reason Zero exists is because *I did not want to learn CMake syntax.* There is absolutely no reason other than that.

My main design goal for this project was to make a build system which as easy to write as possible. 

Zero also avoid implictness,
the user has to be explicit with their flags and compilers to use the build system properly.

### Principle
Like most build systems, Zero uses a *DAG* (Directed Acyclic Graph) to handle dependencies.

### Working
Zero works in the following phases after it is invoked:
```
┌───────────────────────┐
│ Config Script Loading │
└───────────────────────┘
           |
           V
┌───────────────────────┐
│  Graph Construction   │
└───────────────────────┘
           |
           V
┌───────────────────────┐
│    Cycle Detection    │
└───────────────────────┘
           |
           V
┌───────────────────────┐
│  Staleness Detection  │
└───────────────────────┘
           |
           V
┌───────────────────────┐
│      Build Phase      │
└───────────────────────┘
```

---