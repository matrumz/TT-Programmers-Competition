#!/usr/bin/python3

from inputParams import InputParams
from logger import Logger
from inventoryItem import InventoryItem
from purchaseItem import PurchaseItem
from fileLists import InputList, OutputList
#from results import Result, SubmissionResult
import sys, re

class Grader():
	syslogPath = './log.txt'

	inputSearchPath  = './inputs/'
	outputSearchPath = './outputs/'

	inputFileRegex = '^input-([0-9]+)\\.txt'
	outputFileRegex = "^(.+)-([0-9]+)-([0-9]+)\\.txt"
	inputParamRegex = "^\d+,(\d+),(\d+),(\d+);?$"

	inputParam = {}
	inventoryList = []

	syslog = {}

	def __init__(self):
		#Grader.moduleTest()
		self.main()
		try:
			self.syslog.write()
			self.syslog.close()
		except Exception as e:
			print('could not write or close system log: {}'.format(e))

	def main(self):

		# Get input file list
		try:
			inputDict = InputList(self.inputSearchPath, self.inputFileRegex).fileDict
		except Exception as e:
			print("Load list of input files failed: {}".format(e))
			return

		# Get output file list
		try:
			submissionList = OutputList(self.outputSearchPath, self.outputFileRegex).submissionList
		except Exception as e:
			print("Load list of output files failed: {}".format(e))
			return

		# Start the System Logger
		try:
			self.syslog = Logger(self.syslogPath)
		except Exception as e:
			print('Could not open System Logger: {}'.format(e))
			return
			
		# Process
		for inputNumberKey, inputFilePath in inputDict.items(): # foreach found input file
			try:
				self.loadInputFile(inputFilePath)
			except Exception as e:
				self.syslog.error("Error loading INPUT FILE {}: {}".format(inputFilePath, e))
				continue #skip to next input file
			
			for submission in submissionList: # foreach submission file...
				if str(submission.inputNumber) != str(inputNumberKey): # where applies to current input file
					continue
				try:
					submissionContents = self.loadOutputFile(submission.path)
				except Exception as e:
					self.syslog.error("Error loading OUTPUT FILE {}: {}".format(submission.path, e))
				#try:
				#	result = self.validateOutputFile(submissionContents)
	
	def loadOutputFile(self,path):
		pass

	def loadInputFile(self,path):
		inventoryLine = ""
		lineNumber = 0

		# Clear previous info
		self.inputParam = {}
		self.inventoryList = []

		# Open input & get params
		try:
			f = open(path, 'r')
			paramLine = f.readline()
			paramMatch = re.search(self.inputParamRegex, paramLine)
			if paramMatch:
				self.inputParam = InputParams(paramMatch.group(1), paramMatch.group(2), paramMatch.group(3))
			else:
				raise ValueError('Could not match parameter line')
		except Exception as e:
			raise ValueError('Could not get inputfile parameters: {}'.format(e))

		# Load inventory
		while(True): # This makes me sad, but I can't do assignments within conditionals, and I don't know how many lines there are
			inventoryLine = f.readline()
			if (inventoryLine == ""):
				break
			lineNumber += 1;
			inventoryLineItems = inventoryLine.split(',')
			if len(inventoryLineItems) != 6:
				self.syslog.warning('Incorrectly formatted inventory line: {}'.format(inventoryLine), lineNumber, path)
				continue
			try:
				self.inventoryList.append(InventoryItem(inventoryLineItems[0], inventoryLineItems[1], inventoryLineItems[2], inventoryLineItems[3], inventoryLineItems[4], inventoryLineItems[5].replace(';','').replace('\n','')))
			except Exception as e:
				self.syslog.warning('Invalid inventory item: {}'.format(e), lineNumber, path)
				continue

		f.close()
				
	
	# Used for script testing purposes only
	@staticmethod
	def moduleTest():
		logPath = './log.txt'
		inputSearchPath  = './inputs/'
		outputSearchPath = './outputs/'
		inputNumberExtractorRegex = '^input-([0-9]+)\\.txt'
		outputInfoExtractorRegex = "^(.+)-([0-9]+)-([0-9]+)\\.txt"
		
		# Open and test logger
		try:
			logger = Logger(logPath, 'OVERWRITE')
		except ValueError:
			print('Logger open value error')
			sys.exit()
		except IOError:
			print("Logger open io error")
			sys.exit()
		#logger.warning(param.moneyLimit, 11)
		#logger.error(param.weightLimit, 12, 'grader.py')
	
		# Test inputparams
		try:
			param = InputParams('$5','3',4)
		except ValueError as e:
			logger.error(e)
		
		# Test InventoryItem
		cat = []
		try:
			cat.append(InventoryItem('Rum','$9000', 1, '0.1', 'grains'))
			logger.info('I would spend ${} on {}'.format(cat[0].value, cat[0].name))
		except ValueError as e:
			logger.error('could not add item b/c: {}'.format(e), 32)
	
		# Test PurchaseItem
		purchases = []
		try:
			name = 'Rum'
			amount = '9000.9999999999998'
			#fails @ '9000.99999999999998'
			purchases.append(PurchaseItem(name, amount))
			logger.info('purchased {} of {}'.format(purchases[0].amount, purchases[0].name))
		except ValueError as e:
			logger.error('purchase failed: {}'.format(e))
	
		# Test find input files
		try:
			inputList = InputList(inputSearchPath, inputNumberExtractorRegex)
			logger.info(inputList.fileDict)
			outputList = OutputList(outputSearchPath, outputInfoExtractorRegex)
			logger.info(outputList.submissionList)
		except Exception as e:
			print(e)
	
		try:
			logger.write()
		except Exception as e:
			print(e)
		finally:
			logger.close()

# Set Script Entry Point
if __name__ == '__main__':
	Grader()
