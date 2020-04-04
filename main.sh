#!/bin/bash

if ! [ -d "COVID-19" ]; then
	echo "Cloning repository"
	git clone https://github.com/pcm-dpc/COVID-19.git 1>/dev/null

else
	echo "Updating repository"
	cd "COVID-19"
	git pull origin 1>/dev/null
	cd ..
fi

python3 utils/plotter.py "$@"
