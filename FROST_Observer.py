import socket
from optparse import OptionParser

#note, might need to adjust IP address to work with wherever 
# the frost_monkey is running. Also, need to make sure that
# the ports match with the frost_monkey script

parser = OptionParser(usage='usage: %prog -m x.x.x.x')
parser.add_option("-m", "--mininet", dest="mininetIP", 
	help="specify the IP (from the view of Host OS) of your Virtual Machine running Mininet",
	metavar="MN_IP")
(options, args) = parser.parse_args()

if not options.mininetIP:
	parser.error('\n* Must specify IP address (from the view of Host OS) of Virtual Machine running Mininet')

while 1:
	msgToSend = raw_input("You are in a Mininet command line. \nEnter a command or 'h' for help and special commands\n")
	if msgToSend== 'h':
		print "Entering 'h' brings up this help screen. Entering 'q' quits FROST_Observer.py and kills Mininet."
		print "Entering 'q1' quits out of FROST_Observer.py but leaves Mininet running"
		print "Entering 'q2' quits out of FROST_Observer.py *and* kills Mininet"
		print "Other commands operate as standard Mininet commands." 
		print "\nUse standard mininet naming conventions (e.g. h1, s4)"
		print "to run pingall in mininet:"
		print "			PINGALL"
		print "for link events:"
		print "			LINK <interface 1> <interface 2> <'UP'/'DOWN'>"
		print "to FREEZE a switch:"
		print "			SWITCH <switch name> DOWN"
		print "To print out flow information from a switch:"
		print "			DUMP-FLOWS <switch name>"
		print "\n\n"
	elif msgToSend== 'q1':
		print "Quitting FROST_Observer.py, Mininet should continue to run"
		break
	else:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect( (options.mininetIP, 50007) )
		# port hardwired to 50007 in frost_monkey2.py as well
		s.send( msgToSend )
		s.close()
		if msgToSend == 'q2':
			print "Quitting FROST_Observer.py and Mininet."
			break

	