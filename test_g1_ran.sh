#!/bin/bash

function getServerMetrics {
    # Server metrics 9097
    python get_server_metrics.py 9097
    # Server metrics 9098
    python get_server_metrics.py 9098
    # Server metrics 9099
    python get_server_metrics.py 9099
}

rm *_1.metrics

# TEST PUT GROUP 1 Random
for FILE in $(pwd)/G1_FILES/*; 
    do 
        python $(pwd)/cliente.py 0 1 PUT "ACG1/${FILE##*/}";
done

# Metrics for Random PUT Group 1
python get_metrics.py 0 PUT 1
echo "Server storage for RANDOM GROUP 1"
getServerMetrics
