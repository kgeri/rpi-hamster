#!/usr/bin/env bash
set -e pipefail

BASEDIR=$(dirname "$0")
SRC_DIR=$BASEDIR/src
BUILD_DIR=$BASEDIR/build
PATH=$PATH:$BASEDIR/.venv/bin

printf '\033[32mClean...\033[0m\n' >&2
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

for f in "$SRC_DIR"/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" == "main" ]; then
        continue
    fi
    printf "\033[32mCompiling $BUILD_DIR/$name.mpy\033[0m\n" >&2
    mpy-cross "$f" -o "$BUILD_DIR/$name.mpy"
done

# Clearing the device and uploading
mpremote rm -rf :/ || true
mpremote cp "$SRC_DIR/main.py" :/
for f in "$BUILD_DIR"/*.mpy; do
    mpremote cp "$f" :/
done

# Reset
mpremote reset

printf '\033[32mDeployment successful\033[0m\n' >&2
