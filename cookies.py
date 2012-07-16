import os
import recipe_parser as rp
from random import choice

def words_with_token(line, token):
	words = []
	for (w, t) in line:
		if t == token:
			words.append(w)
	return words

def output_results(filepath):
	results = rp.tag_file(filepath)
	if results is None:
		return []

	parsed_results = []

	for line in results:
		
		parsed_line = []		

		food = words_with_token(line, rp.Food)
		quantity = words_with_token(line, rp.Quantity)
		unit = words_with_token(line, rp.Unit)
		modifier = words_with_token(line, rp.Modifier)
		time = words_with_token(line, rp.Time)
		degrees = words_with_token(line, rp.Degrees)
		
		if len(unit) > 0 and len(time) == 0 and len(degrees) == 0:
			parsed_results.append({ rp.Quantity: quantity,
							 rp.Unit: unit,
							 rp.Modifier: modifier,
							 rp.Food : food })
		elif len(time) > 0:
			parsed_results.append({ rp.Time : time })
		elif len(degrees) > 0:
			parsed_results.append({ rp.Degrees : degrees })

	return parsed_results

tag_folder = "tagged_recipes"
tag_files = os.listdir(tag_folder)

for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "recipes"
plain_files = os.listdir(plain_folder)
for plain_filename in plain_files:
	print("%s:" % plain_filename)
	output = output_results(plain_folder + "/" + plain_filename)
	for line in output:
		print line
	print("")
