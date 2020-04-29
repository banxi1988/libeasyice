#!/bin/bash

export LD_LIBRARY_PATH=../sdk/lib

#./tsplay hello.ts  127.0.0.1:1234 >/dev/null 2>&1 &
ffmpeg -re -i /home/codetalks/bili.mp4 -c copy -f mpegts "udp://127.0.0.1:1234" >/dev/null 2>&1 &
#valgrind --leak-check=full  --show-reachable=yes ./test_app_udplive
./test_app_udplive > udp2.log