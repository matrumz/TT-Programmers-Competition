class InputParams:
	moneyLimit = 0.0
	weightLimit = 0.0
	volumeLimit = 0.0

	def __init__(self, moneyLimit, weightLimit, volumeLimit):
		try:
			self.moneyLimit = float(moneyLimit)
			self.weightLimit = float(weightLimit)
			self.volumeLimit = float(volumeLimit)
		except ValueError as e:
			raise ValueError('{}: not a valid float param for InputParams'.format(e))
