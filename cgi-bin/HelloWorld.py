#!/usr/bin/python3
import cgitb
cgitb.enable()


print("Content-type:text/html\r\n\r\n")
print("<html><body")
print("<h1 It Works! <\h1>")
for i in range(5):
    print("<h2> Hello World! "+ str(i)+"<\h2>")
print("<\body><\html>")