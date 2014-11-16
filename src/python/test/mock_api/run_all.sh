#!/bin/bash -e

for i in {1..$(($(nproc)+4))}; do
    ./run.sh $((5000+$i)) >> $i.log &
done
