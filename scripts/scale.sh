#!/bin/bash

set -e

for i in {1..5}; do 
    OUTPUT=$(docker rm --force econ${i})
    docker run -p 800${i}:800${i} -d --name econ${i} -e PORT=800${i} image; 
done

