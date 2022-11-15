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
from multiprocessing import Process, Pipe
import string
from socket import *

def processPostRequest(connectionSocket):
    pass

# If a GET request with user input is received, a CGI program will run
def processGetRequest(pathToWebObj):
    pass


# If a GET request requests a program to run, create bidirectional pipes between
# the web server (this program) and the CGI program.
# The method will return a response
def processCgiRequest(requestMsgDecodedAndSplit):
    # here is some data
    REQUEST_METHOD = requestMsgDecodedAndSplit[0]
    SCRIPT_NAME = requestMsgDecodedAndSplit[1]
    DOCUMENT_ROOT = "docroot/"
    QUERY_STRING = ""
    data = "Hi there, this is a test of pipes"

    # Create a Two Pipes - one connecting webserver.py to cgi-bin/HelloWorld.py and vice versa
    (parentInput,childOutput) = os.pipe()    # Create a pipe from child to parent
    (childInput,parentOutput) = os.pipe()    # Create a pipe from parent to child

    # Run 'HelloWorld.py' on the data above
    pid = os.fork() # Create a child process. Method returns 0 in the child process and the pid in parent process
    if pid != 0:
        # I'm the parent
        os.close(childOutput)
        os.close(childInput)
        os.write(parentOutput, data.encode())
        os.close(parentOutput)
        response = os.read(parentInput, 1000)
        print(f"py: {response}")
        os.waitpid(pid, 0)  # wait for child to exit
        return response
    else:
        # I'm the child
        os.close(parentOutput)
        os.close(parentInput)
        os.dup2(childInput, 0)
        os.dup2(childOutput, 1)
        enviornmentVariables = {}
        enviornmentVariables["REQUEST_METHOD"] = REQUEST_METHOD
        enviornmentVariables["SCRIPT_NAME"] = SCRIPT_NAME
        enviornmentVariables["DOCUMENT_ROOT"] = DOCUMENT_ROOT
        enviornmentVariables["QUERY_STRING"] = QUERY_STRING
        os.execve("cgi-bin/"+SCRIPT_NAME.decode(), [SCRIPT_NAME.decode()], enviornmentVariables)     # run 'HelloWorld.py'

# This method is identical to the method above except that it uses threading instead of forking.
# Reason for having this is because Windows OS does not support forking.
# this method uses Pipe from multiprocessing module NOT OS module
#   https://superfastpython.com/multiprocessing-pipe-in-python/#What_is_a_Pipe
def processCgiRequest_usingThreading_parentProcess(requestMsgDecodedAndSplit):
    # here is some data
    print("ee: \n\n",requestMsgDecodedAndSplit)
    REQUEST_METHOD = requestMsgDecodedAndSplit[0]
    SCRIPT_NAME = requestMsgDecodedAndSplit[1]
    DOCUMENT_ROOT = "docroot/"
    QUERY_STRING = ""
    data = "Hi there, this is a test of pipes"

    # Create a Two Pipes - one connecting webserver.py to cgi-bin/HelloWorld.py and vice versa
    parentConnection, childConnection = Pipe()
    childProcess = Process(target=processCgiRequest_usingThreading_childProcess, args=(childConnection,parentConnection,REQUEST_METHOD,SCRIPT_NAME,DOCUMENT_ROOT,QUERY_STRING))
    childProcess.daemon = True # makes it so where childProcess ends immediately when parentProcess ends
    childProcess.start()
    response = parentConnection.recv()
    childProcess.join()
    childProcess.close()
    parentConnection.close()
    print(response)
    print("aklsfjakljfk")
    return response

def processCgiRequest_usingThreading_childProcess(childConnection,parentConnection,REQUEST_METHOD,SCRIPT_NAME,DOCUMENT_ROOT,QUERY_STRING):
        enviornmentVariables = {}
        enviornmentVariables["REQUEST_METHOD"] = REQUEST_METHOD
        enviornmentVariables["SCRIPT_NAME"] = SCRIPT_NAME
        enviornmentVariables["DOCUMENT_ROOT"] = DOCUMENT_ROOT
        enviornmentVariables["QUERY_STRING"] = QUERY_STRING
        os.execve("cgi-bin/"+SCRIPT_NAME.decode(), [SCRIPT_NAME], enviornmentVariables)
        #childConnection.send(response)
        #
        # enviornmentVariables = {}
        # enviornmentVariables["REQUEST_METHOD"] = REQUEST_METHOD
        # enviornmentVariables["SCRIPT_NAME"] = SCRIPT_NAME
        # enviornmentVariables["DOCUMENT_ROOT"] = DOCUMENT_ROOT
        # enviornmentVariables["QUERY_STRING"] = QUERY_STRING
        # os.execve("cgi-bin/"+SCRIPT_NAME.decode(), [SCRIPT_NAME], enviornmentVariables)     # run 'HelloWorld.py' 

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

        isCgiRequest = False
        isWebObjectRequest = False

        # Get msg retrieved
        try:
            requestMsg = connectionSocket.recv(1024)
                    # recv(): receives data from socket (at most 1024 bytes at a time)
            requestMsgDecodedAndSplit = requestMsg.split()
                    # note: String.split() converts a string into a list of strings (delimiter being ' ')
                    #       Bytes.split() converts a byte string into a list of byte strings
            method = requestMsgDecodedAndSplit[0].decode()
            #print("\requestMsgDecodedAndSplit: ", requestMsgDecodedAndSplit)
                    # recall 1st info inside HTTP request msg is the method
            url = requestMsgDecodedAndSplit[1].decode()
                    # recall 2nd info inside HTTP request msg is the url for the WebPage object or to a script
                    #       webpage object ==> url to .html files, images, etc
                    #       url can also contain user input

            # Creating print statments to log diagnostic information
            print("\n**************************************************************")
            print("Diagnostic messages:\n\tHTTP request type: "+method) # Print the type of HTTP request
            print("\tRequested document: "+url) # Prints the requested document name
            address = requestMsgDecodedAndSplit[4].decode() # creates a new variable that holds the address of the incoming connection.
            print("\tAddress of the incoming connection: "+address) # prints the address of the incoming connectoin.
            print("**************************************************************\n")

            if method == "GET":
                #print(f"\tdocroot: {docroot} \n\turlToWebObj: {urlToWebObj}\n\tfullPathToWebObj: {fullPathToWebObj}")
                #print("requestMsgDecodedAndSplit: ",requestMsgDecodedAndSplit)
                #print("urlToWebObj[:7]: ",urlToWebObj[:7])

                # Is request for a web object or CGI access (What is MIME type? Does url imply webObject or py script?)
                if url[-3:] == ".py":    
                    isCgiRequest = True
                else:
                    isWebObjectRequest = True

                # If url wants web object, then try 
                # opening the file, sending the content type, and senting the file
                if isWebObjectRequest:
                    print("url (WebObjectRequest): ", url)
                    f = open("docroot"+url)
                    connectionSocket.send("HTTP/1.0 200 OK\n".encode())
                    # Figure out the content type
                    if (url[-5:] == ".html"):
                        connectionSocket.send("Content-type: text/html\n".encode())
                    elif (url[-4:] == ".gif"):
                        connectionSocket.send("Content-type: image/gif\n".encode())
                    elif (url[-4:] == ".jpg"):
                        connectionSocket.send("Content-type: image/jpg\n".encode())
                    elif (url[-5:] == ".jpeg"):
                        connectionSocket.send("Content-type: image/jpeg\n".encode())
                    else:
                        connectionSocket.send("Content-length: text/plain\n".encode())

                    # Read the opend file & send its contents
                    data = f.read()
                    connectionSocket.send(f"Content-length: {len(data)}\n".encode())
                    connectionSocket.send("\n".encode())
                    connectionSocket.send(data.encode())
                    f.close()
                    connectionSocket.close()
                elif isCgiRequest:
                    print("url (cgiRequest): ", url)
                    connectionSocket.send("HTTP/1.0 200 OK\n".encode())
                    # Figure out the content type
                    #print(requestMsgDecodedAndSplit)

                    # Response holds info for next webPage, as well as user input info
                    #   response = processCgiRequest(requestMsgDecodedAndSplit)
                    print("adsadsf")
                    response = processCgiRequest(requestMsgDecodedAndSplit)
                    print("Before")
                    print("response:\n",response)
                    connectionSocket.send(response)
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