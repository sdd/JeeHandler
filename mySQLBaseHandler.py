import sys
import _mysql as mdb

class mySQLBaseHandler:
	"""Abstract JeeNode BaseHandler class that implements MySQL connection"""
	_con = None
	_dbHost = 'localhost'
	_dbUser = 'JeeHandler'
	_dbPass = 'JeeHandler'
	_dbDB	= 'JeeHandler'
	dbTable	= 'weathernodes'
	
	def __init__(self):
		#TODO: read DB settings from config file
		
		try:
			pass
			self._con = mdb.connect(
				self._dbHost,
				self._dbUser,
				self._dbPass,
				self._dbDB)
			
		except mdb.Error, e:
		    print "Error %d: %s" % (e.args[0],e.args[1])
		    sys.exit(1)

	def log(self, data):
		#curs = self._con.cursor()
		query = self.buildQuery(data)
		print query
		self._con.query(query)
		
	def buildQuery(self, data):
		query = """INSERT INTO `{0}` ({1}) VALUES ({2})""".format(
			self.dbTable,
			','.join(map(str, data.keys())),
			','.join(map(str, data.values())))
		return query
		
		
