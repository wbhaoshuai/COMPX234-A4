import sys
import socket
import os
import random
import threading
import base64

def main():
    # Validate whether sufficient parameters are provided
    if len(sys.argv) != 2:
        print("You should enter: Python UDPclient.py port_number")
        sys.exit(1)
    
    # Process the command line arguments
    port_number = int(sys.argv[1])

    host = 'Bin'
    port = port_number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Reuse address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind to the port
    server_socket.bind((host, port))

    print("Server is running and ready to accept multiple clients...")

    # Port number available from the server
    number_pool = list(range(50000, 51001))
    random.shuffle(number_pool)

    while True:
        # wait for a client DOWNLOAD request
        data, client_address = server_socket.recvfrom(1024)
        print(f"New client connected from {client_address}")
        downloal_message = data.decode('ascii')
        
        parts = downloal_message.strip().split()
        # Validate the message
        if(len(parts) == 2 and parts[0] == "DOWNLOAD"):
            file_name = parts[1]
            # Check if the filename exists
            if os.path.exists(file_name):
               # Get file size
               file_size = os.path.getsize(file_name)
               # Get a port number randomly
               client_port = number_pool.pop()
               response = "OK "+file_name+" SIZA "+str(file_size)+" PORT "+str(client_port)
               server_socket.sendto(response.encode('ascii'), client_address)
               threading.Thread(target=handleFileTransmission, args=(host, client_port)).start()
            else:
                response = "ERR " + file_name +" NOT_FOUND"
                server_socket.sendto(response.encode('ascii'), client_address)
        else:
            continue
        
def handleFileTransmission(host, client_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind((host, client_port))
    while True:
        data, client_address = client_socket.recvfrom(4096)
        message = data.decode('ascii')
        parts = message.strip().split()
        # print("request" + message)

        if(parts[2] =="CLOSE"):
            file_name = parts[1]
            response = f"FILE {file_name} CLOSE_OK"
            client_socket.sendto(response.encode('ascii'), client_address)
            client_socket.close()
            break

        if(parts[2] == "GET"):
            file_name = parts[1]
            start = int(parts[4])
            end = int(parts[6])
            try:
                with open(file_name, 'rb') as file:
                    # Read the contents of the corresponding section in the file
                    file.seek(start)
                    file_data = file.read(end - start + 1)
                    
                    base64_data = base64.b64encode(file_data).decode()
                    response = f"FILE {file_name} OK START {start} END {end} DATA {base64_data}"
                    client_socket.sendto(response.encode('ascii'), client_address)
            except Exception as e:
                print(f"文件传输错误: {e}")




if __name__ == "__main__":
   main()