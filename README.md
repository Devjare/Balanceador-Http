# LOAD BALANCER SIMULATION.

### Running the code.

In order to run the tests, firs the servers must be enabled.
To do so, run the script "server_run.sh". If server ports are changed
in the file, then those ports should also change on the array named
"server_ports" on client.py directly to match.

Once the servers are running, run "test.sh" to run all tests for all 
combinations of file groups, balancing algorithms, and request methods,
and get the metrics results on one run.

If is desired to run each test separatedly, theres one file for each
file group "test_g1.sh", "test_g2.sh" and "test_g3.sh", there's also 
a script to get the metrics only "metrics.py".
