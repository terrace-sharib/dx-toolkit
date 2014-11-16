#!/bin/bash -e

for i in $(seq $(($(nproc)+4))); do
    ./run.sh $i >> $i.log &
done
