#!/usr/bin/env python

import argparse
import os
import sys
import subprocess
import hashlib
import time
import datetime
import urllib
import re

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

cljs_home = os.getenv('CLOJURESCRIPT_HOME')
ng_dir = "./.nailgun/nailgun-0.7.1/"

parser = argparse.ArgumentParser(description='A script for clojurescript autocompiling')
parser.add_argument('-o', help="output file", default="")
parser.add_argument('-i', help="input file")
parser.add_argument('-opts', help="options sent to the compiler", default="")
parser.add_argument('-cljs-home', help="clojurescript home directory", dest="home")
parser.add_argument('-no-persistence', help="build without using persistent jvm", action="store_true", default=False)
parser.add_argument('-cp', help="include path to classpath", default="")

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

# ----------------------------------------------------
# file status

def hash_sum(s):
	return hashlib.sha1(s).hexdigest()

def get_status(target):
	p = subprocess.Popen(["ls", "-l", target], stdout=subprocess.PIPE)
	return p.communicate()[0]

def get_status_hash(target):
	return hash_sum(get_status(target))

# ----------------------------------------------------
# nailgun / java env

classpath = ":".join(map((lambda p: cljs_home + "/" + p),  ["lib/*", "src/clj", "src/cljs"]))

if args.cp:
	classpath = classpath + ":" + args.cp

def setup_nailgun():
	if not os.path.exists('.nailgun'):
		os.makedirs('.nailgun')
		if not os.path.exists(ng_dir + "ng"):
			print OKBLUE + "Fetching nailgun" + ENDC
			urllib.urlretrieve("https://github.com/downloads/odyssomay/cljs-buildtools/nailgun-0.7.1.zip", "nailgun.zip")
			print OKBLUE + "Unpacking nailgun" + ENDC
			subprocess.call(["unzip", "-o", "-qq", "-d", ".nailgun", "nailgun.zip"])
			os.remove('nailgun.zip')
			print OKBLUE + "Building nailgun" + ENDC
			subprocess.Popen(["make"], cwd=ng_dir, stdout=subprocess.PIPE).wait()

def nailgun_started():
	test_p = subprocess.Popen([ng_dir + "ng", "clojure.main", "-e", "'hello" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = test_p.communicate()
	if re.match(r'.*hello.*', out):
		return True
	else:
		return False

def init_nailgun():
	if not nailgun_started():
		print OKBLUE + "Starting nailgun server" + ENDC
		p = subprocess.Popen(["java", "-server", "-cp",
			classpath + ":" + ng_dir + "nailgun-0.7.1.jar", "com.martiansoftware.nailgun.NGServer"],
			stdout=subprocess.PIPE)
		while not nailgun_started():
			time.sleep(0.1)
			p.poll()
			if p.returncode and p.returncode != 0:
				print FAIL + "Failed starting nailgun, using non-persistent fallback" + ENDC
				return False
	return True

if not args.no_persistence:
	jvm_cmd = [ng_dir + "ng"]
	setup_nailgun()
	if not init_nailgun():
		jvm_cmd = ["java", "-cp", classpath]
else:
	jvm_cmd = ["java", "-cp", classpath]

# ----------------------------------------------------
# build

def build(target, options):
	print OKBLUE + "Building..." + ENDC,
	sys.stdout.flush()
	p = subprocess.Popen(jvm_cmd + ["clojure.main", cljs_home + "/bin/cljsc.clj", args.i, args.opts],\
						 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()

	if p.returncode == 0:
		print OKGREEN + "success!" + HEADER + " Built " + str(target) + " at",
		print datetime.datetime.now().strftime("%H:%M:%S") + ENDC
		if args.o:
			f = open(args.o, "w")
			f.write(out)
			f.close()
		else:
			sys.stdout.write(out)
	else:
		print FAIL + "failed!" + ENDC
	
	sys.stdout.write(err)

# ----------------------------------------------------
# main loop

try:
	while True:
		hsum1 = get_status_hash(args.i)
		hsum2 = hsum1
		build(args.i, args.opts)
		while hsum1 == hsum2:
			time.sleep(0.5)
			hsum2 = get_status_hash(args.i)
except KeyboardInterrupt:
	if nailgun_started():
		print OKBLUE + "Shutting down nailgun" + ENDC
		sys.stdout.flush()
		subprocess.Popen([ng_dir + "ng", "ng-stop"]).wait()

