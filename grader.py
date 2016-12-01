#!/usr/bin/python3

from taskParams import TaskParams
from logger import Logger
from inventoryItem import InventoryItem
from purchaseItem import PurchaseItem
import sys

def moduleTest():
	param = TaskParams(1,2,3,4)
	path = './log.txt'
	
	try:
		logger = Logger(path, 'OVERWRITE')
	except ValueError:
		print('Logger open value error')
		sys.exit()
	except IOError:
		print("Logger open io error")
		sys.exit()
	
	logger.warning(param.moneyLimit, 11)
	logger.error(param.weightLimit, 12, 'grader.py')
	
	cat = []
	try:
		cat.append(InventoryItem('Rum','9000', 1, '0.1', 'grains'))
		logger.info('I would spend ${} on {}'.format(cat[0].value, cat[0].name))
	except ValueError as e:
		logger.error('could not add item b/c: {}'.format(e), 32)

	purchases = []
	try:
		purchases.append(PurchaseItem('Rum', '9000.0'))
		logger.info('purchase made')
	except ValueError as e:
		logger.error('purchase failed: {}'.format(e))

	try:
		logger.write()
	except Exception as e:
		print(e)



moduleTest()
