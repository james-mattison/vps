#!/bin/bash

ROOT=$( dirname $( dirname $( realpath $0 )))

cd "$ROOT"

docker build -t core .

cd db

docker build -t core .

cd "$ROOT"

