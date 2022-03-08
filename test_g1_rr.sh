#!/bin/bash

function getServerMetrics {
    # Server metrics 9097
    python get_server_metrics.py 9097
    # Server metrics 9098
    python get_server_metrics.py 9098
    # Server metrics 9099
    python get_server_metrics.py 9099
}


# Remove group 1 metrics
rm *_1.metrics

# TEST PUT GROUP 1 Round Robin
for FILE in $(pwd)/G1_FILES/*; 
    do 
        python $(pwd)/cliente.py 1 1 PUT "RRCG1/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# Metrics for Round Robin PUT Group 1
python get_metrics.py 1 PUT 1
echo "Server storage for ROUND ROBIN GROUP 1"
getServerMetrics
rm server_*.metrics
