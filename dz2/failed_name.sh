#!/bin/bash

function failed_name {
    local dir="$1"

    for item in "$dir"/*; do
        if [[ -d "$item" ]]; then
                failed_name "$item"
        elif [[ -f "$item" ]]; then
            filename=$(basename "$item")
            if [[ "$filename" =~ [^a-zA-Z0-9_.-] ]]; then
                # rm "$item"
		echo "DELETE: $item"
            fi
        fi
    done
}

#dir="/home/are/dz2"
failed_name "."


