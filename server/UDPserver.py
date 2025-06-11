import sys

def main():
    # Validate whether sufficient parameters are provided
    if len(sys.argv) != 2:
        print("You should enter: Python udpclient.py host_name port_number file_name")
        sys.exit(1)
    
    # Process the command line arguments
    port_number = sys.argv[1]

if __name__ == "__main__":
   main()