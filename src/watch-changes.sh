#!/bin/bash

watchmedo shell-command \
    --patterns="*.py;*.txt" \
    --recursive \
    --command='python3 '$1 \