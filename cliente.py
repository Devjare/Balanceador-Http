import socket
from numpy import random as rnd
import hashlib
import sys
import pickle
import os
from os import walk
from datetime import datetime

RANDOM = 0
RR = 1 #Round Robin
HASH = 2 # HASH

servers_ports = [ 9097, 9098, 9099 ]

def get_save_dir(algorithm,group):
    P1 = P2 = P3 = ""
    if(algorithm == RANDOM): 
        P1 = "A"
    if(algorithm == RR):
        P1 = "RR"
    if(algorithm == HASH):
        P1 = "H"
    P2 = "D" # Client will always download, only server needs to create new folder for Uploads("C")
    P3 = f"G{group}"

    return f"{P1}{P2}{P3}"

def get_test_files(group):
    files_path = f"G{group}_FILES"
    file_list = []
    for (dirpath, dirnames, filenames) in walk(files_path):
        for i in range(len(filenames)):
            filenames[i] = f"{dirpath}/{filenames[i]}"
        
        file_list.extend(filenames)
        break

    return file_list

def get_metrics_file(method, algorithm, group):
    filename = ""
    if(algorithm == RANDOM):
        filename = filename + "a"
    if(algorithm == RR):
        filename = filename + "rr"
    if(algorithm == HASH):
        filename = filename + "h"

    activity = "c" if method == "PUT" else "d"
    filename = filename + f"_{activity}_{group}.metrics"
    return filename

def get_file_data(file_path):
    info  = { "size": 0, "bytes": bytes(0) }
    f = open(file_path, "rb")
    file_size = os.path.getsize(file_path)

    info['size'] = file_size
    info['bytes'] = f.read()
    f.close()

    return info

def select_server(filename=None,method=RANDOM, rr_current=None):
    if(method == RR):
        current_rr = None
        with open("rr_next", "r") as f:
            current = str(f.read())
            current_rr = int(current)
        with open("rr_next", "w") as f:
            nxt_srvr = current_rr + 1 if current_rr < 2 else 0
            f.write(str(nxt_srvr))
        return servers_ports[current_rr]
    # return server_ports[rr_current+1]
    elif(method == HASH):
        selected = int(hashlib.sha1(filename.encode("utf-8")).hexdigest(), 16) % 3
        return servers_ports[selected]
    else:
        return rnd.choice(servers_ports) 

if __name__ == "__main__":
    MAX_ALLOWED_SIZE = 1000 * 1000 * 100 # 100MB
    algorithm = int(sys.argv[1]) # Balancer selection method(RR, Hash, Random)
    group = int(sys.argv[2])
    method = sys.argv[3]
    destination = sys.argv[4]
    port = 9099 # DEFAULT PORT

    # Si el algoritmos es random o round robin, no importa si el metodo es PUT o GET
    if(algorithm == RANDOM):    
        port = select_server(filename=None,method=RANDOM)
    elif(algorithm == RR):
        current_rr = None
        port = select_server(filename=None,method=RR)
   
    
    test_file_list = get_test_files(group)
    for fname in test_file_list:
        fname_rawname = fname.split("/")[1]
        destination_rawname = destination.split("/")[1]
        if(fname_rawname != destination_rawname):
            continue
        if(algorithm == HASH):
            port = select_server(filename=fname,method=HASH)
        
        file_to_upload = fname 

        HEADERSIZE = 1024 # 1 Kb header MAX.

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), port))

        # INICIAR ACTIVIDAD

        header = f"{method} {destination}"

        start = 0
        end = 0
        ellapsed = 0 # Time taken on the operation GET or PUT

        if(method == "PUT"):
        
           file_data = get_file_data(file_to_upload)
        
           # prepare header
           header = header + "\n"
           header = header + "Content-length: " + str(file_data['size']) + "\n"
           header = header + "\n" # LINEA EN BLANCO
           header = bytes(header, 'utf-8')
        
           msg = file_data['bytes']
           msg = header + msg
        
           # process request 
           start = datetime.now()
           s.sendall(msg)
           # s.send(msg)
            
            # Process response
           response = s.recv(HEADERSIZE)
           end = datetime.now()
        
           ellapsed = (end - start).total_seconds() * 1000
        
        else:
           # ================================= GET REQUESTS =================================
           file_name = header.split(" ")[1].split("/")[1]
           header = bytes(header, "utf-8") # encode header
           start = datetime.now()
           s.send(header)
        
            
           response = s.recv(MAX_ALLOWED_SIZE) #
           if('404' in str(response)):
               print(f"File: {file_name} not found")
           elif('Content-length' in str(response)):
        
               header = str(response).split("\\n\\n")[0]
               HEADERSIZE = len(bytes(header, 'utf-8')) # extra byte.
        
               file_size = header.split(":", 1)[1].split("\\n")[0].strip()
        
               content = response[HEADERSIZE:]
               while(len(content) < int(file_size)):
                   nmsg = s.recv(MAX_ALLOWED_SIZE)
                   content += nmsg
               
               end = datetime.now()
               ellapsed = (end - start).total_seconds() * 1000
        
               download_folder = get_save_dir(algorithm, group)
               file_path = f"{download_folder}/{file_name}"
               if not os.path.exists(download_folder):
                   npath = os.path.join(os.getcwd(), download_folder)
                   os.makedirs(npath)

               f = open(f"{file_path}", 'wb')
               f.write(content)
               f.close()
        
           else:
               # Retrieving list of files.
               response_body = pickle.loads(s.recv(MAX_ALLOWED_SIZE)) #
               print("Files: ") 
               for i in range(len(response_body)):
                   print(f"{response_body[i]}")
        

        metrics_file = get_metrics_file(method, algorithm, group)
        # Write to file:
        file_path = os.path.join(os.getcwd(), metrics_file)
        if(os.path.exists(file_path)):
            # Append to current file.
            with open(file_path, "a") as f:
                f.write(str(f"\n{ellapsed}"))
        else:
            # Create file
            with open(file_path, "w") as f:
                f.write(str(ellapsed))


        s.close()
