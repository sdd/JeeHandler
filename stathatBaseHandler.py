import sys
import time
from stathat import StatHat
from httplib import HTTPException

class stathatBaseHandler:
	"""Abstract JeeNode BaseHandler class that uploads data to stathat"""
	_stathat 		= None
	_email			= 'scott@donnel.ly'
	_retryInterval	= 5
	_maxRetries		= 12
	
	def __init__(self):
		#TODO: read DB settings from config file		
		try:
			self._stathat = StatHat();
			
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise

	def log(self, data):
		nodeid = data['nodeid']
		del(data['nodeid'])
		for k in data:
			for i in range(self._maxRetries):
				try:
					print self._stathat.ez_post_value(self._email, 'node' + str(nodeid) + '-' + k, data[k])				
					break;
				except HTTPException as e:
					print 'Http error ' + str( e ) + ', Retrying in ' + str( self._retryInterval ) + ', attempt number ' + str (i)
					if (i == self._maxRetries):
						raise e
					else:
						time.sleep(self._retryInterval)
		
