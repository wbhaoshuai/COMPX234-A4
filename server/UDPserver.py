import sys
import socket
import os
import random

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
            # Check if the filename exists
            if os.path.exists(parts[1]):
               # Get file size
               file_size = os.path.getsize(parts[1])
               # Get a port number randomly
               client_port = number_pool.pop()
               response = "OK "+parts[1]+" SIZA "+str(file_size)+" PORT "+str(client_port)
               server_socket.sendto(response.encode('ascii'), client_address)
            else:
                response = "ERR " + parts[1] +" NOT_FOUND"
                server_socket.sendto(response.encode('ascii'), client_address)
        else:
            continue


if __name__ == "__main__":
   main()