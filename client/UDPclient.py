import sys

# Validate whether sufficient parameters are provided
if len(sys.argv) < 4:
    print("You should enter: Python udpclient.py host_name port_number file_name")
    sys.exit(1)

# Process the command line arguments
host_name = sys.argv[1]
port_number = sys.argv[2]
file_name = sys.argv[3]
