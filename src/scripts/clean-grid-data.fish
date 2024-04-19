#!/bin/fish
# remove first line of each file
for file in ../movie-short/grid*.csv
  sed -i '1d' $file
end
