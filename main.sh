#!/bin/bash
# The line above is the "shebang". It tells the system to use Bash to run this file.

python3 src/main.py
cd public && python3 -m http.server 8888
