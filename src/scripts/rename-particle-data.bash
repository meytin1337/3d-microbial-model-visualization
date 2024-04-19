
#!/bin/bash
i=1
for file in ../../data/particles/IAM_B_C_*.txt
do
    mv "$file" "../../data/particles/particles-$i.csv"
    i=$((i + 1))
done
