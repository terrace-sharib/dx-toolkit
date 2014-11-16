#!/bin/bash -e

#for i in {1..24}; do
for i in $(seq $(($(nproc)/2))); do
    ./run.sh $i >> $i.log &
done
