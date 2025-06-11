import sys

# Validate whether sufficient parameters are provided
if len(sys.argv) < 4:
    print("You should enter: Python udpclient.py host_name port_number file_name")
    sys.exit(1)

# Process the command line arguments
host_name = sys.argv[1]
port_number = sys.argv[2]
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
