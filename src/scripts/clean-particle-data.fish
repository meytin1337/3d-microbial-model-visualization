#!/bin/fish
# remove leading spaces and replace double spaces with commas
for file in ../../data/particles/particles*
  sed -i 's/^  *//' $file
  sed -i 's/  /,/g' $file
end
