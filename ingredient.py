#imports
import string

class Unit:
	ITEM = 'item'
	TSP = 'tsp'
	OZ = 'oz'
	TBSP = 'tbsp'
	CUP = 'cup'
	LB = 'lb'

	@staticmethod
	def chk_str(array,unit):
		for test in array:
			if test in unit:
				return True
		return False

	@staticmethod
	def parse(unit):
		if len(unit) == 0:
			return Unit.ITEM
		unit = ''.join(ch for ch in unit[0] if ch in set(string.letters)).lower()
		
		if Unit.chk_str(["tsp","teaspoon"],unit):
			return Unit.TSP
		elif Unit.chk_str(["tbs", "tablespoon"],unit):
			return Unit.TBSP
		elif Unit.chk_str(["cup"], unit) or unit == "c":
			return Unit.CUP
		elif Unit.chk_str(["oz", "ounce"], unit):
			return Unit.OZ
		elif Unit.chk_str(["pound", "lb"], unit):
			return Unit.LB
		else:
			return Unit.ITEM
		

class Ingredient:
#constructor (init)
	def __init__(self, quantity = 0, unit = Unit.ITEM, food = '', modifier = ''):
		self.quantity = quantity
		self.unit = unit
		self.food = food
		self.modifier = modifier

#utility functions
	def convert_to(unit):
		# update quantity
		# update to new unit
		return
