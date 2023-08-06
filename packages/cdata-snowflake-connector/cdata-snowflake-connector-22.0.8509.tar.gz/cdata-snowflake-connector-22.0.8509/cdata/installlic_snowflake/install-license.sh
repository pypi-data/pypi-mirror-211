#!/bin/sh
set -eu

case "$(uname -s)" in
    Linux*)
        LIB_DIR=..
        JRE_HOME=$LIB_DIR/jre
        ;;

    Darwin*)
        LIB_DIR=..
        JRE_HOME=$LIB_DIR/jre/Contents/Home
        ;;
esac

$JRE_HOME/bin/java -jar $LIB_DIR/cdata.pycore.snowflake.jar -l $*