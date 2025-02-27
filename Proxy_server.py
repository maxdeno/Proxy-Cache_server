import os 
from socket import *
import sys
from urllib.parse import urlparse

# create a cache directory
if not os.path.exists("cache"):
    os.mkdirs("cache")

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(("0.0.0.0", 8888))
tcpSerSock.listen(5)
print("Proxy server is running and listening on port 80")

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = tcpCliSock.recv(1024).decode("latin-1")
    print(f"Client Request: \n{message}")

    if not message:
        tcpCliSock.close()
        continue

    # parse the message to extract the HTTP request Header.
    message_line = message.split("\n")[0]
    print(f"Message line: {message_line}")

    # extract the filename from the request
    try:

        filename = message_line.split(" ")[1]

    except IndexError:
        print("Invalid request format")
        tcpCliSock.close()
        continue

    try:
        filename = urlparse(message_line.split()[1]) # parse the filename
        hostn = filename.netloc #Extract the filename
        path = filename.path if filename.path else "/"
        cache_filename = f"cache/{hostn.replace("-","_")}{path.replace("/","_")}"
    
    except IndexError:
        print("Invalid request form")
        tcpCliSock.close()
        continue

    # Check if the file is cached
    if os.path.exists(cache_filename):
        print(f"---> Cache hit: {cache_filename} <---")
        with open(cache_filename, "rb") as f:
            outputdata = f.read()

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.1 200 OK\r\ncontent-Type:text/html\r\n\r\n".encode())
            tcpCliSock.send(outputdata)
            print('Read from cache')

    # Error handling for file not found in cache
    else:
        print(f"----> Cache failed: fetching {cache_filename} from web <----")

    # Create a socket on the proxyserver
    try:
            c = socket(AF_INET, SOCK_STREAM)
            c.settimeout(5)
            # Connect to the socket to port 80
            c.connect((hostn, 80))

        # Create a temporary file on this socket and ask port 80 for the file in requested by the client
            request = f"GET /{filename} HTTP/1.1\r\nHost: {hostn}\r\nconnection: close\r\n\r\n"
            c.send(request.encode())
            # Read the response into buffer
            buffer = c.recv(4096)
            if not buffer:
                print(f"No response from {hostn}")
                tcpCliSock.close()
                continue

            with open(cache_filename, 'wb') as tmpFile:
                while buffer:
                    print(f"writing {len(buffer)} bytes to cahe: {filename}")
                    tmpFile.write(buffer)
                    tcpCliSock.send(buffer)
                    buffer = c.recv(4096)
            print(f"cached file {cache_filename} cached succesfully")
            
    except Exception as e:
            print("Illegal request", e)
    else:
            # HTTP response message for file not found
            
            tcpCliSock.send("HTTP1.1/ 404 Not Found\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
            tcpCliSock.send(
                "<html><body><h1>404 Not Found</h1></body></html>".encode())
        
        # Close the client and the server sockets
    tcpCliSock.close()
    if 'c' in locals():
     c.close()

