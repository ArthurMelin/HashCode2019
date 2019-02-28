#!/bin/bash

for f in *.txt
do
	echo $f
	./hashcode.py $f
done
