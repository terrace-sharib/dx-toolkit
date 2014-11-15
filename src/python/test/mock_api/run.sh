#!/bin/bash

set -e

if [[ $1 == "" ]]; then
    PORT=5000
else
    PORT=$((5000+$1))
fi

./api.py --port $PORT > /dev/null 2>&1 &
MOCK_SERVER_PID=$!

cleanup() {
    kill $MOCK_SERVER_PID
}

trap cleanup EXIT

sleep 5

export DX_APISERVER_PROTOCOL=http
export DX_APISERVER_HOST=localhost
export DX_APISERVER_PORT=$PORT
#export _DX_DEBUG=1

for i in {1..1024}; do
    wire_md5=$(dx download test --output - 2>/dev/null | md5sum | cut -f 1 -d " ")
    desc_md5=$(dx api file-test describe | jq --raw-output .md5)
    echo $i $wire_md5 $desc_md5
    if ! [[ $wire_md5 == $desc_md5 ]]; then
        exit 1
    fi
done
