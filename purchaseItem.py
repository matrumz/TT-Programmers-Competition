class PurchaseItem:
	name = ""
	amount = 0

	def __init__(self, name, amount):
		self.name = name

		numericAmount = float(amount)

		if numericAmount.is_integer():
			self.amount = int(numericAmount)
		else:
			raise ValueError('{} is not an integer purchase amount.'.format(amount))

