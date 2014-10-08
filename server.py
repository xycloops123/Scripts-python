import socket
import sys

gauravDict = {}
def method_put(valLen,keyVal,userEntered) :
	gauravDict[str(keyVal)] = userEntered[:int(valLen)]
	
def method_get(valLen,keyVal) :
	if keyVal in gauravDict :
		if len(gauravDict[keyVal]) >= int(valLen) :
			return gauravDict[keyVal][:int(valLen)]+'\n000'
		else : 
			return '101'
	else :
		return '102'

def method_clear(keyVal) :
	if keyVal in gauravDict :
		del gauravDict[keyVal]
		return '000'
	else :
		return '102'



HOST = ''
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
	s.bind((HOST,PORT))
except socket.error, msg:
	print 'Bind Failed. Error Code : '+ str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

s.listen(10)
while True :
	conn, addr = s.accept()
	inputC = ''
	conn.send('000\n')
	while True :
		strRec = conn.recv(1024)
		if strRec.strip() == 'QUIT' :
			break
		else :
			inputRecieved = strRec.split(' ')
			if inputRecieved[0] == 'PUT' :
				if int(inputRecieved[1]) > 256:
					conn.send('101\n')
				else :
					conn.send('001\n')
				userEntered = ''
       		 		while True :
                			user_input = conn.recv(1024)
                			if '.' in user_input:
						if len(userEntered) > 0 :
                                                        userEntered = userEntered +' '+ user_input
                                                else :
                                                        userEntered = user_input
                        			break
  		              		else:
                	        		if len(userEntered) > 0 :
							userEntered = userEntered +' '+ user_input
                        			else :
                                			userEntered = user_input
				if len(userEntered) < int(inputRecieved[1]) :
        	        		conn.send('101\n')
				else :
					method_put(inputRecieved[1],inputRecieved[2],userEntered)
					conn.send('000\n')
			elif inputRecieved[0] == 'GET' :
				serverReturn = method_get(inputRecieved[1],inputRecieved[2])
				conn.send(serverReturn+'\n')
				#conn.send('000\n')
			elif inputRecieved[0] == 'CLEAR' :
				serverReturn = method_clear(inputRecieved[1])
				conn.send(serverReturn+'\n')
			else :				
				conn.send('100\n')

	conn.close()
s.close()
