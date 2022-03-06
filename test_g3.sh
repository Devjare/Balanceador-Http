#!/bin/bash

rm *_3.metrics

# TEST PUT GROUP 3 Round Robin
for FILE in $(pwd)/G3_FILES/*; 
    do 
        python $(pwd)/cliente.py 1 3 PUT "RRCG3/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# TEST PUT GROUP 2 Random
for FILE in $(pwd)/G3_FILES/*; 
    do 
        python $(pwd)/cliente.py 0 3 PUT "ACG3/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done

# TEST PUT GROUP 2 Hash
for FILE in $(pwd)/G3_FILES/*; 
    do 
        python $(pwd)/cliente.py 2 3 PUT "HCG3/${FILE##*/}";
        # python $(pwd)/tpy.py "$FILE"; 
done
