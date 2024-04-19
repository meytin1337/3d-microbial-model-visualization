#!/bin/fish
set -l i 1
for file in ../movie-short/IAM_V_M_V*.txt
    mv $file ../movie-short/particles-$i.csv
    set i (math $i+1)
end
