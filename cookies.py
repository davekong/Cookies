import os
import recipe_parser as rp
from random import choice

tag_folder = "tagged_recipes"
tag_files = os.listdir(tag_folder)
for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "recipes"
plain_files = os.listdir(plain_folder)
results = rp.tag_file(plain_folder+"/"+choice(plain_files))

def words_with_token(line, token):
	words = []
	for (w, t) in line:
		if t == token:
			words.append(w)
	return words

for line in results:
	'''
	parsed_line = []
	for tagged_pair in line:
		(word, token) = tagged_pair
		print("(%s : %s)" % (word, token)),
	print ""
	'''

	food = ' '.join(words_with_token(line, rp.Food))
	quantity = ' '.join(words_with_token(line, rp.Quantity))
	unit = ' '.join(words_with_token(line, rp.Unit))
	
	if len(food) > 0:
		print("%s %s %s" % (quantity, unit, food))