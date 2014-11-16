#!/bin/bash -e

#for i in {1..$(($(nproc)+4))}; do
for i in {1..24}; do
    ./run.sh $((5000+$i)) >> $i.log &
done
