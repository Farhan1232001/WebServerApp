# WebServerApp
The purpose of this group project is to learn how to create a web server.

The purpose of this project is to learn about the server side of the web by implementing a simple, yet functional web server and using it to construct a simple shopping cart application. Along the way, we also want to learn about the HTTP protocol, CGI, server side includes, and other server-related topics. 

The following tutorial is followed (NOTE: For the class project, ONLY part 1 is required)
- Part I: https://www.classes.cs.uchicago.edu/archive/1999/winter/CS219/projects/project2/project2.html
- Part II: https://www.classes.cs.uchicago.edu/archive/1999/winter/CS219/projects/project2/project2b.html


How to connect to webserver from browser?
    Insert following URL in browser to connect to server
        http://127.0.0.1:1025/ShoppingCart.html

How to run the web server program?
    - In general,
        $ python3 webserver.py <relativePathToDocRoot> <portNumberr>
    
            - docRoot holds all html files for the website
            - portNumber must be >1024 for this project
            - 
    ex) $ python3 webserver.py docroot 1025     <--- Just copy this in the cmd line and server should work.


Important Things to note:
- The web server code is all in the main() function in the webserver.py
- The server does NOT fully work on Windows as the os.fork() is not supported on windows.