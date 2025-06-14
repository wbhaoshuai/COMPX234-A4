# COMPX234-A4
## summary
This project implements a file transfer system based on UDP protocol, including a server and a client.  
The server can simultaneously process file download requests from multiple clients, and the client can download specified files from the server.  
## The main functions of the server-side program are as follows:
- Listen for download requests from clients.
- Verify that the requested file name exists.
- If file exists, assign a new port to client and create a new thread to handle file transfer.
- Handle the file data request and close request of the client.
## The main functions of the client program are as follows:
- Read the list of file names to download from the specified file.
- Send a download request to the server.
- Download each part of the file according to the response of the server.
- When the download is complete, send a close request.
## How to run this program：
### Server side：
1. Open the terminal and enter the directory where the code is located.
2. Run the following command to start the server:
    python UDPserver.py <port_number>
- Where<port_number>is the port number that the server listens on.  
  
For this project, for example, you can enter:  
    python UDPserver.py 54321
  
### Client side：
1. Prepare a text file, each line containing a file name to download.
2. Open the terminal and enter the directory where the code is located.
3. Run the following command to start the client:
    python UDPclient.py <host_name> <port_number> <file_name>
- <host_name>is the host name or IP address of the server.
- <port_number>is the port number that the server listens on.
- <file_name>is a text file containing a list of file names to download.
  
For this project, for example, you can enter:  
    python UDPclient.py localhost 54321 request.txt 
  
## Matters needing attention：
- The server and client need to communicate in the same network or through appropriate network configuration.
- The file name list file each line contains only one file name.
- The server will randomly assign ports within the range of 50000-51000 to the client for file transmission.
- If the program runs with errors, or the download file is incomplete, please try running the client multiple times or restarting the program.
