 # coding=utf-8

from __future__ import division
import string
import re
from bs4 import BeautifulSoup
from recipe import Recipe
from ingredient import Ingredient
from ingredient import Unit as u
from fractions import Fraction

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

def strip_parens(line):
	return re.sub("\(.*?\)",'',line)

valid_characters = set(string.letters).union(string.digits)
def clean(word):
	word = word.upper()
	s = ''.join(ch for ch in word if ch in valid_characters)
	return s

# Populates all of the relevant statistics from a parsed file
def learn(parsed_lines):
	for line in parsed_lines:
		for i in range(len(line)):
			(word, token) = line[i]

			clean_word = clean(word)
			count = dictionary[token].get(clean_word, 0)
			dictionary[token][clean_word] = count+1

			count = tag_count[token]
			tag_count[token] = count+1

			if i == 0:
				count = start_tag_count[token]
				start_tag_count[token] = count + 1
			else:
				(pword, ptoken) = line[i-1]

				prob = tuples[ptoken].get(token, 0)
				tuples[ptoken][token] = prob+1


def total_tag_count():
	sum(tag_count[token] for token in tokens)

def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7d" % i,
    print
 
    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print

# This was modeled after the example at http://en.wikipedia.org/wiki/Viterbi_algorithm
def viterbi(states, output, output_prob, tuple_probability, start_probability):
	if len(output) == 0:
		return []

	V = []
	path = {}

	for i in range(len(output)):
		V.append({})

		word = clean(output[i])
		newpath = {}
		probability = {}

		prob_sum = 0
		for state in states:
			probability[state] = output_prob.get(state, {}).get(word, 0)
			prob_sum += probability[state]

		# Handle unkown words
		if prob_sum == 0:
			for state in states:
				probability[state] = 1.0
		
		for state in states:
			if i == 0:
				V[i][state] = (probability[state] * start_probability[state])
				newpath[state] = [state]
			else:
				(prob, best_state) = max([(V[i-1][s] * probability[state] * tuple_probability[s][state], s) for s in states])
				V[i][state] = prob
				newpath[state] = path[best_state] + [state]

		path = newpath

	(prob, state) = max([(V[len(output) - 1][y], y) for y in states])
	final_path = path[state]

	return [(output[i], final_path[i]) for i in range(len(output))]


def learn_from_file(path):
	data = parse_learning_data(open(path))
	learn(data)

def parse_recipe(filepath):
	results = tag_file(filepath)
	if results is None:
		return None

	recipe = Recipe()

	for line in results:
		food = words_with_token(line, Food)
		quantity = words_with_token(line, Quantity)
		unit = words_with_token(line, Unit)
		modifier = words_with_token(line, Modifier)
		time = words_with_token(line, Time)
		degrees = words_with_token(line, Degrees)
		

		if len(quantity) > 0:
			ingredient = Ingredient()
			
			if len(food) == 0:
				if len(modifier) > 0:
					food = modifier
					modifier = []
				else:
					continue

			qty = sum(map(parse_number, quantity))
			if qty == 0:
				continue

			ingredient.food = clean_text(' '.join(food))
			ingredient.unit = u.parse(unit)
			ingredient.quantity = qty
			ingredient.modifier = ' '.join(modifier)

			recipe.add_ingredient(ingredient)
		
		elif len(time) > 0:
			recipe.baking_time = parse_number(time)
		elif len(degrees) > 0:
			recipe.temperature = parse_number(degrees)
	
	return recipe

valid_digits = set(string.digits).union(set('/'))
unicode_fraction=set([u'¼', u'½', u'¾', u'⅓', u'⅔'])
def clean_number(string):
	return ''.join(ch for ch in string if ch in valid_digits)

def clean_text(text):
	punc = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in punc).lower()

def parse_number(string):
	for ch in unicode_fraction:
		if ch in string:
			if string == u'¼':
				return float(0.25)
			if string == u'½':
				return float(0.5)
			if string == u'¾':
				return float(0.75)
			if string == u'⅓':
				return float(Fraction('1/3'))
			if string == u'⅔':
				return float(Fraction('2/3'))

	string = clean_number(string)
	if len(string) == 0:
		return 0

	try:
		return float(Fraction(string))
	except ValueError:
		'Attempted to parse an invalid fraction "%s"' % string
		return 0

def words_with_token(line, token):
	words = []
	for (w, t) in line:
		if t == token:
			words.append(w)
	return words

def tag_file(path):
	output_file = open(path)
	soup = BeautifulSoup(output_file)
	if soup is None:
		return []

	clean_text = '\n'.join(soup.findAll(text=True))
	clean_text = strip_parens(clean_text)

	output_probability = {}
	tuple_probability = {}
	start_probability = {}

	for token in tokens:
		count = tag_count[token]
		if count == 0:
			count = 1

		output_probability[token] = {}
		tuple_probability[token] = {}
		start_probability[token] = start_tag_count[token]/sum(start_tag_count.get(t, 0) for t in tokens)
		for word in dictionary[token]:
			output_probability[token][word] = dictionary[token].get(word, 0)/count
		for token2 in tokens:
			tuple_probability[token][token2] = tuples[token].get(token2, 0)/count

	return [viterbi(tokens, line.split(), output_probability, tuple_probability, start_probability)
		for line in clean_text.split('\n')]

