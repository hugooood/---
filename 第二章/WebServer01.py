#import socket module
from socket import socket, AF_INET, SOCK_STREAM
import os.path
import time

def openTcpSocket(port):
	serverSocket= socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('',port))
	serverSocket.listen(1)
	print "Listening on port %s\nInterrupt with CTRL-C" % port
	return serverSocket

def main():
    serverSocket = openTcpSocket(12003)
    while True:
        try:
	    #Establish the connection
            print 'Ready to serve...'
            connectionSocket, addr = serverSocket.accept()
            message = connectionSocket.recv(4096)
            print message
            filename = message.split()[1].partition("/")[2]
            sendFile(connectionSocket, filename, "text/plain")
            connectionSocket.close()
        except IOError:
            print "Not found %s" % filename
            sendError(connectionSocket, '404', 'Not Found')
            connectionSocket.close()
        except KeyboardInterrupt:
            print "\nInterrupted by CTRL-C"
            break
    serverSocket.close()

def sendFile (socket, fileName, mime):
	f = open(fileName)
	outputdata = f.read()
	socket.send("HTTP/1.1 200 OK\r\n")
	socket.send("Content-Type:%s\r\n" % mime)
	socket.send("Content-Length:%d\r\n" % len(outputdata))
	socket.send("\r\n")
	socket.send(outputdata)

def sendError(socket, code, msg):
	f = open(""+code+".html")
	outputdata = f.read()
	socket.send("HTTP/1.1 %s %s\r\n" % (code, msg))
	socket.send("Content-Type:text/html\r\n")
	socket.send("Content-Length:%d\r\n" % len(outputdata))
	socket.send("\r\n")
	socket.send(outputdata)
	
main()