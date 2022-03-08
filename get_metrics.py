import sys
import os

def get_median(arr):
    median = 0.0
    total_data = len(arr)
    for i in range(total_data):
        n = float(arr[i])
        median += n

    median = median / total_data
    return median

if __name__ == "__main__":
    algorithm = int(sys.argv[1])
    method =  sys.argv[2]
    group = int(sys.argv[3])

    algorithm_prefix = ""
    if(algorithm == 0):
        algorithm_prefix = "a"
    if(algorithm == 1):
        algorithm_prefix = "rr"
    if(algorithm == 2):
        algorithm_prefix = "h"
    
    method_prefix = ""
    method_prefix = "c" if method == "PUT" else "d"

    group_prefix = str(group)

    metrics_file = f"{algorithm_prefix}_{method_prefix}_{group_prefix}.metrics"

    try:
        with open(os.path.join(os.getcwd(), metrics_file), "r") as metrics_file:
            data = metrics_file.read().split("\n")
            median = get_median(data)
            source = f"{algorithm_prefix.upper()}{method_prefix.upper()}G{group_prefix}"
            print(f"Median time for {source} = {median}s")
    except:
        print(f"Theres no metrics file: {metrics_file}, run tests first.")
