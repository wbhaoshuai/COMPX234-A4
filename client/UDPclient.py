import sys
import socket

def main():
    # Validate whether sufficient parameters are provided
    if len(sys.argv) != 4:
        print("You should enter: Python UDPclient.py host_name port_number file_name")
        sys.exit(1)

    # Process the command line arguments
    host_name = sys.argv[1]
    port_number = int(sys.argv[2])
    file_name = sys.argv[3]

    # Save the name of the file to download
    request_file = []

    try:
        # Open the file for reading
        with open(file_name, 'r', encoding='utf-8') as file:
            line = file.readline()
            while line:
                line = line.strip()
                # containing the list of files to download
                request_file.append(line)
                line = file.readline()       
    except FileNotFoundError:
        print("File not found, please check the file path.")   

    # Create a UDP socket object and link it to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(len(request_file)):
        # prepare DOWNLOAD message to request the first file on the list
        DOWNLOAD_reaquest = "DOWNLOAD " + request_file[i]
        download_receive = sendAndResponse(client_socket,host_name,port_number,DOWNLOAD_reaquest)
        print(download_receive)

def sendAndResponse(c_socket, ip, port, packet):
    c_socket.connect((ip, port))
    counter = 0
    # Timeout with the initial value
    current_timeout = 1000
    while(counter < 5):
        try:
            c_socket.settimeout(current_timeout/1000)
            c_socket.sendall(packet.encode('ascii'))

            response = c_socket.recv(1024)
            return response.decode('ascii')
            
        except socket.timeout:
            counter += 1
            current_timeout *= 2 
            
            # If the maximum number of retries is reached, exit the loop
            if counter >=5:
                print("the maximum number of retries has been reached, give up the attempt")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
   main()
