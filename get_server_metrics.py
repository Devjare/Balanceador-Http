import sys
import os

def get_used_storage(arr):
    storage = 0
    total_data = len(arr) - 1 # omit the last \n added.
    for i in range(total_data):
        n = int(arr[i])
        storage += n
    
    # In bytes
    return storage

if __name__ == "__main__":
    port = sys.argv[1]

    filename = f"server_{port}.metrics"
    filepath = os.path.join(os.getcwd(), filename)
    try:
        with open(filepath, "r") as metrics_file:
            data = metrics_file.read().split("\n")
            storage = get_used_storage(data)
            storage_on_kb = storage / 1000
            source = f"Server {port}, used storage: {storage} Bytes, {storage_on_kb} Kilobytes"
            print(source)
    except Exception as e:
        print(f"Theres no metrics file: {filepath}, run tests first.")
