import sys
import socket

def main():
    # Validate whether sufficient parameters are provided
    if len(sys.argv) != 2:
        print("You should enter: Python udpclient.py host_name port_number file_name")
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
    

if __name__ == "__main__":
   main()