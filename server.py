import socket
import pickle
import sys
import os
from os import listdir
from os.path import isfile, join

def get_file_data(file_path):
    info  = { "size": 0, "bytes": bytes(0) }
    f = open(file_path, "rb")
    file_size = os.path.getsize(file_path)
   
    info['size'] = file_size
    info['bytes'] = f.read()
    f.close()
   
    return info

if __name__ == "__main__":
    
    status = {
            "200": "OK",
            "404": "NOT FOUND"
            }

        
    port = int(sys.argv[1])
    
    HEADERSIZE = 1024
    MAX_ALLOWED_SIZE = 1000 * 1000 * 100 # 100MB
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(5)

    status_code = 200
    response_header = ""
    
    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
       
        msg = clientsocket.recv(MAX_ALLOWED_SIZE)
        
        header = str(msg).split("\\n\\n")[0]
        HEADERSIZE = len(bytes(header, 'utf-8')) - 1 # extra byte.

        ### Request info
        method =  "PUT" if "PUT" in header.split(" ")[0] else "GET"
        
        ### FILE INFO
        file_path = header.split(" ")[1].split("\\n")[0].split("/")
        file_dir = file_path[0] # File_dir is always specified.
        file_name = None if file_path[1] == '' else file_path[1]
        
        stored_size = "0"

        if(method == "PUT"): 
            file_size = header.split(":", 1)[1].split("\\n")[0].strip()
            stored_size = file_size
            
            ### FILE CONTENT
            content = msg[HEADERSIZE:]
       
            while(len(content) < int(file_size)):
                nmsg = clientsocket.recv(MAX_ALLOWED_SIZE)
                content += nmsg
 

            # Create file  
            ## Verify if dir doesn't exists already.
            if not os.path.exists(file_dir):
                npath = os.path.join(os.getcwd(), file_dir)
                os.makedirs(npath)

            # Write file contents
            f = open(f"{file_dir}/{file_name}", 'wb')
            f.write(content)
            print(f"Uploading file {file_dir}/{file_name} of size: {len(content)}")
            f.close()
         
            status_msg = status[str(status_code)]
            u_response_header = response_header + str(status_code) + f" {status_msg}\n\n"
            clientsocket.send(bytes(u_response_header, "utf-8"))
            clientsocket.close()

        else:
            file_name = file_name[0:len(file_name)-1]
            if(file_name == ""):
                file_name = None
                # Get list of files in dir.
                if os.path.exists(file_dir):
                    file_list = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
                    files = pickle.dumps(file_list)

                    status_msg = status[str(status_code)]
                    # u_response_header, u_ for unique, using response_header, overrited the value
                    # for all next requests.
                    u_response_header = response_header + str(status_code) + f" {status_msg}"
                    b_response_header = bytes(u_response_header, "utf-8")
                    clientsocket.send(b_response_header)

                    clientsocket.send(files)
                    # clientsocket.send(msg)
                    clientsocket.close()
                else:
                    status_code = 404
                    u_response_header = response_header + str(status_code) + f" {status_msg}"
                    b_response_header = bytes(u_response_header, "utf-8")
                    clientsocket.send(b_response_header)


            else:
                ''' GET file '''
                if os.path.exists(file_dir):
                    # Get the specified file.
                    file_data = get_file_data(f"{file_dir}/{file_name}")
                    
                    # prepare header
                    header = response_header
                    header = header + "Content-length: " + str(file_data['size']) + "\n"
                    header = header + "\n" # LINEA EN BLANCO
                    header = bytes(header, 'utf-8')
       
                    # Prepare file to send
                    msg = file_data['bytes']
                    msg = header + msg
                    
                    try:
                        print(f"Sending file: {file_dir}/{file_name}")
                        clientsocket.sendall(msg)
                    except socket.error as exc:
                        print("Exception: ", exc)


                else:
                    status_code = 404
                    status_msg = status[str(status_code)]
                    u_response_header = response_header + str(status_code) + f" {status_msg}"
                    b_response_header = bytes(u_response_header, "utf-8")
                    clientsocket.send(b_response_header)

      
        server_metrics_file = f"server_{port}.metrics"
        file_path = os.path.join(os.getcwd(), server_metrics_file)
        try:
            if(os.path.exists(file_path)):
                # Append to current file.
                with open(file_path, "a") as f:
                    f.write(stored_size + "\n")
            else:
                # Create file
                with open(file_path, "w") as f:
                    f.write(stored_size + "\n")
        except Exception as ex:
            print(ex)
