
A simple autobuild tool paired with a persistent build script for clojurescript.

## Installation

For autobuild only [`autobuild.py`](https://raw.github.com/odyssomay/cljs-buildtools/master/autobuild.py) is needed.

For build script use [`build.py`](https://raw.github.com/odyssomay/cljs-buildtools/master/build.py).

## Usage

Usage is the same for both scripts.

`
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
`

The `-no-persistence` can be used if there is a problem with nailgun.

## Old scripts

There is an older script which can be used if there is a problem with for example python.

You need both [`autobuild.sh`](https://github.com/odyssomay/cljs-buildtools/blob/master/old/autobuild.sh) and
[`autobuild.clj`](https://github.com/odyssomay/cljs-buildtools/blob/master/old/autobuild.clj) in the same directory.

The usage is as follows:

`
1st argument: path to clojurescript
2nd argument: path to file to compile
3rd argument or more: optional, paths to files to watch (but not compile)
last argument: optional, options to be passed to compiler 
`

Note that it isn't possible to compile directories with this script.

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

