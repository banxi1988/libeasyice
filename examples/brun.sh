#!/bin/bash
g++ -g udplive.cpp -o file_demo -I../sdk/include -L../sdk/lib -L/usr/local/lib -leasyice -ltr101290 -ldvbpsi -lhlsanalysis
export LD_LIBRARY_PATH=../sdk/lib:/usr/local/lib
./file_demo
