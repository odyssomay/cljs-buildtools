#!/usr/bin/env python

import argparse
import os
import sys
import subprocess
import hashlib
import time
import datetime
import urllib

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

cljs_home = os.getenv('CLOJURESCRIPT_HOME')

parser = argparse.ArgumentParser(description='A script for clojurescript autocompiling')
parser.add_argument('-o', help="output file", default="")
parser.add_argument('-i', help="input file")
parser.add_argument('-opts', help="options sent to the compiler", default="")
parser.add_argument('-cljs-home', help="clojurescript home directory", dest="home")
parser.add_argument('-no-persistence', help="build without using persistent jvm", action="store_true", default=False)

args = parser.parse_args()

if args.home:
	cljs_home = args.home

if not cljs_home:
	print FAIL + "ERROR: You must specify CLOJURESCRIPT_HOME " \
	      + "or use option -cljs-home" + ENDC
	sys.exit(1)

if not args.i:
	print FAIL + "ERROR: no input specified, use option -i" + ENDC
	sys.exit(1)

if not args.o:
	print WARNING + "WARNING: no output specified" + ENDC

if not os.path.exists("build.py"):
	print OKBLUE + "Fetching build script" + ENDC
	urllib.urlretrieve("https://raw.github.com/odyssomay/cljs-buildtools/master/build.py", "build.py")
	subprocess.Popen(["chmod +x build.py"], shell=True).wait()

def hash_sum(s):
	return hashlib.sha1(s).hexdigest()

def get_status(target):
	p = subprocess.Popen(["ls", "-l", target], stdout=subprocess.PIPE)
	p.wait()
	return p.stdout.read()

def get_status_hash(target):
	return hash_sum(get_status(target))

def build(target, options):
	print OKBLUE + "Building..." + ENDC,
	sys.stdout.flush()
	p = subprocess.Popen(["./build.py", "-i", target, "-o", args.o, "-cljs-home", cljs_home, "-opts", options], \
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	out = p.stdout.read()
	err = p.stderr.read()

	if p.returncode == 0:
		print OKGREEN + "success!" + HEADER + " Built " + str(target) + " at",
		print datetime.datetime.now().strftime("%H:%M:%S") + ENDC
		if args.o:
			f = open(args.o, "w")
			f.write(out)
	else:
		print FAIL + "failed!" + ENDC
	
	sys.stdout.write(out)
	sys.stdout.write(err)

while True:
	hsum1 = get_status_hash(args.i)
	hsum2 = hsum1
	build(args.i, args.opts)
	while hsum1 == hsum2:
		time.sleep(0.5)
		hsum2 = get_status_hash(args.i)

