import glob, os, re

class InputList:

	fileDict = {}

	def __init__(self, searchPath, fileGlob, numberRegex):
		try:
			os.chdir(searchPath)
			for f in glob.glob(fileGlob):
				match = re.search(numberRegex, f)
				if match:
					self.fileDict[match.group(1)] = '{}{}'.format(searchPath, f)
		except:
			raise
		finally:
			# This is getting me back to the root directory assuming successful navigation to searchPath
			if not os.path.exists(searchPath):
				os.chdir('../')

class OutputList:
	
	submissionList = []

	def __init__(self, searchPath, fileGlob, infoCaptureRegex):
		try:
			for f in os.listdir(searchPath):
				match = re.search(infoCaptureRegex, f)
				if match:
					self.submissionList.append(Submission(match.group(1), match.group(2), match.group(3), '{}{}'.format(searchPath, f)))
		except:
			raise
		finally:
			# This is getting me back to the root directory assuming successful navigation to searchPath
			if not os.path.exists(searchPath):
				os.chdir('../')


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
