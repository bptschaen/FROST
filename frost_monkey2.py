#!/usr/bin/python


""" Creates a full mesh mininet topology
  allows for links to go down/come up
  
  connects to remote controller

"""

import socket


from time import sleep
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI

from optparse import OptionParser

parser = OptionParser(usage='usage: %prog -c x.x.x.x')
parser.add_option("-c", "--controller", dest="controllerIP", 
	help="specify the IP of your Controller for Mininet",
	metavar="CONTR_IP")
parser.add_option("-p", "--port", dest="port", help="specify the port of Mininet Controller",
	default=6633)
(options, args) = parser.parse_args()

if not options.controllerIP:
	parser.error('\n* Controller IP must be specified. In the VM try sudo route -n or ifconfig to find the IP.\n' + 
		'* Try sudo dhclient eth1 to set an IP if none have been set yet. \n' + 
		'* You want the non-zero IP under Gateway.\n' +
	 	'* Other configurations require running ifconfig on the Host OS ' +
	 	'and finding inet addr for vboxnet0' + '\n' + 
	 	'================================\n' +
	 	'* Also, this script must run before starting the Controller in Eclipse on Host OS\n' +
	 	'* And you have to wait for it to timeout trying to reach the remote Controller, \n' +
	 	'at which point it will build the Mininet topology and then ask you to start the Controller')


net = Mininet()
#will be used for controller
#c1 = net.addController('c1', ip='192.168.56.1')
c1 = net.addController(name='c1', controller=RemoteController, 
	ip=options.controllerIP, port=options.port)

def createFullMesh( numSw=4 ):
	hosts = [ net.addHost( 'h%d'%i )
				for i in range(1, numSw+1) ]
	switches = [ net.addSwitch( 's%d'%i )
				for i in range(1, numSw+1) ]
	for i in range(0, numSw):
		print "connecting host and switch ", i
		net.addLink( hosts[i], switches[i] )
	for i in range(0, numSw):
		for j in range(0, i):
			if(i!=j):
				print "connecting switch ", i+1, " with switch ", j+1
				net.addLink( switches[i], switches[j] )
	net.build()
	c1.start()
	for i in range(0, numSw):
		switches[i].start( [c1] )
	return net

"""takes sw1 -> sw2 down
sw1 and sw2 are the switch names, must be lowercase
e.g. s1, s2, s3,..."""
def linkDownEvent( sw1, sw2 ):
	net.configLinkStatus( sw1, sw2, 'down')

"""takes sw1 -> sw2 down
sw1 and sw2 are the switch names, must be lowercase
e.g. s1, s2, s3,..."""
def linkUpEvent( sw1, sw2 ):
	net.configLinkStatus( sw1, sw2, 'up')

"""stops the switch input"""
def switchDownEvent( sw ):
	swtch = net.getNodeByName(sw)
	print 'removing ', swtch, " from the network"
	swtch.stop()

def switchUpEvent( sw ):
	swtch = net.getNodeByName(sw)
	print 'not correctly implemented.'
	#print 'adding connection to ', swtch
	#swtch.start( [c1] )

def parseObserverInput( observerInput ):
	parts = observerInput.upper().split(' ')
	if len(parts)<1:
		return
	if parts[0] == "PINGALL":
		net.pingAll()
	elif parts[0] == "LINK":
		if len(parts) == 4:
			if parts[3] == "UP":
				linkUpEvent( parts[1].lower(), parts[2].lower() )
			elif parts[3] == "DOWN":
				linkDownEvent( parts[1].lower(), parts[2].lower() )
	elif parts[0] == "SWITCH":
		if len(parts) >= 3 and parts[2]=="DOWN":
			switchDownEvent( parts[1].lower() )
		if len(parts) >= 3 and parts[2]=="UP":
			switchUpEvent( parts[1].lower() )

def startListeningLoop():
	HOST = ''
	PORT = 50007
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind( (HOST, PORT) )
	s.listen(1)
	while 1:
		conn, addr = s.accept()
		print 'Connected by ', addr
		data = conn.recv(1024)
		if not data: break
		if data == "q2":
			print "terminating connection"
			break
		else:
			print data
			parseObserverInput( data )
	conn.close()

if __name__=="__main__":
	createFullMesh()
	print 'You may now start the remote SDN controller'
	print 'Then start up FROST Observer'
	startListeningLoop()
	print '\nExiting Mininet\n'
	net.stop()


