import serial, sys

class dataDelegator:
	"""Passes valid incoming data from remote nodes to the registered handler"""
	nodeMap = {}
	handlers = {}
	
	def addHandler(self, handlername):
		# see http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
		mod = __import__(handlername + 'Handler', fromlist=[handlername + 'Handler'])
		klass = getattr(mod, handlername + 'Handler')
		self.handlers[handlername] = klass()
		print self.handlers
		
	def registerNode(self, nodeid, handlername):
		self.nodeMap[nodeid] = handlername
		print self.nodeMap
		
	def process(self, line):
		#print line
		line = line.split()
		# check if the string is valid.
		if len(line) > 0 and line[0] == 'OK':
			# if valid, strip off the node id,
			nodeid = int(line[1]);
			line = line[2:]
			for x in range(len(line)):
				line[x] = int(line[x])
			# and call the handler for this node id, passing the string.
			self.handlers[self.nodeMap[nodeid]].handle(nodeid, line)

ser = serial.Serial()
try:
	ser.port = '/dev/ttyUSB0'
	ser.baudrate = 57600
	ser.open()
	
	# instantiate the port data delegator
	dd = dataDelegator()
	
	# register the handlers
	dd.addHandler('weathernode')
	
	# register the nodes to the handlers
	dd.registerNode(3, 'weathernode')
	
	# main process loop
	while True:
		dd.process(ser.readline())
		
except KeyboardInterrupt:
    sys.stderr.write('\n--- exit ---\n')
	
#except SerialException as (errno, strerror):
#	print "problem opening serial port ({0}: {1})".format(errno, strerror)
	
finally:
	if ser.isOpen():
		ser.close()

