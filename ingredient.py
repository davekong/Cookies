#imports

class Unit:
	ITEM = 0
	TSP = 1
	OZ = 2
	TBSP = 3
	CUP = 4
	PINCH = 5
	DASH = 6


class Ingredient:
#constructor (init)
	def __init__(quantity = 0, unit = Unit.ITEM, food = '', modifier = ''):
		self.quantity = quantity
		self.unit = unit
		self.food = food
		self.modifier = modifier

#utility functions
	def convert_to(unit):
		# update quantity
		# update to new unit
		return
