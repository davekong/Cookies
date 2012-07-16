from __future__ import division
import string

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

tokens = (Unit, Quantity, Food, Modifier, Time, Degrees, Boring)

token_description = ["U", "Q", "F", "M", "T", "D", "B"]

tuples = {}
start_tag_count = {}
tag_count = {}
dictionary = {}

for token in tokens:
	tuples[token] = {}
	start_tag_count[token] = 0
	tag_count[token] = 0
	dictionary[token] = {}

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

valid_characters = set(string.letters).union(string.digits)
def clean(word):
	word = word.upper()
	s = ''.join(ch for ch in word if ch in valid_characters)
	return s

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

				prob = tuples[token1].get(token2, 0)
				tuples[token1][token2] = prob+1

				clean_word = clean(word2)
				count = dictionary[token2].get(clean_word, 0)
				dictionary[token2][clean_word] = count+1

				count = tag_count[token2]
				tag_count[token2] = count+1

def total_tag_count():
	sum(tag_count[token] for token in tokens)

def viterbi(states, output, output_prob, tuple_probability, start_probability):
	if len(output) == 0:
		return []

	V = []
	path = {}

	for i in range(len(output)):
		V.append({})
		word = clean(output[i])
		
		for state in states: #for each state
			probability = output_prob.get(state, {}).get(word, 0)
			if i == 0:
				V[i][state] = (probability * start_probability[state])
				path[state] = [state]
			else:
				(prob, best_state) = max((V[i-1][s] * probability * tuple_probability[s][state], s) for s in states)
				V[i][state] = prob
				path[state] = path[best_state] + [state]

	(prob, state) = max([(V[len(output) - 1][y], y) for y in states])
	final_path = path[state]

	return [(output[i], final_path[i]) for i in range(len(output))]


def learn_from_file(path):
	data = parse_learning_data(open(path))
	learn(data)

def tag_file(path):
	output_file = open(path)
	output_probability = {}
	tuple_probability = {}
	start_probability = {}

	for token in tokens:
		output_probability[token] = {}
		tuple_probability[token] = {}
		start_probability[token] = start_tag_count[token]/sum(start_tag_count.get(t, 0) for t in tokens)
		for word in dictionary[token]:
			output_probability[token][word] = dictionary[token].get(word, 0)/tag_count[token]
		for token2 in tokens:
			tuple_probability[token][token2] = tuples[token].get(token2, 0)/tag_count[token]

	for line in output_file:
		return [viterbi(tokens, line.split(), output_probability, tuple_probability, start_probability)
			for line in output_file]

