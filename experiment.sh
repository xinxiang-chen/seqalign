#!/bin/bash

# Usage: ./run_basic.sh Datapoints Out/basic

in_dir="Datapoints"    # e.g. Datapoints
out_dir="Out/efficient"   # e.g. Out/basic

if [ -z "$in_dir" ] || [ -z "$out_dir" ]; then
    echo "Usage: $0 <input_folder> <output_folder>"
    exit 1
fi

# Create output folder if it doesn't exist
mkdir -p "$out_dir"

# Loop over every txt file under the input folder
for infile in "$in_dir"/*.txt; do
    # Skip if no files match
    [ -e "$infile" ] || continue

    base=$(basename "$infile")   # e.g. in1.txt
    num="${base#in}"            # remove 'in' -> 1.txt
    num="${num%.txt}"           # remove '.txt' -> 1

    outfile="$out_dir/out${num}.txt"  # e.g. Out/basic/out1.txt

    echo "Running: python3 efficient.py \"$infile\" \"$outfile\""
    python3 efficient.py "$infile" "$outfile"
done