echo "####################### GENERATING FILES"
./gen_files.sh

echo "####################### STARTING SERVERS"
./servers_run.sh

# Run and write results to files.
./test_put.sh > results_put.txt
./test_get.sh > results_get.txt


# Delete unnecesary files after execution.
rm -rf *_FILES
rm -rf *D*
rm -rf *C*

rm *.metrics

# Stop servers
kill -9 $(ps -e | grep python | awk '{print $1}')
