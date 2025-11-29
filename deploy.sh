#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(dirname "$0")/src
BUILD_DIR=$(dirname "$0")/build

echo "Cleaning build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Compiling .py files to .mpy..."
for f in "$PROJECT_DIR"/*.py; do
    name=$(basename "$f" .py)
    echo "  $f → $BUILD_DIR/$name.mpy"
    mpy-cross "$f" -o "$BUILD_DIR/$name.mpy"
done

echo "Uploading to MicroPython device..."
mpremote connect auto fs mkdir /app || true

for f in "$BUILD_DIR"/*.mpy; do
    echo "  Uploading $f"
    mpremote connect auto fs cp "$f" :/app/
done

echo "Setting main.py entrypoint..."
mpremote connect auto fs cp main.py :main.py

echo "Done."
