#!/usr/bin/python3

from inputParams import InputParams
from logger import Logger
from inventoryItem import InventoryItem, possibleFG
from purchaseItem import PurchaseItem
from fileLists import InputList, OutputList
from results import SubmissionResult
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
				try: # Parse submission file
					submissionContents = self.loadOutputFile(submission.path)
				except Exception as e:
					self.syslog.error("Error loading OUTPUT FILE {}: {}".format(submission.path, e))
				try: # Validate answer (solution)
					result = self.validateOutputFile(submissionContents, submission.path, submission.task)
					self.syslog.result(submission.name, submission.task, submission.inputNumber, result)
				except Exception as e:
					self.syslog.error("Error validating submission {}: {}".format(submission.path, e))
	
	def validateOutputFile(self, pItems, path, task):
		sumCost = 0.0
		sumWeight = 0.0
		sumVolume = 0.0
		sumCategories = {}
		for cat in possibleFG:
			sumCategories[cat] = 0
		numItems = 0
		itemPurchaseAmount = {}
		overPurchasedItemDict = {}
		
		# Get results of all purchases
		for p in pItems:
			i = {}
			# Find the item in the inventory list
			try:
				iList = list(filter(lambda invItem: invItem.name == p.name, self.inventoryList))
				if len(iList) > 1:
					raise ValueError("Item '{}' found more than once in catalogue".format(p.name))
				elif len(iList) < 1:
					raise IndexError("Filter failed to find item")
				else: # == 1
					i = iList[0]
			except IndexError:
				self.syslog.warning("Item '{}' not found in catalogue".format(p.name), None, path)
				continue
			except Exception as e:
				self.syslog.warning("Error finding '{}' in catalogue: {}".format(p.name, e), None, path)
				continue

			# Calculate sums
			sumCost += p.amount * i.value
			sumWeight += p.amount * i.weight
			sumVolume += p.amount * i.volume
			sumCategories[i.fG] += p.amount
			numItems += p.amount
			if p.name in itemPurchaseAmount:
				itemPurchaseAmount[p.name] += p.amount
			else:
				itemPurchaseAmount[p.name] = p.amount
			purchasedAmount = itemPurchaseAmount[p.name]
			if purchasedAmount > i.quantity:
				overPurchasedItemDict[p.name] = purchasedAmount;

		# Return computed result
		return SubmissionResult(numItems, overPurchasedItemDict, sumCost, sumWeight, sumVolume, sumCategories, self.inputParam, task)

	def loadOutputFile(self,path):
		fileContents = ""
		purchases = []

		try:
			f = open(path, 'r')
			fileContents = f.read()
		except Exception as e:
			self.syslog.error("Could not read output file {}: {}".format(path, e))
		finally:
			try:
				f.close()
			except:
				pass

		# Replace all newlines with ';'
		# Then tokenize on ';' for purchase objects strings
		# Find all remaining ';' in each purchase object string and delete them
		# This should give valid POSs in the following cases
		# 		all POSs on one line, ';' delimited
		# 		all POSs on individual lines
		#			';' terminated
		# 			not ';' terminated
		fileContents = fileContents.replace('\n',';')
		pOSList = fileContents.split(';')
		for pOS in pOSList:
			pOS = pOS.replace(';', '')
			splitPOS = pOS.split(',')
			if not pOS.strip(): # if empty string (pOS.strip() == '' was NOT working)
				continue
			if len(splitPOS) != 2:
				self.syslog.warning("Invalid purchase object string '{}' b/c wrong number of commas".format(pOS), None, path)
				continue
			try:
				purchases.append(PurchaseItem(splitPOS[0], splitPOS[1]))
			except Exception as e:
				self.syslog.warning("Invalid PurchaseItem '{}': {}".format(pOS, e), None, path)
				continue

		return purchases

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
			f.close()
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
