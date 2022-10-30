# Simple Python web-server
#   How to connect to webserver from browser?
#       Insert following URL in browser to connect to server
#           http://127.0.0.1:1025/HelloWorld.html
#
#   How to run program?
#       In general,
#           $ python3 webserver.py <relativePathToDocRoot> <portNumberr>
#       
#           docRoot holds all html files for the website
#           portNumber must be >1024 for this project
#       

import sys
import string
from socket import *

# check the command line arguments for validity.
if len(sys.argv) != 3:
    print("usage : webserver docroot port")
    sys.exit(0)

# Set the document root and port
docroot = sys.argv[1]
# Why 127.0.0.1?
#       Localhost is the default name of the computer you are working on.
#       The term is a pseudo name for 127.0. 0.1, the IP address of the local computer. 
#       This IP address allows the machine to connect to and communicate with itself.
#       
#       IF you want server to respond to requests from local machine:
#           use:        serverSocket.bind((localHost, port))  wh/ localhost == 127.0.0.1
#       else:
#           use:        serverSocket.bind(("", port))
localHost = "127.0.0.1"
port = int( sys.argv[2] )

# Open up a socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((localHost, port))
    # Tell socket to begin listening 
    #   and tell it the max # of queued connections
serverSocket.listen(5)       
print(f"Web-server listening on port {port} ")

while True:
    # Establish the connection
    print("\nReady to serve...")
    # Blocks until somebody comes knocking, socket created on return
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection from {addr} ")

    # Get msg retrieved
    try:
        requestMsg = connectionSocket.recv(1024)
                # recv(): receives data from socket (at most 1024 bytes at a time)
        requestMsgDecodedAndSplit = requestMsg.split()
                # note: String.split() converts a string into a list of strings (delimiter being ' ')
                #       Bytes.split() converts a byte string into a list of byte strings
        method = requestMsgDecodedAndSplit[0]
                # recall 1st info inside HTTP request msg is the method
        document = requestMsgDecodedAndSplit[1]
                # recall 2st info inside HTTP request msg is the url for the WebPage object
                #       webpage object ==> url to .html files, images, etc

        if method.decode() == "GET":
            # Form the full filename path
            file = docroot + document.decode()
            print(f"\tdocroot: {docroot} \n\tdocument: {document}\n\tfile: {file}")

            # Try opening the file
            f = open(file)
            connectionSocket.send("HTTP/1.0 200 OK\n".encode())

            # Figure out the connect type
            if (file[-5:] == ".html"):
                connectionSocket.send("Content-type: text/html\n".encode())
            elif (file[-4:] == ".gif"):
                connectionSocket.send("Content-type: image/gif\n".encode())
            elif (file[-4:] == ".jpg"):
                connectionSocket.send("Content-type: image/gif\n".encode())
            else:
                connectionSocket.send("Content-length: text/plain\n".encode())
            
            # Read the file & send it
            data = f.read()
            connectionSocket.send(f"Content-length: {len(data)}\n".encode())
            connectionSocket.send("\n".encode())
            connectionSocket.send(data.encode())
            f.close()
            connectionSocket.close()
            # HTTP 404 is a std response code indicating the browser was able to communicate with server
            # but was not able to find what was requested
            connectionSocket.send("HTTP/1.0 404 Not Found\n".encode())
            connectionSocket.send("Content-type: text/html\n\n".encode())
            connectionSocket.send("<h1> File Not Found </h1>".encode())
            connectionSocket.close()
        else:
            connectionSocket.send("HTTP/1.0 501 Not Implemented\n".encode())
            connectionSocket.send("Content-type: text/html\n\n".encode())
            connectionSocket.send("<h1> Unimplemented request type </h1>".encode())
            connectionSocket.close()
    except IOError:
        print("404 NOT found")
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Close client socket
        connectionSocket.close()

serverSocket.close()
