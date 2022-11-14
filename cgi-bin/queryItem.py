#!/usr/bin/python3
import cgi, cgitb
cgitb.enable()
import sys

REQUEST_METHOD = sys.argv[0]
SCRIPT_NAME = sys.argv[1]
DOCUMENT_ROOT = sys.argv[2]
QUERY_STRING = sys.argv[3]

print(REQUEST_METHOD,SCRIPT_NAME,DOCUMENT_ROOT,QUERY_STRING)

print("Content-type: text/html\n")
print("")
print("<html><body>")
print("<h1> Hello Program! </h1>")

itemDictionary = {
    "eggs": "$5.00",
    "milk": "$5.50",
    "bread": "$5.49"
}

form = cgi.FieldStorage()
item_name = form.getvalue("item_name")
if form.getvalue("item_name"):
    print(f"<h1>Price of {item_name} is " +itemDictionary[item_name])
else:
    print(f"{item_name} is not in inventory.")


# Using HTML input and forms method
print("<button onclick=\"history.back()\">Go Back</button>")
print("</body></html>")

exit(0)
