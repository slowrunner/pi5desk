#!/bin/bash

cd ~/wali_desk/c3ws

echo "Removing c3ws/src/create3_sim and cleaning build/install/log folders"
rm -rf src/create3_sim
rm -rf log
rm -rf install
rm -rf build

echo "Done\n"
