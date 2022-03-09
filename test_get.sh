#!/bin/bash

function getServerMetrics {
    # Server metrics 9097
    python get_server_metrics.py 9097
    # Server metrics 9098
    python get_server_metrics.py 9098
    # Server metrics 9099
    python get_server_metrics.py 9099
}

echo "========================== GET TESTS ===================================="
for i in 1 2 3
do
    export G=$i

    # remove metrics existing.
    rm *d_$G.metrics
    # Remove existing loaded files
    rm -rf ADG${G}
    rm -rf RRDG${G}
    rm -rf HDG${G}

    for j in 0 1 2
    do
        export ALG=$j

        if [ $j -eq 0 ]; then
            export ALG_NAME=RANDOM
            export ALG_INITIALS=A
        fi
        if [ $j -eq 1 ]; then
            export ALG_NAME="Round Robin"
            export ALG_INITIALS=RR
        fi
        if [ $j -eq 2 ]; then
            export ALG_NAME="HASH"
            export ALG_INITIALS=H
        fi

        echo "Grupo $i Algoritmo $ALG:$ALG_NAME"

        for FILE in $(pwd)/G${G}_FILES/*; 
            do 
                # OBTAINS FILES FROM UPLOADS FOLDER FOR EACH ALG/GROUP.
                # AND SAVES IT TO THE FOLDER FOR DOWNLOADS FOR EACH ALG/GROUP
                # IE. RRDG1, ADG3, HDG2, ETC...
                python $(pwd)/cliente.py $ALG $G GET "${ALG_INITIALS}CG${G}/${FILE##*/}";
        done
        
        # Metrics for Random PUT Group 1
        python get_metrics.py $ALG GET $G
        echo "Server storage for $ALG_NAME GROUP ${G}"
        getServerMetrics
        rm server_*.metrics
    done
done

# KILL PYTHON SERVERS PROCESS.
# kill -9 $(ps -e | grep python | awk '{print $1}')                                   [±master ✓]

# Remove everything left
# rm -rf *C*
# rm *.metrics
