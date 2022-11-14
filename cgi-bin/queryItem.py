#!/usr/bin/python3
import cgi

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
if form.getvalue("name"):
    name = form.getvalue("item_name")
    print(f"<h1>Price of {name} is " +itemDictionary["eggs"])


# Using HTML input and forms method
print("<button onclick=\"history.back()\">Go Back</button>")
print("</body></html>")

#exit(0)
