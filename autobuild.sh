#!/bin/sh

SCRIPT=`readlink -f $0`
SCRIPTPATH=`dirname $SCRIPT`

if [ "$1" == "" -o "$2" == "" ]; then
	echo "
1st argument:         path to clojurescript
2nd argument:         path to file/dir to compile
3rd argument or more: optional, paths to files to watch (but not compile)
last argument:        optional, options to be passed to compiler"
	exit 1
fi

CLOJURESCRIPT_HOME=$1

CLJSC_CP=''
for next in lib/*: src/clj: src/cljs: test/cljs; do
  CLJSC_CP=$CLJSC_CP$CLOJURESCRIPT_HOME'/'$next
done

java -server -cp $CLJSC_CP clojure.main $SCRIPTPATH/autobuild.clj $*

