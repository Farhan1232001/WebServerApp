# Simple Python web-server
#   How to connect to webserver from browser?
#       Insert following URL in browser to connect to server
#           http://127.0.0.1:1025/ShoppingCart.html
#
#   How to run program?
#       In general,
#           $ python3 webserver.py <relativePathToDocRoot> <portNumberr>
#       
#           docRoot holds all html files for the website
#           portNumber must be >1024 for this project
#       ex) $ python3 webserver.py docroot 1025
#       

import sys
import os
import string
from socket import *

def processPostRequest(connectionSocket):
    pass

# If a GET request with user input is received, a CGI program will run
def processGetRequest(pathToWebObj):
    pass
# If a GET request requests a program to run
def processCgiRequest(pathToCgiProgram):
    # here is some data
    data = "Hi there, this is a test of pipes"

    # Create a Two Pipes - one connecting webserver.py to cgi-bin/HelloWorld.py and vice versa
    (parentInput,childOutput) = os.pipe()    # Create a pipe from child to parent
    (childInput,parentOutput) = os.pipe()    # Create a pipe from parent to child

    # Run 'wc' on the data above
    pid = os.fork()
    if pid != 0:
        # I'm the parent
        os.close(childOutput)
        os.close(childInput)
        os.write(parentOutput, data)
        os.close(parentOutput)
        response = os.read(parentInput, 1000)
        print(f"py: {response}")
        os.waitpid(pid, 0)  # wait for child to exit
    else:
        # I'm the child
        os.close(parentOutput)
        os.close(parentInput)
        os.dup2(childInput, 0)
        os.dup2(childOutput, 1)
        e = {}                  # Enviornment variables
        e["FOO"] = "BAR"
        os.execve("/usr/bin/wc", ["wc"], e)     # run 'wc'

def main():
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
            print("\requestMsgDecodedAndSplit: ", requestMsgDecodedAndSplit)
                    # recall 1st info inside HTTP request msg is the method
            urlToWebObj = requestMsgDecodedAndSplit[1]
                    # recall 2nd info inside HTTP request msg is the url for the WebPage object
                    #       webpage object ==> url to .html files, images, etc
                    #       url can also contain user input

            if method.decode() == "GET":
                # Form the full filename path (full path is relative to WebServerApp directory)
                fullPathToWebObj = docroot + urlToWebObj.decode()
                print(f"\tdocroot: {docroot} \n\turlToWebObj: {urlToWebObj}\n\tfullPathToWebObj: {fullPathToWebObj}")

                # Try opening the file
                f = open(fullPathToWebObj)
                connectionSocket.send("HTTP/1.0 200 OK\n".encode())

                # Figure out the content type
                if (fullPathToWebObj[-5:] == ".html"):
                    connectionSocket.send("Content-type: text/html\n".encode())
                elif (fullPathToWebObj[-4:] == ".gif"):
                    connectionSocket.send("Content-type: image/gif\n".encode())
                elif (fullPathToWebObj[-4:] == ".jpg"):
                    connectionSocket.send("Content-type: image/jpg\n".encode())
                elif (fullPathToWebObj[-5:] == ".jpeg"):
                    connectionSocket.send("Content-type: image/jpeg\n".encode())
                elif (urlToWebObj[0:3] == "/url"): # IF Get request contains user input
                    pass
                elif (urlToWebObj[:7] == "/cgi-bin"): # IF Get request cgi request
                    processCgiRequest(urlToWebObj)
                else:
                    connectionSocket.send("Content-length: text/plain\n".encode())

                # Read the file & send it
                data = f.read()
                connectionSocket.send(f"Content-length: {len(data)}\n".encode())
                connectionSocket.send("\n".encode())
                connectionSocket.send(data.encode())
                f.close()
                connectionSocket.close()
            elif method == "POST":
                pass
            else: 
                # If an unsupported format is request 
                # (say if .gif was sent & this webServer doesn't support it) then send 501 error
                connectionSocket.send("HTTP/1.0 501 Not Implemented\n".encode())
                connectionSocket.send("Content-type: text/html\n\n".encode())
                connectionSocket.send("<h1> Unimplemented request type </h1>".encode())
                connectionSocket.close()
        except IOError:
            # HTTP 404 is a std response code indicating the browser was able to communicate with server
            # but was not able to find what was requested
            print("404 NOT found")
            # Send response message for file not found
            connectionSocket.send("HTTP/1.0 404 Not Found\n".encode())
            connectionSocket.send("Content-type: text/html\n\n".encode())
            connectionSocket.send("<h1> File Not Found </h1>".encode())
            connectionSocket.close()

    serverSocket.close()

if __name__ == "__main__":
    main()