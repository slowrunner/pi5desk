#!/bin/bash
#
# totallife.sh    print total hours and sessions of life in life.log
#
# requires bc  (sudo apt-get install bc)
#
echo "(Cleaning life.log first)"
/home/pi/pi5desk/plib/cleanlifelog.py
echo " "
fn="/home/pi/pi5desk/logs/life.log"
totalLife=`(awk -F':' '{sum+=$3}END{print sum;}' $fn)`
echo "*** Pi5DESK TOTAL LIFE STATISTICS ***"
echo "Total Life: " $totalLife "hrs (since Nov 28, 2023)"
echo "Sessions (boot): " `(grep -c "\- boot \-" $fn)`
booted=`(grep -c "\- boot \-" $fn)`
aveSession=`(echo "scale=1; ($totalLife / $booted)" | bc -l)`
echo "Average Session: " $aveSession "hrs"
safetyShutdowns=`(grep -c "SAFETY SHUTDOWN" $fn)`
echo "Safety Shutdowns: " $safetyShutdowns 
