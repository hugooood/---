#create-time:2017/4/20
#author:hugo
#emil:hugooood
#计算机网络-自顶向下方法 第六版
#套接字编程练习
#作业1：Web服务器

#import socket module
from socket import *
#Prepare a server socket

#Fill in start
serverIP = ''  	   #对应本机所有ip地址
serverPort = 12000 #TCP socket端口
serverAddress = (serverIP,serverPort)

serverSocket = socket(AF_INET,SOCK_STREAM) #创建TCP socket
serverSocket.bind(serverAddress) #绑定地址
serverSocket.listen(1) #开始监听

#Fill in end
while True:
	#Establish the connection
	print('Ready to serve...')

	try:
		#print('2333')
		connectionSocket,addr = serverSocket.accept()#获取连接socket
		message = connectionSocket.recv(1024) #获得http报文
		#print('message',message)
		filename = message.split()[1] #获得URI，去掉首部'/'就是文件名
		#print('filename',filename)

		f = open(filename[1:]) #打开文件
		#print('f:',f)
		outputdata = f.readlines()#逐行读出文件内容并存到list中
		#print('outputdata-type',type(outputdata))
		
		#Send one HTTP header line into socket	
		connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')#网络传输数据时是比特类型的

		#Send the content of the requested file to the client
		#发送请求文件的内容到客户端
		for i in range(0, len(outputdata)):
			connectionSocket.send(bytes(outputdata[i],encoding='utf-8')	)
		connectionSocket.close()

	except IOError:  #当文件不存在时，程序并不能报错。

		#Send response message for file not found
		connectionSocket.send(b'404 not found')
		#Close client socket
		connectionSocket.close()
serverSocket.close()