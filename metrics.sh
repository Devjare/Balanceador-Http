function getServerMetrics {
    # Server metrics 9097
    python get_server_metrics.py 9097
    # Server metrics 9098
    python get_server_metrics.py 9098
    # Server metrics 9099
    python get_server_metrics.py 9099
}

# Remove server_metrics file, to get separatedly how much storage was used per aglrotihm

# Metrics for Random PUT Group 1
python get_metrics.py 0 PUT 1
echo "Server storage for RANDOM GROUP 1"
getServerMetrics
rm server_*.metrics
# Metrics for Round Robin PUT Group 1
python get_metrics.py 1 PUT 1
echo "Server storage for ROUND ROBIN GROUP 1"
getServerMetrics
rm server_*.metrics
# Metrics for Hash PUT Group 1
python get_metrics.py 2 PUT 1
echo "Server storage for HASH GROUP 1"
getServerMetrics
rm server_*.metrics

# Metrics for Random PUT Group 2
python get_metrics.py 0 PUT 2
echo "Server storage for RANDOM GROUP 2"
getServerMetrics
rm server_*.metrics
# Metrics for Round Robin PUT Group 2
python get_metrics.py 1 PUT 2
echo "Server storage for ROUND ROBIN GROUP 2"
getServerMetrics
rm server_*.metrics
# Metrics for Hash PUT Group 2
python get_metrics.py 2 PUT 2
echo "Server storage for HASH GROUP 2"
getServerMetrics
rm server_*.metrics

# Metrics for Random PUT Group 3
python get_metrics.py 0 PUT 3
echo "Server storage for RANDOM GROUP 3"
getServerMetrics
rm server_*.metrics
# Metrics for Round Robin PUT Group 3
python get_metrics.py 1 PUT 3
echo "Server storage for ROUND ROBIN GROUP 3"
getServerMetrics
rm server_*.metrics
# Metrics for Hash PUT Group 3
python get_metrics.py 2 PUT 3
echo "Server storage for HASH GROUP 3"
getServerMetrics
rm server_*.metrics
