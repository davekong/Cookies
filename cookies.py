from __future__ import division
import os

#Tag types
Unit = 0
Quantity = 1
Food = 2
Modifier = 3
Time = 4
Degrees = 5
Boring = 6

tokens = {
	"u" : Unit,
	"q" : Quantity,
	"f" : Food,
	"m" : Modifier,
	"t" : Time,
	"d" : Degrees,
	"b" : Boring
}

token_description = ["U", "Q", "F", "M", "T", "D", "B"]
token_description_verbose = ["Unit", "Quantity", "Food", "Modifier", "Time", "Degrees", "Boring"]

tuple_probability = []
start_tag_count = []
tag_count = []
parsed_lines = []
dictionary = []

# Go through a tagged file and split it into
# (word, token) tuples, line by line.
# Appends results to parsed_lines array
def parse_learning_data(f):
	parsed_line = []
	for line in f:
		for word in line.split():
			word_parts = word.split("_")
			token = Boring
			if (len(word_parts) > 1):
				token = tokens.get(word_parts[1][0], Boring)
			parsed_line.append((word_parts[0], token))
		parsed_lines.append(parsed_line)

def is_number(word):
	if len(word) > 0:
		try:
			float(word[0])
			return True
		except ValueError:
			return False

# Initialize a table to hold probability relationships
for row in range(7):
	tuple_probability.append([])
	tag_count.append(0)
	start_tag_count.append(0)
	dictionary.append({})
	for col in range(7):
		tuple_probability[row].append(0)

# Load all the tagged_recipes file
files = os.listdir("tagged_recipes")
for f in files:
	parse_learning_data(open("tagged_recipes/" + f))

# Calculate the probability of a tuple occurance
for line in parsed_lines:
	for i in range(len(line)):
		if i == 0:
			gram1 = line[0]
			count = start_tag_count[gram1[1]] 
			start_tag_count[gram1[1]] = count + 1
		else:
			gram1 = line[i-1]
			token1 = gram1[1]

			gram2 = line[i]
			token2 = gram2[1] 
			word2 = gram2[0]

			prob = tuple_probability[token1][token2]
			tuple_probability[token1][token2] = prob+1

			count = dictionary[token2].get(word2.upper(), 0)
			dictionary[token2][word2.upper()] = count+1

			count = tag_count[token2]
			tag_count[token2] = count+1

# Print out the probability results
print "\nProbabilities: "
print "     U     Q     F     M     T     D     B"
for i in range(len(tuple_probability)):
	row = tuple_probability[i]
	print (token_description[i]),
	for num in row:
		print("%4d " % num),
	print ""

def find_tag(word, prev_tag):
	array = tuple_probability[prev_tag]
	best_tag = Boring
	match = 0
	for x in range(len(array)):
		if array[x] > match:
			match = array[x]
			best_tag = x
	return best_tag

def total_tag_count():
	total = 0
	for number in tag_count:
		total+=number
	return total

def viderbi():

	text = open("recipes/2.txt")
	states = [0, 1, 2, 3, 4, 5, 6]

	for line in text:
		words = line.split()
		V = []
		path = []

		for i in range(len(words)):
			V.append([])
			word = words[i]
			
			for state in states: #for each state
				output_prob = dictionary[state].get(word.upper(), 0)/tag_count[state]

				#print (word, token_description_verbose[state], output_prob)

				if i == 0:
					V[i].append(output_prob * start_tag_count[state]/sum(start_tag_count))
					path.append([state])
				else:
					(prob, y0) = max((output_prob * tuple_probability[y0][state]/tag_count[y0] 
						* V[i-1][y0], y0) for y0 in states)
					V[i].append(prob)
					path[state].append(y0)

		if (len(words) == 0):
			continue

		(prob, state) = max([(V[len(words) - 1][y], y) for y in states])
		final_path = path[state]

		for i in range(len(words)):
				print("("+words[i] + ": " + token_description_verbose[final_path[i]] + ")"),
		print ""

viderbi()