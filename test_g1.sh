#!/bin/bash

rm *_1.metrics

# TEST PUT GROUP 1 Round Robin
for FILE in $(pwd)/G1_FILES/*; 
    do 
        python $(pwd)/cliente.py 1 1 PUT "RRCG1/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# TEST PUT GROUP 1 Random
for FILE in $(pwd)/G1_FILES/*; 
    do 
        python $(pwd)/cliente.py 0 1 PUT "ACG1/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# TEST PUT GROUP 1 Hash
for FILE in $(pwd)/G1_FILES/*; 
    do 
        python $(pwd)/cliente.py 2 1 PUT "HCG1/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done
