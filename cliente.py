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

def get_save_dir(method,algorithm,group):
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
    # Files path => directory containing the test files for the specified group.
    files_path = f"G{group}_FILES"
    file_list = []
    for (dirpath, dirnames, filenames) in walk(files_path):
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
        selected = int(hashlib.sha1(filename.encode("utf-8")).hexdigest(), 16) % 3
        return servers_ports[selected]
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
    if(algorithm == RANDOM):    
        port = select_server(filename=None,method=RANDOM)
    elif(algorithm == RR):
        current_rr = None
        port = select_server(filename=None,method=RR)
        print("Port RR: ", port)
    
    file_to_upload = None 
    if(method == "PUT"):
        group = int(sys.argv[5])
        try:
            file_to_upload = sys.argv[4]
            if(algorithm == HASH):    
                port = select_server(filename=file_to_upload,method=HASH)
        except:
            print("A put request must indicate which file to upload as 4th parameter.")

    else:
        print("Destination: ", destination)
        group = int(sys.argv[4])
        if(algorithm == HASH):    
            port = select_server(filename=file_to_upload,method=HASH)
        

    HEADERSIZE = 1024 # 1 Kb header MAX.

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    # INICIAR ACTIVIDAD

    header = f"{method} {destination}"

    start = 0
    end = 0
    ellapsed = 0 # Time taken on the operation GET or PUT

    test_file_list = get_test_files(group)
    # print(test_file_list)
    if(method == "PUT"):
        # Esta parte es la que se repetiria 100 veces, por cada archivo, por cada tipo
        # de algoritmo, por cada grupo.
        # ================================= PUT REQUESTS =================================
        # ESTRUCTURA PUT
        # > $ python cliente.py n req destiny source group
        # donde:
        # n = algoritmo balanceo(0)Round robin(1), Hash(2))
        # req = request method(GET/PUT)
        # destiny = Destination or where to store the file on server.
        # source = File to upload, to be stored on destiny.
        # group = test files group(MIN(1), MED(2), BIG(3))
        # EJEMPLO PUT
        # > $ python cliente.py 1 PUT dirx/file2 RRCG1/FILE_220301230356071056 1
        # Subir archivo FILE_2203... a directorio dirx/file2 en servidor,
        # utilizando Round Robin(n=1) para seleccionar servidor, y subir los archivos
        # del grupo 1(MIN)
        # NOTA PARA DESARROLLADOR: El grupo no es necesario si se iterara a traves de un script de bash.

        print("PUT REQUEST")
        try:
            file_to_upload = sys.argv[4]
        except:
            print("A put request must indicate which file to upload as 4th parameter.")

        port = select_server(filename=destination,method=RANDOM, rr_current=None)
        print("File to uplaod: ", file_to_upload)
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
        start = datetime.now()
        s.send(msg)

        response = s.recv(HEADERSIZE)
        end = datetime.now()

        ellapsed = (end - start).total_seconds() * 1000
        print("Ellapsed = %f, type: %s" % (ellapsed, type(ellapsed)))

        # print("Time taken to upload file: ", ellapsed.total_seconds() * 1000)
        print("Server response: ", str(response))

    else:
        # ================================= GET REQUESTS =================================
        print("GET REQUEST")
        file_name = header.split(" ")[1].split("/")[1]
        print("Filename: ", file_name)
        header = bytes(header, "utf-8") # encode header
        print("Send header: ", header)
        s.send(header)

        response = s.recv(MAX_ALLOWED_SIZE) #
        print("Full response: ", response)
        if('404' in str(response)):
            print("File not found")
        elif('Content-length' in str(response)):
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

            print("Saving to: ", file_name)
            f = open(f"{file_name}", 'wb')
            f.write(content)
            f.close()

        else:
            response_body = pickle.loads(s.recv(MAX_ALLOWED_SIZE)) #
            print("Files: ") 
            for i in range(len(response_body)):
                print(f"{response_body[i]}")


    metrics_file = get_metrics_file(method, algorithm, group)
    print("metrics File to write: ", metrics_file)
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
