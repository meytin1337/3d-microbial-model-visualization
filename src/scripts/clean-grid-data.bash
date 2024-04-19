#!/bin/bash
# remove first line of each file
for file in ../../data/grid/grid*.csv; do
  sed -i '1d' "$file"
done
