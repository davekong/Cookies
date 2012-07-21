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

plain_folder = "lots_of_recipes"
plain_files = os.listdir(plain_folder)
recipes = []

for plain_filename in plain_files:
	print("Parsing recipe %s" % plain_filename)
	recipe = rp.parse_recipe(plain_folder + "/" + plain_filename)
	if recipe is None:
		continue
	recipes.append((plain_filename.replace('.txt', ''), recipe))

gexf = g.Gexf("Hackerschool", "Chocolate Chip Cookie Recipes") 
graph = gexf.addGraph("undirected","static","Chocolate Chip Cookie Recipes")
dupeAttr = graph.addNodeAttribute("duplicates", '0', "Integer")
ingAttr = graph.addNodeAttribute("ingredients", '', "String")

non_duplicate_recipes = set(recipes)
duplicate_count = {}

# Trim out all the duplicate recipes
print('Counting duplicate recipes...')

for i in range(len(recipes)):
	# Check against every other recipe once
	if recipes[i] not in non_duplicate_recipes:
		continue

	for j in range(len(recipes)):

		if j <= i:
			continue
		
		(r1_name, r1) = recipes[i]
		(r2_name, r2) = recipes[j]

		# If they turn out to be equal, remove the second recipe from the list
		if round(r1.compare(r2)) == 1.0:
			if recipes[j] in non_duplicate_recipes:
				non_duplicate_recipes.remove(recipes[j])
			dupes = duplicate_count.get(r1_name, 0) # Increase duplicate count
			duplicate_count[r1_name] = dupes + 1
			print('%s is a duplicate of %s' % (r2_name, r1_name))

	recipe = recipes[i][0]
	dupes = duplicate_count.get(recipe, 0)
	print('Removed %i duplicates of recipe %s' % (dupes, recipe))

non_duplicate_recipes = list(non_duplicate_recipes)

# Add a node for each unique recipe
print('Adding nodes...')
for i in range(len(non_duplicate_recipes)):
	(recipe_name, recipe) = non_duplicate_recipes[i]
	n = graph.addNode(str(i), recipe_name)
	dupe_count = duplicate_count.get(recipe_name, 0)
	n.addAttribute(dupeAttr, str(dupe_count))
	n.addAttribute(ingAttr, ', '.join(
		['%.2f %s %s' % (ing.quantity, ing.unit, ing.food) for ing in recipe.ingredients]))


# Calculate the difference between all the remaining nodes
print('Adding edges...')
for i in range(len(non_duplicate_recipes)):
	for j in range(len(non_duplicate_recipes)):

		if i <= j:
			continue		

		(r1_name, r1) = non_duplicate_recipes[i]
		(r2_name, r2) = non_duplicate_recipes[j]

		val = r1.compare(r2)
		if val > 0:
			graph.addEdge(str(i)+str(j), str(i), str(j), str(val))
			print('Adding edge from %s to %s' % (r1_name, r2_name))

print('Saving graph...')
output_file = open("graph.gexf", "w")
gexf.write(output_file)