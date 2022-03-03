for filename in /RRCG1/*; do
    for ((i=0; i<=3; i++)); do
        echo filename
        # ./MyProgram.exe "$filename" "Logs/$(basename "$filename" .txt)_Log$i.txt"
    done
done

