 # coding=utf-8

import os, sys
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
			
			if len(food) == 0:
				if len(modifier) > 0:
					food = modifier
					modifier = []
				else:
					continue

			qty = sum(map(parse_number, quantity))
			if qty == 0:
				continue

			ingredient.food = clean_text(' '.join(food))
			ingredient.unit = Unit.parse(unit)
			ingredient.quantity = qty
			ingredient.modifier = ' '.join(modifier)

			recipe.add_ingredient(ingredient)
		
		elif len(time) > 0:
			recipe.baking_time = parse_number(time)
		elif len(degrees) > 0:
			recipe.temperature = parse_number(degrees)
	
	return recipe
	
valid_digits = set(string.digits).union(set('/'))
unicode_fraction=set([u'¼', u'½', u'¾', u'⅓', u'⅔'])
def clean_number(string):
	return ''.join(ch for ch in string if ch in valid_digits)

def clean_text(text):
	punc = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in punc).lower()

def parse_number(string):
	for ch in unicode_fraction:
		if ch in string:
			if string == u'¼':
				return float(0.25)
			if string == u'½':
				return float(0.5)
			if string == u'¾':
				return float(0.75)
			if string == u'⅓':
				return float(Fraction("1/3"))
			if string == u'⅔':
				return float(Fraction("2/3"))

	string = clean_number(string)
	if len(string) == 0:
		return 0

	try:
		return float(Fraction(string))
	except ValueError:
		'Attempted to parse an invalid fraction "%s"' % string
		return 0

def process_files(filename, folder=None):
		print("%s:" % filename)
		path = filename if folder is None else os.path.join(folder,filename)
		return output_results(path)

if len(sys.argv) < 2: 
	tag_folder = "tagged_recipes"
else :
	tag_folder = sys.argv[1]
tag_files = os.listdir(tag_folder)

for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "test_recipes"
plain_files = os.listdir(plain_folder)
if len(sys.argv) < 3:
	plain_folder = "recipes"
else:
	plain_folder = sys.argv[2]

recipes = []
if os.path.isdir(plain_folder):
	print "%s is a folder" % (plain_folder)
	plain_files = os.listdir(plain_folder)
	for plain_filename in plain_files:
		recipe = process_files(plain_filename, plain_folder)
		if recipe is None:
			continue
		recipes.append(recipe)
		for ing in recipe.ingredients:
			print("%.2f %s %s %s" % (ing.quantity, ing.unit, ing.modifier, ing.food))
else :
	plain_file = plain_folder
	recipe = process_files(plain_file)
	if recipe is not None:
		for ing in recipe.ingredients:
			print("%.2f %s %s %s" % (ing.quantity, ing.unit, ing.modifier, ing.food))