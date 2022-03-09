# Running the programs.

To run, just execute run.sh, or run any of the scripts manually in the next order:
- gen_files.sh
- servers_run.sh
- test_put.sh
- test_get.sh


And in case of wanting to delete all the files that were created, just run:
- rm -rf *_FILES
- rm -rf *D*
- rm -rf *C*
- rm *.metrics

In order to stop the servers for listening, kill the process directly is needed.
- sudo kill -9 $(ps -e | grep python | awk '{print $1}')

# Notes on scripts.

### gen_files.sh

Just generates 100 files of each file size group, calls file_gen.py with 3 arguments:
- [1] File size group.
- [2] How many files to generate.
- [3] Folder to save those files(Ideally Keep it the way it is, otherwise will be necesary to change on test_put and test_get scripts)

### servers_run.sh

Run the 3 servers with 3 different ports running server.py with the port as argument.
If the port is changed here, then it will be necesary to change those ports on client.py
on the servers_ports array.

### test_put.sh and test_get.sh

These 2 scripts only call the 9 differnet configurations for client.py
One configuration for each file group, algorithm, and request method.
Additionaly, the output is saved to a results file(restuls_put.txt, and results_get.txt).


## get_metrics.py and get_server_metrics.py

These 2 python scripts, read the outputs for the server and client, which are written on some special
files created only for this purpose, for that reason, those files are deleted inmediatly, in order to allow new metrics each time tests are run.
