class Logger:
	__file = {}
	__log = []

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

	def write(self):
		try:
			self.__file.write(''.join(map(str, self.__log)))
		except Exception:
			raise
		
		# Clear log if write successful
		self.__log = []

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
