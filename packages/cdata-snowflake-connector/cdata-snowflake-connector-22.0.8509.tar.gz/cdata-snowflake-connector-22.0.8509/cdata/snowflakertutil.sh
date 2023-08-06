#!/bin/bash
BASE_PATH=
LOCAL_PATH=
RUNTIME_FOLDER_NAME="jre"
RUNTIME_FOLDER_NAME_ARM64="jre17_aarch64"
JRE17_ZIP_FILE="jre_arm64.tar.gz"
JRE17_FOLDER_NAME="jdk-17.0.5+8-jre"
JRE8_ZIP_FILE="jre.tar.gz"
JRE8_FOLDER_NAME="jdk8u345-b01-jre"
ACTION="INSTALL"
ARCH="x86_64"
JRE_RELEASE="Contents/Home/release"

help() {
  echo "Usage: "
  echo "snowflakertutil.sh -b <base path> -l <local path> -a <CPU architecture>"
  echo
  echo "Description:"
  echo "-u    uninstall runtime."
  echo "-b    base path."
  echo "-l    local path."
  echo "-a    CPU architecture."
  
  exit -1
}

while getopts "i:u:b:l:a:" opt; do
  case $opt in
    u)
      ACTION="UNINSTALL"
      ;;
    b)
      BASE_PATH=$OPTARG
      echo "BASE_PATH : $BASE_PATH"
      ACTION="INSTALL"
      ;;
    l)
      LOCAL_PATH=$OPTARG
      echo "LOCAL_PATH : $LOCAL_PATH"
      ACTION="INSTALL"
      ;;
    a)
      ARCH=$OPTARG
      echo "ARCH : $ARCH"
      ;;      
    ?) help;;
  esac
done

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
NEED_JRE_8="false"
NEED_JRE_17="false"

if [ $ACTION == "INSTALL" ]; then
  if [ ! -d "$BASE_PATH/$RUNTIME_FOLDER_NAME" ]; then
    NEED_JRE_8="true"   
  fi

  if [ ! -d "$LOCAL_PATH/$RUNTIME_FOLDER_NAME" ]; then
    NEED_JRE_8="true"	
  fi

  if [ $ARCH == "arm64" ]; then
    if [ ! -d "$BASE_PATH/$RUNTIME_FOLDER_NAME_ARM64" ]; then
      NEED_JRE_17="true"   
    fi

    if [ ! -d "$LOCAL_PATH/$RUNTIME_FOLDER_NAME_ARM64" ]; then
      NEED_JRE_17="true"	
    fi
  fi

  if [ $NEED_JRE_8 == "false" ]  && [ $NEED_JRE_17 == "false" ]; then
    echo "The runtime home exists."
    exit -1
  fi

  echo "The runtime home does not exist. Creating the runtime home..."

  RUNTIME_TEMP_DIR=`mktemp -d -t cdatatmpXXXXXXXXXXXX`

  # check if tmp dir was created
  if [[ ! "$RUNTIME_TEMP_DIR" || ! -d "$RUNTIME_TEMP_DIR" ]]; then
    echo "Could not create temp dir"
    exit 1
  fi

  # deletes the temp directory
  function cleanup {      
    rm -rf "$RUNTIME_TEMP_DIR"
    echo "Deleted temp working directory $RUNTIME_TEMP_DIR"
  }

  # register the cleanup function to be called on the EXIT signal
  trap cleanup EXIT
  
  if [ ! -d $LOCAL_PATH ]; then
    mkdir -p $LOCAL_PATH
    echo "Create folder $LOCAL_PATH"
  fi

  if [ ! -d $BASE_PATH ]; then
    mkdir -p $BASE_PATH
    echo "Create folder $BASE_PATH"
  fi

  #Unzip jre8_x86_64
  if [ $NEED_JRE_8 == "true" ]; then
    tar -xvf $CURRENT_DIR/$JRE8_ZIP_FILE -C $RUNTIME_TEMP_DIR
    cp -r $RUNTIME_TEMP_DIR/$JRE8_FOLDER_NAME $LOCAL_PATH/$RUNTIME_FOLDER_NAME
    cp -r $RUNTIME_TEMP_DIR/$JRE8_FOLDER_NAME $BASE_PATH/$RUNTIME_FOLDER_NAME
  fi

  #Unzip jre17_aarch64
  if [ $NEED_JRE_17 == "true" ]; then  
    tar -xvf $CURRENT_DIR/$JRE17_ZIP_FILE -C $RUNTIME_TEMP_DIR
    cp -r $RUNTIME_TEMP_DIR/$JRE17_FOLDER_NAME $LOCAL_PATH/$RUNTIME_FOLDER_NAME_ARM64
    cp -r $RUNTIME_TEMP_DIR/$JRE17_FOLDER_NAME $BASE_PATH/$RUNTIME_FOLDER_NAME_ARM64
  fi
elif [ $ACTION == "UNINSTALL" ]; then
  rm -rf $CURRENT_DIR/$RUNTIME_FOLDER_NAME
  rm -rf $CURRENT_DIR/$RUNTIME_FOLDER_NAME_ARM64
fi
