import sys
import socket

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

    while True:
        # wait for a client DOWNLOAD request
        data, client_address = server_socket.recvfrom(1024)
        print(f"New client connected from {client_address}")
        downloal_message = data.decode('ascii')

    

if __name__ == "__main__":
   main()