
A simple autobuild tool paired with a persistent build script for clojurescript.

## Installation

For autobuild only [`autobuild.py`](https://raw.github.com/odyssomay/cljs-buildtools/master/autobuild.py) is needed.

For build script use [`build.py`](https://raw.github.com/odyssomay/cljs-buildtools/master/build.py).

## Usage

```
> ./autobuild.py -h
usage: autobuild.py [-h] [-o O] [-i I] [-opts OPTS] [-cljs-home HOME]
                    [-no-persistence]

A script for clojurescript autocompiling

optional arguments:
  -h, --help       show this help message and exit
  -o O             output file
  -i I             input file
  -opts OPTS       options sent to the compiler
  -cljs-home HOME  clojurescript home directory
  -no-persistence  build without using persistent jvm
```

## License (zlib) 

Copyright (c) 2011 Jonathan Fischer Friberg

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

