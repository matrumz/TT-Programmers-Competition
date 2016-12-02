import glob, os, re

class InputList:

	fileDict = {}

	def __init__(self, searchPath, numberRegex):
		try:
			for f in os.listdir(searchPath):
				match = re.search(numberRegex, f)
				if match:
					self.fileDict[match.group(1)] = '{}{}'.format(searchPath, f)
		except:
			raise

class OutputList:
	
	submissionList = []

	def __init__(self, searchPath, infoCaptureRegex):
		try:
			for f in os.listdir(searchPath):
				match = re.search(infoCaptureRegex, f)
				if match:
					self.submissionList.append(Submission(match.group(1), match.group(2), match.group(3), '{}{}'.format(searchPath, f)))
		except:
			raise

class Submission:
	name = ""
	task = 0
	inputNumber = 0
	path = ""

	def __init__(self, name, task, inputNumber, path):
		self.name = name
		try:
			self.task = int(task)
			self.inputNumber = int(inputNumber)
		except:
			raise
		self.path = path

	def __repr__(self):
		return '{},{},{},{}'.format(self.name, self.task, self.inputNumber, self.path)
