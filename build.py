#!/usr/bin/env python

import os
import argparse
import sys
import subprocess
import re
import urllib
import datetime

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

cljs_home = os.getenv('CLOJURESCRIPT_HOME')
ng_dir = "./nailgun-0.7.1/"

parser = argparse.ArgumentParser(description='A script for clojurescript autocompiling')
parser.add_argument('-o', help="output file", default="")
parser.add_argument('-i', help="input file")
parser.add_argument('-opts', help="options sent to the compiler", default="")
parser.add_argument('-cljs-home', help="clojurescript home directory", dest="home")
parser.add_argument('-no-persistence', help="build without using persistent jvm", action="store_true", default=False, dest="no_persistence")

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

classpath = ":".join(map((lambda p: cljs_home + "/" + p),  ["lib/*", "src/clj", "src/cljs"]))

def setup_nailgun():
	if not os.path.exists(ng_dir + "ng"):
		print OKBLUE + "Fetching nailgun" + ENDC
		urllib.urlretrieve("https://github.com/downloads/odyssomay/cljs-buildtools/nailgun-0.7.1.zip", "nailgun.zip")
		print OKBLUE + "Unpacking nailgun" + ENDC
		subprocess.call(["unzip", "-o", "-qq", "nailgun.zip"])
		print OKBLUE + "Building nailgun" + ENDC
		subprocess.Popen(["make"], cwd=ng_dir, stdout=subprocess.PIPE).wait()

def init_nailgun():
	test_p = subprocess.Popen([ng_dir + "ng", "clojure.main", "-e", "'hello" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	test_p.wait()
	out = test_p.stdout.read()
	err = test_p.stdout.read()
	if not re.match(r'.*hello.*', out):
		subprocess.Popen(["java", "-server", "-cp",
			classpath + ":" + ng_dir + "nailgun-0.7.1.jar", "com.martiansoftware.nailgun.NGServer"], \
			stdout=subprocess.PIPE).wait()

if not args.no_persistence:
	jvm_cmd = [ng_dir + "ng"]
	setup_nailgun()
	init_nailgun()
else:
	jvm_cmd = ["java", "-cp", classpath]

p = subprocess.Popen(jvm_cmd + ["clojure.main", cljs_home + "/bin/cljsc.clj", args.i, args.opts],\
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out = p.stdout.read()
err = p.stderr.read()
p.wait()

if p.returncode == 0:
	if args.o:
		f = open(args.o, "w")
		f.write(out)
		f.close()
	else:
		sys.stdout.write(out)

sys.stdout.write(err)

sys.exit(p.returncode)
