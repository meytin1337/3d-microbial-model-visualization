#!/bin/bash
i=1
for file in ../../data/grid/IAM_B_C_*.txt
do
    mv "$file" "../../data/grid/grid-$i.csv"
    i=$((i + 1))
done
