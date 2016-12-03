class SubmissionResult:

	totalCost = 0.0
	totalWeight = 0.0
	totalVolume = 0.0
	fGDistribution = {}
	totalItems = 0
	overPurchasedItemsDict = {}

	overPurchased = True
	overCost = True
	overWeight = True
	overVolume = True
	badDist = True

	def __init__(self, totalItems, overPurchasedItemsDict, totalCost, totalWeight, totalVolume, fGCount, params, task):
		self.totalItems = totalItems
		self.overPurchasedItemsDict = overPurchasedItemsDict
		self.totalCost = totalCost
		self.totalWeight = totalWeight
		self.totalVolume = totalVolume
		for key, value in fGCount.items():
			self.fGDistribution[key] = value/self.totalItems

		self.overPurchased = len(self.overPurchasedItemsDict) > 0
		self.overCost = self.totalCost > params.moneyLimit
		self.overWeight = self.totalWeight > params.weightLimit and int(task) > 1
		self.badDist = any(dist > .3 or dist < .2 for dist in self.fGDistribution.values()) and task == "3"
		self.overVolume = self.totalVolume > params.volumeLimit and task == "4"

	def __repr__(self):
		return 'totalItems:{}\noverPurchasedItemsDict:{}\ntotalCost:{}\ntotalweight:{}\ntotalVolume:{}\nfGDistribution:{}\noverPurchased:{}\noverCost:{}\noverWeight:{}\noverVolume:{}\nbadDist:{}\n'.format(self.totalItems, self.overPurchasedItemsDict, self.totalCost, self.totalWeight, self.totalVolume, self.fGDistribution, self.overPurchased, self.overCost, self.overWeight, self.overVolume, self.badDist)
