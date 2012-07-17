import os
import recipe_parser as rp
from random import choice
import string
from fractions import Fraction
from recipe import Recipe
from ingredient import Ingredient, Unit


def words_with_token(line, token):
	words = []
	for (w, t) in line:
		if t == token:
			words.append(w)
	return words

#TODO: Move this into recipe_parser.py so it's returned by tag_file()
def output_results(filepath):
	results = rp.tag_file(filepath)
	if results is None:
		return None

	recipe = Recipe()

	for line in results:
		food = words_with_token(line, rp.Food)
		quantity = words_with_token(line, rp.Quantity)
		unit = words_with_token(line, rp.Unit)
		modifier = words_with_token(line, rp.Modifier)
		time = words_with_token(line, rp.Time)
		degrees = words_with_token(line, rp.Degrees)
		

		if len(quantity) > 0:
			ingredient = Ingredient()
			ingredient.food = ' '.join(food)
			ingredient.unit = Unit.parse(unit)
			ingredient.quantity = sum(map(parse_number, quantity))
			ingredient.modifier = ' '.join(modifier)

			recipe.add_ingredient(ingredient)
		elif len(time) > 0:
			recipe.baking_time = parse_number(time)
		elif len(degrees) > 0:
			recipe.temperature = parse_number(degrees)
	print recipe
	return recipe
	
valid_digits = set(string.digits).union(set('/'))
def clean_number(string):
	return ''.join(ch for ch in string if ch in valid_digits)

def parse_number(string):
	string = clean_number(string)
	if len(string) == 0:
		return 0

	return float(Fraction(string))

tag_folder = "tagged_recipes"
tag_files = os.listdir(tag_folder)

for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "recipes"
plain_files = os.listdir(plain_folder)
for plain_filename in plain_files:
	print("%s:" % plain_filename)
	recipe = output_results(plain_folder + "/" + plain_filename)
	if recipe is None:
		continue
	for ing in recipe.ingredients:
		print("%.2f %s %s %s" % (ing.quantity, ing.unit, ing.modifier, ing.food))
