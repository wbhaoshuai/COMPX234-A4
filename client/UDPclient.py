import sys
import socket
import base64

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
        file_name = request_file[i]
        # prepare DOWNLOAD message to request the first file on the list
        DOWNLOAD_reaquest = "DOWNLOAD " + file_name
        download_receive = sendAndResponse(client_socket,host_name,port_number,DOWNLOAD_reaquest)
        print(f"Received: {download_receive}")
        file_size = 0
        data_port = 0
        # split the parts of the request
        if(download_receive!=None):
            parts = download_receive.strip().split()
            # Check the value of the response
            if(parts[0] == "ERR"):
                print(download_receive)
                continue
            elif(parts[0] == "OK"):
                file_size = parts[3]
                # print(file_size)
                data_port = parts[5]
     
        try:
            # Open file for writing
            with open(file_name, 'wb') as file:
                total_received = 0
                block_size = 1000  # 1000 bytes per block
                
                # Enter a cycle through which the file will be downloaded until it is completed
                while total_received < int(file_size):
                    start = total_received
                    end = min(start + block_size - 1, int(file_size) - 1)
                    
                    # Build request
                    request = f"FILE {file_name} GET START {start} END {end}"
                    response = sendAndResponse(client_socket, host_name, int(data_port), request)
                    if(response!=None):
                        parts = response.strip().split()
                        fileData = base64.b64decode(parts[8])
                        file.seek(start)
                        file.write(fileData)

                    # print(response)
                    total_received += end - start + 1
                    progress = int((total_received / int(file_size)) * 50)
                    print(f"\r[{progress*'*'}{(50-progress)*'.'}] {total_received}/{file_size} bytes", end="")
                request = f"FILE {file_name} CLOSE"
                response = sendAndResponse(client_socket, host_name, int(data_port), request)
                if(response):
                    print("OK,close")            
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()
        

# sent_responses = set() 
        

def sendAndResponse(c_socket, ip, port, packet):
    counter = 0
    # Timeout with the initial value
    current_timeout = 1000
    while(counter < 5):
        try:
            c_socket.settimeout(current_timeout/1000)
            c_socket.sendto(packet.encode('ascii'), (ip, port))

            data, _ = c_socket.recvfrom(4096)
            response = data.decode('ascii')
            # if response not in sent_responses:
            #     sent_responses.add(response)
            #     return response
            return response
                   
        except socket.timeout:
            counter += 1
            current_timeout *= 2
            print(f"Error:The {counter}-th sending timeout. Retransmit the message.")
            
            # If the maximum number of retries is reached, exit the loop
            if counter >=5:
                print("the maximum number of retries has been reached, give up the attempt")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            break



if __name__ == "__main__":
   main()
