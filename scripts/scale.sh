#!/bin/bash

# Scale up an image, particularly an src/micro app

set -e

if [ $# -eq 0 ]
  then
    echo "Image name not supplied"
    exit 1
fi

for i in {1..5}; do 
    OUTPUT=$(docker rm --force econ${i})
    docker run -p 800${i}:800${i} -d --name econ${i} -e PORT=800${i} $1; 
done

