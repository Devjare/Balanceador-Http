#!/bin/bash

rm *_2.metrics

# TEST PUT GROUP 2 Round Robin
for FILE in $(pwd)/G2_FILES/*; 
    do 
        python $(pwd)/cliente.py 1 2 PUT "RRCG2/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# TEST PUT GROUP 2 Random
for FILE in $(pwd)/G2_FILES/*; 
    do 
        python $(pwd)/cliente.py 0 2 PUT "ACG2/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# TEST PUT GROUP 2 Hash
for FILE in $(pwd)/G2_FILES/*; 
    do 
        python $(pwd)/cliente.py 2 2 PUT "HCG2/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done
