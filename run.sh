for file in $(ls benchmarks/data/*.txt); do
    python3 palletizationWithConstraints.py -f $file
done