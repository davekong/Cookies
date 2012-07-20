 # coding=utf-8

import os, sys
import recipe_parser as rp
from random import choice
import string
from fractions import Fraction
from recipe import Recipe
from ingredient import Ingredient, Unit	

def process_files(filename, folder=None):
		print("%s:" % filename)
		path = filename if folder is None else os.path.join(folder,filename)
		return rp.parse_recipe(path)

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