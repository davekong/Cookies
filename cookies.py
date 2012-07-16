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
		return 0

	found_line = 0
	for line in results:
		
		parsed_line = []
		for tagged_pair in line:
			(word, token) = tagged_pair
			#print("(%s : %s)" % (word, token)),
		#print ""
		

		food = ' '.join(words_with_token(line, rp.Food))
		quantity = ' '.join(words_with_token(line, rp.Quantity))
		unit = ' '.join(words_with_token(line, rp.Unit))
		modifier = ' '.join(words_with_token(line, rp.Modifier))
		time = ' '.join(words_with_token(line, rp.Time))
		degrees = ' '.join(words_with_token(line, rp.Degrees))
		
		if len(food) > 0:
			print(quantity, unit, modifier, food)
			found_line += 1
		elif len(time) > 0:
			print(time + " minutes")
		elif len(degrees) > 0:
			print(degrees + " degrees")

	return found_line

tag_folder = "tagged_recipes"
tag_files = os.listdir(tag_folder)

for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "recipes"
plain_files = os.listdir(plain_folder)
for plain_filename in plain_files:
	output_results(plain_folder + "/" + plain_filename)
	print ""
