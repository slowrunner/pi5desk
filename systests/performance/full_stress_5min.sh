#!/bin/bash

# REQUIRES:
#  sudo apt install stress


# 0x50000  means throttling occurred, under-voltage occurred  
# 0x50005  means throttled now and under-voltage now  
# 0x80008  means soft temperature limit exceeded (no throttling yet)  

# RESULTS Pi5DESK:

# ********** ROS2 Pi5Desk MONITOR ******************************
# Saturday 12/02/23
#  11:08:28 up 1 day,  2:04,  4 users,  load average: 4.05, 2.25, 0.93
# temp=70.3'C
# frequency(0)=2400004352
# throttled=0x0
#                total        used        free      shared  buff/cache   available
# Mem:           7.9Gi       594Mi       208Mi        33Mi       7.2Gi       7.3Gi
# Swap:           99Mi          0B        99Mi

# (This test on Dave temp throttles)


# stress four cpu cores for 5 minutes
stress -c 4 -t 300
