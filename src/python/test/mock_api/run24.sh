#!/bin/bash -e

for i in {1..24}; do
    ./run.sh $((5000+$i))  >> $i.log &
done
