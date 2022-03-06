for FILE in $(pwd)/G1_FILES/*; 
    do 
        python $(pwd)/cliente.py 1 1 PUT RRCG1/"$FILE"
        # python $(pwd)/tpy.py "$FILE"
    ; 
done
