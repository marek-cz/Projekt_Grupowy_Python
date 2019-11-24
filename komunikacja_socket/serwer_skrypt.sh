#!/bin/bash

while true
do
	python3  socket_serwer.py 
	echo "Aby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)
	echo "Aby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)
	echo "Aby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)
	echo "Aby wyjsc CTRL + C"
	sleep 5
	kill $(lsof -t -i:5005)

done
