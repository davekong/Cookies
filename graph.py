import os
import recipe_parser as rp
import string
from fractions import Fraction
from recipe import Recipe
from ingredient import Ingredient, Unit
import gexf as g

def words_with_token(line, token):
	words = []
	for (w, t) in line:
		if t == token:
			words.append(w)
	return words

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
			ingredient.food = clean_text(' '.join(food))
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

def clean_text(text):
	punc = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in punc).lower()

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
recipes = []

for plain_filename in plain_files:
	recipe = output_results(plain_folder + "/" + plain_filename)
	if recipe is None:
		continue
	recipes.append((plain_filename, recipe))

gexf = g.Gexf("Hackerschool", "Chocolate Chip Cookie Recipes") 
graph = gexf.addGraph("directed","static","Chocolate Chip Cookie Recipes")

for i in range(len(recipes)):
	(recipe_name, recipe) = recipes[i]
	graph.addNode(str(i), recipe_name)

for i in range(len(recipes)):
	for j in range(len(recipes)):
		if i == j:
			continue
		(r1_name, r1) = recipes[i]
		(r2_name, r2) = recipes[j]

		val = r1.compare(r2)
		graph.addEdge(str(i)+str(j), str(i), str(j), str(val))

output_file = open("graph.gexf", "w")
gexf.write(output_file)