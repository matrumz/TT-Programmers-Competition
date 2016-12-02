import re

class InputParams:
	moneyLimit = 0.0
	weightLimit = 0.0
	volumeLimit = 0.0

	def __init__(self, moneyLimit, weightLimit, volumeLimit):
		try:
			# Replace only the first dollar sign if found, more will be cause for error
			self.moneyLimit = float(str(moneyLimit).replace('$','',1))
			self.weightLimit = float(weightLimit)
			self.volumeLimit = float(volumeLimit)
		except ValueError as e:
			raise ValueError('{}: not a valid float param for InputParams'.format(e))

		# Error on negatives
		if (self.moneyLimit < 0 or self.weightLimit < 0 or self.volumeLimit < 0):
			raise ValueError('Negative values not allowed in input params')
