#!/bin/bash

python3 -m poetry shell
python3 -c "import pyroscope_io as pyroscope;\
	from time import sleep; pyroscope.configure(app_name=\"simple.python.app\",server_address=\"http://pyroscope:4040\");\
	sleep(10)" \
       	| grep -i "upload profile"

