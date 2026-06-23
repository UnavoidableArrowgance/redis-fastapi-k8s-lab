#!/bin/bash

for file in scripts/*.sh; do
    if [ ! -x "$file" ]; then
        chmod +x "$file"
    fi
done

echo "Made all .sh files in scripts directory executable."