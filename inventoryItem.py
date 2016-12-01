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
			self.value = float(value)
			self.weight = float(weight)
			self.volume = float(volume)
		except ValueError:
			raise

		if fG in possibleFG:
			self.fG = fG
		else:
			raise ValueError('"{}" is not a valid food group'.format(fG))
