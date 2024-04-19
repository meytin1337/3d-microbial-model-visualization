#!/bin/fish
set -l i 1
for file in ../../data/grid/IAM_B_C_*.txt
    mv $file ../../data/grid/grid-$i.csv
    set i (math $i+1)
end
