#imports
from ingredient import Ingredient, Unit

class Recipe:

#constructor (init)
	def __init__(self, ingredients = [], baking_time = 0, temperature = 0):
		self.ingredients = []
		for ing in ingredients:
			self.add_ingredient(ing)
		self.baking_time = baking_time
		self.temperature = temperature

#utility functions
	def add_ingredient(self, ingredient):
		if ingredient.__class__ is Ingredient:
			self.ingredients.append(ingredient)
		else:
			raise Exception("This is not an ingredient, it is a %s" % ingredient.__class__)

	def add_ingredients(self, *ingreds):
		for ingredient in ingreds:
			self.add_ingredient(ingredient)

	def quantity_of(self, ing, unit):
		quantity = 0
		for ingredient in self.ingredients:
			if ingredient.food == ing:
				quantity += Unit.convert(ingredient.quantity, ingredient.unit, unit)
		return quantity

	def compare(self, other):
		value = 0
		
		#  Create a list of all ingredients
		r1_ings = set()
		r2_ings = set()
		
		for ing in self.ingredients:
			if len(ing.food) > 0:
				r1_ings.add(ing.food)
		for ing in other.ingredients:
			if len(ing.food) > 0:
				r2_ings.add(ing.food)

		common_ings = r1_ings.intersection(r2_ings)

		if len(common_ings) < 2:
			return 0

		#  Create two dicts with each ing/qty pair
		r1 = {}
		r2 = {}

		for ing in r1_ings.union(r2_ings):
			r1[ing] = self.quantity_of(ing, Unit.TSP)
			r2[ing] = other.quantity_of(ing, Unit.TSP)

		scale_ing = ''
		min_val = 1000000000
		for recipe in [r1, r2]:
			for ing in common_ings:
				if recipe[ing] < min_val and r1[ing] > 0 and r2[ing] > 0:
					scale_ing = ing
					min_val = recipe[ing]


		for recipe in [r1, r2]:
			scale_value = recipe[scale_ing]
			for ing in recipe:
				qty = recipe[ing]
				recipe[ing] = qty / scale_value
		
		print ''
		print r1
		print r2 

		count = len(r1_ings.union(r2_ings))

		weight = 1.0/(count-1)
		
		for ing in common_ings:
			if ing == scale_ing:
				continue
			numerator = min(r1[ing], r2[ing])
			denominator = max(r1[ing], r2[ing])
		
			if denominator == 0:
				continue
			similarity = float(numerator) / float(denominator)
			value += (weight * similarity)
		
		return value
