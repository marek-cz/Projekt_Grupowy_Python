#!/bin/bash

while true
do
	python3  socket_serwer.py 
	echo "\n\nAby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)
	echo "\n\nAby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)
	echo "\n\nAby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)
	echo "\n\nAby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)

done
