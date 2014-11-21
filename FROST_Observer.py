import socket

#note, might need to adjust IP address to work with wherever 
# the frost_monkey is running. Also, need to make sure that
# the ports match with the frost_monkey script

while 1:
	msgToSend = raw_input("Enter something to send to VM, 'q' to quit, 'h' for help: ")
	if msgToSend== 'h':
		print "\nuse standard mininet naming conventions (e.g. h1, s4)"
		print "to run pingall in mininet:"
		print "			PINGALL"
		print "for link events:"
		print "			LINK <interface 1> <interface 2> <'UP'/'DOWN'>"
		print "to FREEZE a switch:"
		print "			SWITCH <switch name> DOWN"
		print "To print out flow information from a switch:"
		print "			DUMP-FLOWS <switch name>"
		print "\n\n"
	else:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect( ('192.168.56.101', 50007) )
		s.send( msgToSend )
		s.close()
	if msgToSend== 'q':
		print "ending connection, you have also terminated server socket"
		break
