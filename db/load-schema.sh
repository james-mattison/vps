#!/bin/bash

set -ex
mysql < schema.sql

if [ $? -eq 0 ]; then
	echo Loaded schema
else
	echo Failed to load schema
fi

