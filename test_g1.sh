#!/bin/bash

function getServerMetrics {
    # Server metrics 9097
    python get_server_metrics.py 9097
    # Server metrics 9098
    python get_server_metrics.py 9098
    # Server metrics 9099
    python get_server_metrics.py 9099
}

export G=1
export ALG=0

# remove metrics existing.
rm *_$G.metrics
# Remove existing loaded files
rm -rf ACG${G}
rm -rf RRCG${G}
rm -rf HCG${G}

# TEST PUT GROUP 1 Random
for FILE in $(pwd)/G${G}_FILES/*; 
    do 
        python $(pwd)/cliente.py $ALG $G PUT "ACG${G}/${FILE##*/}";
done

# Metrics for Random PUT Group 1
python get_metrics.py $ALG PUT $G
echo "Server storage for RANDOM GROUP ${G}"
getServerMetrics
rm server_*.metrics

export ALG=1

# TEST PUT GROUP 1 Round Robin
for FILE in $(pwd)/G${G}_FILES/*; 
    do 
        python $(pwd)/cliente.py $ALG $G PUT "RRCG${G}/${FILE##*/}";
done

# Metrics for Round Robin PUT Group 1
python get_metrics.py $ALG PUT $G
echo "Server storage for Round Robin GROUP ${G}"
getServerMetrics
rm server_*.metrics


export ALG=2

# TEST PUT GROUP 1 HASH
for FILE in $(pwd)/G${G}_FILES/*; 
    do 
        python $(pwd)/cliente.py $ALG $G PUT "HCG${G}/${FILE##*/}";
done

# Metrics for Hash PUT Group 1
python get_metrics.py $ALG PUT $G
echo "Server storage for Hash GROUP ${G}"
getServerMetrics
rm server_*.metrics

# TEST GETS
rm -rf ADG${G}
rm -rf RRDG${G}
rm -rf HDG${G}
