class Logger:
	__file = {}
	__log = []
	__results = []

	def __init__(self, path, writeMode = 'OVERWRITE'):
		mode = ""
		if writeMode == 'OVERWRITE':
			mode = 'w'
		else:
			raise ValueError('Invalid writeMode')

		try:
			self.__file = open(path, mode)
		except (IOError):
			raise

	def error(self, message, line = None, fileName = 'grapher.py'):
		self.__log.append(LogEntry('ERROR  ', line, fileName, message))

	def warning(self, message, line = None, fileName = 'grapher.py'):
		self.__log.append(LogEntry('WARNING', line, fileName, message))

	def info(self, message):
		self.__log.append(LogEntry('INFO   ', None, None, message))
	
	def result(self, entrant, task, inputNumber, result):
		self.__results.append(ResultEntry(entrant, task, inputNumber, result))

	def write(self):
		try:
			self.__file.write(''.join(map(str, self.__log)))
			self.__file.write(''.join(map(str, self.__results)))
		except Exception:
			raise
		
		# Clear log if write successful
		self.__log = []
		self.__results = []

	def close(self):
		self.__file.close()

class LogEntry:
	level = ""
	lineNumber = 0
	fileName = ""
	message = ""

	def __init__(self, level, lineNumber, fileName, message):
		self.level = level
		self.lineNumber = lineNumber
		self.fileName = fileName
		self.message = message

	def __repr__(self):
		return str("({}) {}:{} \"{}\"\n".format(self.level, self.fileName, self.lineNumber, self.message))

class ResultEntry:
	entrant = ""
	task = ""
	inputNumber = ""
	result = {}

	def __init__(self, entrant, task, inputNumber, result):
		self.entrant = entrant
		self.task = task
		self.inputNumber = inputNumber
		self.result = result

	def __repr__(self):
		outString = ""
		fR = ""

		# Get reasons for fail as needed
		if self.result.overPurchased:
			fR += "Over-purchased the following items: {}\n".format(self.result.overPurchasedItemsDict)
		if self.result.overCost:
			fR += "Cost too high: {}\n".format(self.result.totalCost)
		if self.result.overWeight:
			fR += "Weight too high: {}\n".format(self.result.totalWeight)
		if self.result.overVolume:
			fR += "Volume too high: {}\n".format(self.result.totalVolume)
		if self.result.badDist:
			fR += "Bad food group distribution: {]\n".format(self.result.fGDistribution)

		if len(fR) == 0:
			outString = "<{} PASSED task {} input {} with {} items and the following stats:\n{}>\n".format(self.entrant, self.task, self.inputNumber, self.result.totalItems, self.result)
		else:
			outString = "<{} FAILED task {} input {} because of the following reasons:\n{}>\n".format(self.entrant, self.task, self.inputNumber, fR)

		return outString
