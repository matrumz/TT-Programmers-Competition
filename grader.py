#!/usr/bin/python3

from inputParams import InputParams
from logger import Logger
from inventoryItem import InventoryItem
from purchaseItem import PurchaseItem
from fileLists import InputList, OutputList
import sys

def main():
	moduleTest()

# Used for script testing purposes only
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
	main()
