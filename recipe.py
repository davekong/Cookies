#imports
import ingredient

class Recipe:
#properties

#constructor (init)
	def __init__(ingredients = [], baking_time = 0, temperature = 0):
		apply(add_ingredient, ingredients)
		self.baking_time = baking_time
		self.temperature = temperature

#getters & setters


#utility functions
	def add_ingredient(ingredient):
		if type(ingredient) == Ingredient:
			ingredients.append(ingredient)
		else:
			raise Exception("This is not an ingredient")

	def add_ingredients(*ingreds):
		for ingredient in ingreds:
			self.add_ingredient(ingredient)


