#!/bin/bash

cd ..
cd src || return

python run_cli.py "$@"