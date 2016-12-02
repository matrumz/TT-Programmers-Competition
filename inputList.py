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
		except Exception:
			raise
