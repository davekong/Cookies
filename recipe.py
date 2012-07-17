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


