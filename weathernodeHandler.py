import stathatBaseHandler

class weathernodeHandler(stathatBaseHandler.stathatBaseHandler):
	def handle(self, nodeid, data):
		data = self._unserialize(nodeid, data)
		self.log(data)
		
	def _unserialize(self, nodeid, data):	
		# data payload format:
		# { int temp; int32_t pres; int humid; int temp2; int batt; int32_t lux; }
		payload = {}
		payload['nodeid']		= nodeid	
		payload['temperature1'] = round((data[0]  + (data[1]<<8)) * 0.1, 1)
		payload['pressure'] 	= round((data[2]  + (data[3]<<8) + (data[4]<<16) + (data[5]<<24)) * 0.01, 1)
		payload['humidity']		= (data[6]  + (data[7]<<8))
		payload['temperature2']	= (data[8]  + (data[9]<<8))
		payload['battery']		= round((data[10] + (data[11]<<8)) * 0.001, 3)
		payload['lux']			= (data[12] + (data[13]<<8) + (data[14]<<16) + (data[15]<<24))
		return payload

