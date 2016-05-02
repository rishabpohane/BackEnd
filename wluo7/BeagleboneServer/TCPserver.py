#!/usr/bin/env python

import signal, os
import sys
import re
import socket
import thread

from RequestHandlers.GETHandler import *
from RequestHandlers.POSTHandler import *

TCP_IP = '192.168.1.200' # Change to 192.168.1.109 if on Beaglebone or its static ip
TCP_PORT = 5005
BUFFER_SIZE = 1024
SERVER_ON = True 

# Parses the incoming request to appropriate function
def process_request(request):
	match = re.search(r'(\S+)\s(\S+)', request)	
	if match:
		type = match.group(1);
		content = match.group(2)
		
		# Include corresponding functions for avaiable http requests
		switch = {
			'GET': get_data,
            'POST': post_data
		}
		try:
			print "Routing to proper request handler..."
			return switch.get(type)(content)
		except TypeError, NameError:
			return 'Invalid request type "'+type+'"'	
	else:
		return 'Invalid, can not parse request "'+request+'"'	

# Called when connection is recieved
def request_handler(conn, addr):
    while True:
    	print "Waiting for front-end request..."
        request = conn.recv(BUFFER_SIZE)
     	print "Request from front-end received: "+request
        result = process_request(request)
        try:
        	conn.send(result)
        	print "Reponse to front-end send..."
        except:
        	print "Connection loss... closing socket."
        	break
    conn.close()
    print "Disconnected client ", addr
					
if __name__ == '__main__':
# Initialize server socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(3)

# Wait for client connection
	try:
		while SERVER_ON:
			conn, addr = s.accept()
			print "Connected to client ", addr
    			thread.start_new_thread(request_handler, (conn, addr))
	# Close server socket if ctrl-c is recieved
	except KeyboardInterrupt:
		s.close()
		print "\rBeagleboneServer socket at "+TCP_IP+":"+str(TCP_PORT)+" closed."
