class TaskParams:
	task = 0
	moneyLimit = 0
	weightLimit = 0
	volumeLimit = 0

	def __init__(self, task, moneyLimit, weightLimit, volumeLimit):
		self.task = task
		self.moneyLimit = moneyLimit
		self.weightLimit = weightLimit
		self.volumeLimit = volumeLimit
