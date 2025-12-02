#!/usr/bin/env bash
set -e pipefail

BASEDIR=$(dirname "$0")
SRC_DIR=$BASEDIR/src
BUILD_DIR=$BASEDIR/build
PATH=$PATH:$BASEDIR/.venv/bin

printf '\033[32mClean...\033[0m\n' >&2
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Clearing the device, compiling and uploading
mpremote rm -rf :/ || true
# Not compiling main.py, as it's expected by boot to be a .py file
mpremote cp "$SRC_DIR/main.py" :/
for d in $(find "$SRC_DIR" -type d ! -name __pycache__); do
    dir="${d#"$SRC_DIR"}"
    mkdir -p $BUILD_DIR$dir
    mpremote mkdir ":$dir" || true
    
    for f in "$d"/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" == "main" ]; then
            continue
        fi
        mpy-cross "$f" -o "$BUILD_DIR$dir/$name.mpy"
        mpremote cp "$BUILD_DIR$dir/$name.mpy" ":$dir"
    done
done

# Reset
mpremote reset

printf '\033[32mDeployment successful\033[0m\n' >&2
