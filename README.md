# linux-distance-tracker
Linux distance tracker

## Installation

### Build requirements

To build, you need:

* meson build system
* a working C/C++ compiler
* python 3.7+

### Build
In the project dir, run

```
meson build
cd build
meson compile
```

### Install

To install, run (still from ./build)

```
sudo meson install
```

Note that if you skip this step, the application may not find some important files like UI templates and icons.

