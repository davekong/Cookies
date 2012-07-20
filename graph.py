 # coding=utf-8
import os
import recipe_parser as rp
import string
from fractions import Fraction
from recipe import Recipe
from ingredient import Ingredient, Unit
import gexf as g

tag_folder = "tagged_recipes"
tag_files = os.listdir(tag_folder)

for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "downloaded_recipes"
plain_files = os.listdir(plain_folder)
recipes = []

for plain_filename in plain_files:
	print("Parsing recipe %s" % plain_filename)
	recipe = rp.parse_recipe(plain_folder + "/" + plain_filename)
	if recipe is None:
		continue
	recipes.append((plain_filename, recipe))

gexf = g.Gexf("Hackerschool", "Chocolate Chip Cookie Recipes") 
graph = gexf.addGraph("directed","static","Chocolate Chip Cookie Recipes")

for i in range(len(recipes)):
	(recipe_name, recipe) = recipes[i]
	print("Adding node %s" % recipe_name)
	n = graph.addNode(str(i), recipe_name)

for i in range(len(recipes)):
	print("Adding edge from node %s" % recipes[i][0])
	for j in range(len(recipes)):

		if i == j:
			continue

		(r1_name, r1) = recipes[i]
		(r2_name, r2) = recipes[j]

		val = r1.compare(r2)
		if val > 0:
			graph.addEdge(str(i)+str(j), str(i), str(j), str(val))

output_file = open("graph.gexf", "w")
gexf.write(output_file)