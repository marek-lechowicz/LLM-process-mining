#!/bin/bash

docker build --tag=tpaszun/thesis:latest .

CONTAINER_ID=$(docker run --rm -d -t tpaszun/thesis bash)

rm -rf solutions/

docker cp $CONTAINER_ID:/thesis/solutions solutions

docker stop $CONTAINER_ID