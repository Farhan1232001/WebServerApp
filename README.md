# WebServerApp
The purpose of this group project is to learn how to create a web server.

The purpose of this project is to learn about the server side of the web by implementing a simple, yet functional web server and using it to construct a simple shopping cart application. Along the way, we also want to learn about the HTTP protocol, CGI, server side includes, and other server-related topics. 

The following tutorial is followed (NOTE: For the class project, ONLY part 1 is required)
- https://www.classes.cs.uchicago.edu/archive/1999/winter/CS219/projects/project2/project2.html


How to run the web server program?
    1) Download 3rd party module
        - download imageio
            - On WINDOWS: $ pip install imageio
            - On MAC/linux: $ pip install imageio
    2) Run server via command line
        - In general,
            $ python3 webserver.py <relativePathToDocRoot> <portNumberr>
        
                - docRoot holds all html files for the website
                - portNumber must be >1024 for this project

        WINDOWS
        ex) $ python webserver.py docroot 1025     <--- Just copy this in the cmd line and server should work.

        MACOS/Linux
        ex) $ python3 webserver.py docroot 1025     <--- Just copy this in the cmd line and server should work.

    3) How to connect to webserver from browser?
        Insert following URL in browser to connect to server
            http://127.0.0.1:1025/ShoppingCart.html


Important Things to note:
- The web server code is all in the main() function in the webserver.py
- The server does NOT fully work on Windows as the os.fork() is not supported on windows.

What are the main parts of our project directory?
- cgi-bin directory stores the CGI scripts our webserver will use
- docroot directory contains the web pages and web objects our server will use
- webserver.py contains the code for the web server.