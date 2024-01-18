#!/bin/bash

set -ex
mysql -uroot -p123456 -h10.0.0.10 < schema.sql

if [ $? -eq 0 ]; then
	echo Loaded schema
else
	echo Failed to load schema
fi

