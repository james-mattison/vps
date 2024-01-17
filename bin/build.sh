#!/bin/bash

ROOT=$( dirname $( dirname $( realpath $0 )))

cd "$ROOT"

docker build -t app .

cd db

docker build -t db .

cd "$ROOT"

