#!/bin/bash
cd $(dirname $0)
ARGS=$@
TRAP=""
while [ $1 ]; do
	if [[ -n $TRAP ]]; then
		TRAP="$TRAP ;"
	fi
	TRAP="$TRAP echo $1 > /sys/class/gpio/unexport"
	shift
done
trap "$TRAP" EXIT
./RasPi_logGPIO $ARGS
