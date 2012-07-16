from __future__ import division
import os

#Tag types
Unit = "Unit"
Quantity = "Quantity"
Food = "Food"
Modifier = "Modifier"
Time = "Time"
Degrees = "Degrees"
Boring = "Boring"

token_map = {
	"u" : Unit,
	"q" : Quantity,
	"f" : Food,
	"m" : Modifier,
	"t" : Time,
	"d" : Degrees,
	"b" : Boring
}

tokens = { Unit, Quantity, Food, Modifier, Time, Degrees, Boring }

token_description = ["U", "Q", "F", "M", "T", "D", "B"]
token_description_verbose = ["Unit", "Quantity", "Food", "Modifier", "Time", "Degrees", "Boring"]

tuples = {}
start_tag_count = {}
tag_count = {}
dictionary = {}

# Go through a tagged file and split it into
# (word, token) tuples, line by line.
# Appends results to parsed_lines array
def parse_learning_data(f):
	parsed_lines = []
	parsed_line = []
	for line in f:
		for word in line.split():
			word_parts = word.split("_")
			token = Boring

			word = word_parts[0]
			if (len(word_parts) > 1):
				token = token_map.get(word_parts[1][0], Boring)
			parsed_line.append((word, token))
		parsed_lines.append(parsed_line)
	return parsed_lines

def is_number(word):
	if len(word) > 0:
		try:
			float(word[0])
			return True
		except ValueError:
			return False

# Calculate the probability of a tuple occurance
def learn(parsed_lines):
	for line in parsed_lines:
		for i in range(len(line)):
			if i == 0:
				gram = line[0]
				(word, token) = gram

				count = start_tag_count[token]
				start_tag_count[token] = count + 1

				count = tag_count[token]
			else:
				gram1 = line[i-1]
				gram2 = line[i]

				(word1, token1) = gram1
				(word2, token2) = gram2

				prob = tuple_probability[token1][token2]
				tuple_probability[token1][token2] = prob+1

				count = dictionary[token2].get(word2.upper(), 0)
				dictionary[token2][word2.upper()] = count+1

				count = tag_count[token2]
				tag_count[token2] = count+1

for token in tokens:
	tuples[token] = {}
	start_tag_count[token] = 0
	tag_count[token] = 0
	dictionary[token] = {}

print tuples

# Load all the tagged_recipes file
files = os.listdir("tagged_recipes")
for f in files:
	data = parse_learning_data(open("tagged_recipes/" + f))
	learn(data)

def total_tag_count():
	total = 0
	for number in tag_count:
		total+=number
	return total

def viderbi():

	text = open("recipes/1.txt")
	states = [0, 1, 2, 3, 4, 5, 6]

	for line in text:
		words = line.split()
		V = []
		path = []

		for i in range(len(words)):
			V.append([])
			word = words[i]
			
			for state in states: #for each state
				word_sum = sum((dictionary[s].get(word.upper(), 0)) for s in states)
				if (word_sum == 0):
					word_sum = 1

				output_prob = dictionary[state].get(word.upper(), 0)/word_sum

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