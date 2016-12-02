class PurchaseItem:
	name = ""
	amount = 0

	def __init__(self, name, amount):
		self.name = name.strip()

		numericAmount = float(amount)

		if numericAmount.is_integer():
			self.amount = int(numericAmount)
		else:
			raise ValueError('{} is not an integer purchase amount.'.format(amount))

		if self.amount < 0:
			raise ValueError('Cannot purchase a negative quantity: {}'.format(self.amount))

	def __repr__(self):
		return '{},{}\n'.format(self.name, self.amount)
