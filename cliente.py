import socket
from numpy import random as rnd
import hashlib
import sys
import pickle
import os

RANDOM = 0
RR = 1 #Round Robin
HASH = 2 # HASH

servers_ports = [ 9097, 9098, 9099 ]

def get_file_data(file_path):
    info  = { "size": 0, "bytes": bytes(0) }
    f = open(file_path, "rb")
    file_size = os.path.getsize(file_path)
    # print(f.read()) 
   
    info['size'] = file_size
    info['bytes'] = f.read()
    f.close()
   
    return info

def select_server(filename=None,method=RANDOM, rr_current=None):
    if(method == RR):
        if(rr_current == HASH):
            rr_current = RANDOM 
        return server_ports[rr_current+1]
    elif(method == HASH):
        selected = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % 3
        return server_ports[selected]
    else:
        return rnd.choice(servers_ports) 

if __name__ == "__main__":
    port = int(sys.argv[1])

    method = sys.argv[2]
    destination = None # Including filename

    if(len(sys.argv) < 4):
        print("Any request must include a source/destiny objective as 3rd parameter(i.e. PUT/GET source/destiny)")
    else:
        destination = sys.argv[3]
    
    file_to_upload = None 
    
    HEADERSIZE = 1024 # 1 Kb header MAX.
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    header = f"{method} {destination}"
    
    if(method == "PUT"):
        print("PUT REQUEST")
        try:
            file_to_upload = sys.argv[4]
        except:
            print("A put request must indicate which file to upload as 4th parameter.")
      
        file_data = get_file_data(file_to_upload)
        # print("File data: ", file_data)
        
        # prepare header
        header = header + "\n"
        header = header + "Content-length: " + str(file_data['size']) + "\n"
        header = header + "\n" # LINEA EN BLANCO
        header = bytes(header, 'utf-8')
       
        # Prepare file to send
        # msg = pickle.dumps(file_data['bytes'])
        msg = file_data['bytes']
        msg = header + msg
        
        # process request 
        s.send(msg)

        response = s.recv(HEADERSIZE)
        print("Server response: ", response)

    else:
        print("GET REQUEST")
        header = bytes(header, "utf-8") # encode header

    s.close()
