#!/bin/bash
# remove leading spaces and replace double spaces with commas
for file in ../../data/particles/particles*; do
  sed -i 's/^  *//' "$file"
  sed -i 's/  /,/g' "$file"
done
