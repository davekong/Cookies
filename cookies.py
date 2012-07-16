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

for line in results:
	for tagged_pair in line:
		(word, token) = tagged_pair
		print("(%s : %s)" % (word, token)),
	print ""