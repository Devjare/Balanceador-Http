import socket
import sys
import os

if __name__ == "__main__":
   
    port = int(sys.argv[1])
    
    HEADERSIZE = 1024
    MAX_ALLOWED_SIZE = 1000 * 1000 * 100 # 100MB
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(5)
    
    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        
        msg = clientsocket.recv(MAX_ALLOWED_SIZE)
        # print("Client FULL: message: ")
        # print("START =======================================================")
        # print(msg)
        # print(" END =======================================================")
        
        # print("msg header:",msg[:HEADERSIZE])
        # header = msg[:HEADERSIZE]
        header = str(msg).split("\\n\\n")[0]
        HEADERSIZE = len(bytes(header, 'utf-8')) - 1 # extra byte.
        print("HEADER RAW: ", header)
        print("HEADER RAW LEN: ", HEADERSIZE)
        # print("HEADER STRING: ", header)

        ### Request info
        method =  "PUT" if "PUT" in header.split(" ")[0] else "GET"
        print("METHOD: ", str(method))

        if(method == "PUT"): 
            file_size = header.split(":", 1)[1].split("\\n")[0].strip()
            print("File size: ", file_size)

        ### FILE INFO
        file_path = header.split(" ")[1].split("\\n")[0].split("/")
        print("File path: ", file_path)
        file_dir = file_path[0] # File_dir is always specified.
        file_name = None if file_path[1] == '' else file_path[1]
        
        print("File_dir: ", file_dir)
        print("File_name: ", file_name)
       
        ### FILE CONTENT
        content = msg[HEADERSIZE:]
        print("File content ====================================")
        print("Fullmsg len: ", len(msg))
        print(len(content))

        # Create file  
        ## Verify if dir doesn't exists already.
        if not os.path.exists(file_dir):
            npath = os.path.join(os.getcwd(), file_dir)
            os.makedirs(npath)

        # Write file contents
        f = open(f"{file_dir}/{file_name}", 'wb')
        f.write(content)
        f.close()
    

        clientsocket.send(bytes("Message recieved!", "utf-8"))
