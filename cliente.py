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
        selected = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % 3
        return server_ports[selected]
    else:
        return rnd.choice(servers_ports) 

if __name__ == "__main__":
    MAX_ALLOWED_SIZE = 1000 * 1000 * 100 # 100MB
    algorithm = int(sys.argv[1]) # Balancer selection method(RR, Hash, Random)
    port = 9099 # DEFAULT PORT

    method = sys.argv[2]
    destination = None # Including filename

    if(len(sys.argv) < 4):
        print("Any request must include a source/destiny objective as 3rd parameter(i.e. PUT/GET source/destiny)")
    else:
        destination = sys.argv[3]
  
    # group = sys.argv[4]
    file_to_upload = None 
    if(method == "PUT"):
        try:
            file_to_upload = sys.argv[4]
        except:
            print("A put request must indicate which file to upload as 4th parameter.")
    
        if(algorithm == RANDOM):    
            port = select_server(filename=None,method=RANDOM, rr_current=None)
        elif(algorithm == RR):
            current_rr = None
            port = select_server(filename=None,method=RR)
            print("Port RR: ", port)
            # port = server_ports[current_rr]
        else:
            port = select_server(filename=file_to_upload,method=HASH, rr_current=None)


    
    HEADERSIZE = 1024 # 1 Kb header MAX.
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    header = f"{method} {destination}"
    
    if(method == "PUT"):
        # EJEMPLO PUT:
        # > $ python cliente.py 9099 PUT dirx/file2 RRCG1/FILE_220301230356071056

        print("PUT REQUEST")
        try:
            file_to_upload = sys.argv[4]
        except:
            print("A put request must indicate which file to upload as 4th parameter.")
      
        port = select_server(filename=destination,method=RANDOM, rr_current=None)
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
        print("Server response: ", str(response))

    else:
        print("GET REQUEST")
        file_name = header.split(" ")[1].split("/")[1]
        print("Filename: ", file_name)
        header = bytes(header, "utf-8") # encode header
        print("Send header: ", header)
        s.send(header)

        response = s.recv(MAX_ALLOWED_SIZE) #
        print("Full response: ", response)
        if('Content-length' in str(response)):
            print("Gotten a file!, downloading...")

            header = str(response).split("\\n\\n")[0]
            HEADERSIZE = len(bytes(header, 'utf-8')) # extra byte.
            print("HEADER RAW: ", header)
            print("HEADER RAW LEN: ", HEADERSIZE)

            file_size = header.split(":", 1)[1].split("\\n")[0].strip()
            print("File size: ", file_size)
            
            content = response[HEADERSIZE:]
            print("File content ====================================")
            print("Fullmsg len: ", len(response))
            print(len(content))

            f = open(f"RRDG1/{file_name}", 'wb')
            f.write(content)
            f.close()
         
        else:
            response_body = pickle.loads(s.recv(MAX_ALLOWED_SIZE)) #
            print("Files: ") 
            for i in range(len(response_body)):
                print(f"{response_body[i]}")

    s.close()
