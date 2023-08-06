#!/bin/bash
INSTALL_PATH=
PYTHON_VERSION=
OS=
FILES=

help() {
  echo "Usage: "
  echo "snowflakecleanup.sh -p <install path> -o <operating system> -v <python version>"
  echo
  echo "Description:"
  echo "-p    install path."
  echo "-o    operating system."
  echo "-v    python version."
  
  exit -1
}

while getopts "p:o:v:" opt; do
  case $opt in
    p)
      INSTALL_PATH=$OPTARG
      ;;
    o)
      OS=$OPTARG
      ;;
    v)
      PYTHON_VERSION=$OPTARG
      ;;      
    ?) help;;
  esac
done

if [ $OS == "linux" ]; then 
  CURRENT_DIR="$( pwd )"
  INSTALL_PATH="$CURRENT_DIR/build/bdist.linux-x86_64/wheel/cdata"
  if [ $PYTHON_VERSION == "py37" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-38-x86_64-linux-gnu.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-39-x86_64-linux-gnu.so"
    FILES[2]="$INSTALL_PATH/snowflake.cpython-310-x86_64-linux-gnu.so"
  elif [ $PYTHON_VERSION == "py38" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-37m-x86_64-linux-gnu.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-39-x86_64-linux-gnu.so"
    FILES[2]="$INSTALL_PATH/snowflake.cpython-310-x86_64-linux-gnu.so"
  elif [ $PYTHON_VERSION == "py39" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-37m-x86_64-linux-gnu.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-38-x86_64-linux-gnu.so"
    FILES[2]="$INSTALL_PATH/snowflake.cpython-310-x86_64-linux-gnu.so"
  elif [ $PYTHON_VERSION == "py310" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-37m-x86_64-linux-gnu.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-38-x86_64-linux-gnu.so"
    FILES[2]="$INSTALL_PATH/snowflake.cpython-39-x86_64-linux-gnu.so"
  fi
elif [ $OS == "darwin" ]; then
  if [ $PYTHON_VERSION == "py38" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-39-darwin.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-310-darwin.so"
  elif [ $PYTHON_VERSION == "py39" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-38-darwin.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-310-darwin.so"
  elif [ $PYTHON_VERSION == "py310" ]; then
    FILES[0]="$INSTALL_PATH/snowflake.cpython-38-darwin.so"
    FILES[1]="$INSTALL_PATH/snowflake.cpython-39-darwin.so" 
  fi
fi  

#Remove redundant .so files from the installation directory
for file in "${FILES[@]}"
do
  rm -rf $file
done

#Delete cleanup.sh from the installation directory
rm -rf $INSTALL_PATH/snowflakecleanup.sh