possibleFG = {"grains", "dairy", "veggies", "meat"}
class InventoryItem:
	name = ""
	value = 0
	weight = 0
	volume = 0
	fG = ""
	

	def __init__(self, name, value, weight, volume, fG):

		self.name = name
		try:
			# Replace only the first dollar sign if found, more will be cause for error
			self.value = float(str(value).replace('$','',1))
			self.weight = float(weight)
			self.volume = float(volume)
		except ValueError:
			raise

		if fG in possibleFG:
			self.fG = fG
		else:
			raise ValueError('"{}" is not a valid food group'.format(fG))

		# Error on negatives
		if (self.value < 0 or self.weight < 0 or self.volume < 0):
			raise ValueError('Negative values not allowed in InventoryItems')
