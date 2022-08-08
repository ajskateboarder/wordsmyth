#!/bin/bash

set -e

for i in {1..5}; do 
    docker rm --force econ${i};
done

echo "Killed containers successfully"