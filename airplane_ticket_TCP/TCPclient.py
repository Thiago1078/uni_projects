#   TCPClient.py                                     
 
from socket import *

# STUDENTS - replace your server machine's name 
serverName = "192.168.56.1"

# STUDENTS - you should randomize your port number.         
# This port number in practice is often a "Well Known Number"  
serverPort = 12000



# create TCP socket on client to use for connecting to remote
# server.  Indicate the server's remote listening port
# Error in textbook?   socket(socket.AF_INET, socket.SOCK_STREAM)  Amer 4-2013 
clientSocket = socket(AF_INET, SOCK_STREAM)

# open the TCP connection
clientSocket.connect((serverName,serverPort))

hello_server = '.'
clientSocket.send(bytes(hello_server, "utf-8"))

while 1:
    response = input()
    # interactively get user's line to be converted to upper case
    # authors' use of raw_input changed to input for Python 3  Amer 4-2013

    # send the user's line over the TCP connection
    # No need to specify server name, port
    # sentence casted to bytes for Python 3  Amer 4-2013
    clientSocket.send(bytes(response, "utf-8"))

    #output to console what is sent to the server
    print ("Sent to Tickets Server: ", response)

    # get user's line back from server having been modified by the server
    got_back = clientSocket.recv(1024).decode("utf-8")

    # output the modified user's line 
    print ("Received from Tickets Server: ", got_back + "\n")


