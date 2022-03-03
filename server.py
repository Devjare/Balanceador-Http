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
    # print(f.read()) 
   
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
        print(f"Connection from {address} has been established on server port: {port}")
        
        msg = clientsocket.recv(MAX_ALLOWED_SIZE)
        
        header = str(msg).split("\\n\\n")[0]
        HEADERSIZE = len(bytes(header, 'utf-8')) - 1 # extra byte.
        print("HEADER RAW: ", header)
        print("HEADER RAW LEN: ", HEADERSIZE)

        ### Request info
        method =  "PUT" if "PUT" in header.split(" ")[0] else "GET"
        print("METHOD: ", str(method))
        
        ### FILE INFO
        file_path = header.split(" ")[1].split("\\n")[0].split("/")
        print("File path: ", file_path)
        file_dir = file_path[0] # File_dir is always specified.
        file_name = None if file_path[1] == '' else file_path[1]
        
        print("File_dir: ", file_dir)
        print("File_name: ", file_name)

        if(method == "PUT"): 
            file_size = header.split(":", 1)[1].split("\\n")[0].strip()
            print("File size: ", file_size)
 
            ### FILE CONTENT
            content = msg[HEADERSIZE:]
            print("File content ====================================")
            print("Fullmsg len: ", len(msg))
            print(len(content))

            # Create file  
            ## Verify if dir doesn't exists already.
            if not os.path.exists(file_dir):
                print(f"Path: {file_dir} doesn't exists, creating...")
                npath = os.path.join(os.getcwd(), file_dir)
                os.makedirs(npath)

            # Write file contents
            f = open(f"{file_dir}/{file_name}", 'wb')
            f.write(content)
            f.close()
         
            status_msg = status[str(status_code)]
            u_response_header = response_header + str(status_code) + f" {status_msg}\n\n"
            print("server response: ",u_response_header)
            clientsocket.send(bytes(u_response_header, "utf-8"))
            clientsocket.close()

        else:
            file_name = file_name[0:len(file_name)-1]
            if(file_name == ""):
                file_name = None
                # Get list of files in dir.
                if os.path.exists(file_dir):
                    file_list = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
                    print(f"Files on dir '{file_dir}: ", file_list)
                    files = pickle.dumps(file_list)

                    status_msg = status[str(status_code)]
                    # u_response_header, u_ for unique, using response_header, overrited the value
                    # for all next requests.
                    u_response_header = response_header + str(status_code) + f" {status_msg}"
                    print("server response: ",u_response_header)
                    b_response_header = bytes(u_response_header, "utf-8")
                    print("response header on bytes: ", b_response_header)
                    clientsocket.send(b_response_header)
                    # print("Response message full: ", msg)

                    clientsocket.send(files)
                    # clientsocket.send(msg)
                    clientsocket.close()
                else:
                    status_code = 404
                    u_response_header = response_header + str(status_code) + f" {status_msg}"
                    b_response_header = bytes(u_response_header, "utf-8")
                    clientsocket.send(b_response_header)

                    print(f"{file_dir} doesn't exists.")

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
                    # msg = pickle.dumps(file_data['bytes'])
                    msg = file_data['bytes']
                    msg = header + msg
                        
                    clientsocket.send(msg)

                    print(f"GET {file_dir}/{file_name}")

                else:
                    status_code = 404
                    status_msg = status[str(status_code)]
                    u_response_header = response_header + str(status_code) + f" {status_msg}"
                    b_response_header = bytes(u_response_header, "utf-8")
                    clientsocket.send(b_response_header)

                    print(f"{file_dir} doesn't exists.")
