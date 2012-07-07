import os

#Tag types
Empty = 0
Unit = 1
Quantity = 2
Food = 3
Modifier = 4
Time = 5
Degrees = 6
Boring = 7

tokens = {
	"e" : Empty,
	"u" : Unit,
	"q" : Quantity,
	"f" : Food,
	"m" : Modifier,
	"t" : Time,
	"d" : Degrees,
	"b" : Boring
}

token_description = ["E", "U", "Q", "F", "M", "T", "D", "B"]
token_description_verbose = ["Empty", "Unit", "Quantity", "Food", "Modifier", "Time", "Degrees", "Boring"]

token_incidence = {}
tuple_probability = []
parsed_lines = []

# Go through a tagged file and split it into
# (word, token) tuples, line by line.
# Appends results to parsed_lines array
def parse_learning_data(f):
	for line in f:
		parsed_line = []
		for word in line.split():
			word_parts = word.split("_")
			if (len(word_parts) > 1):
				token = tokens.get(word_parts[1][0], Boring)
				parsed_line.append((word_parts[0], token))
			else:
				parsed_line.append((word_parts[0], Boring))
		parsed_lines.append(parsed_line)

# Initialize a n-Dim table to hold probability relationships
# Previous by Currrent by isNumber
for row in range(8):
	tuple_probability.append([])
	for col in range(8):
		tuple_probability[row].append([])
		for num in range(2):
			tuple_probability[row][col].append(0)

# Load all the tagged_recipes file
files = os.listdir("tagged_recipes")
for f in files:
	parse_learning_data(open("tagged_recipes/" + f))

# Calculate the probability of a tuple occurrence
for line in parsed_lines:
	for i in range(len(line)):
		gram1 = ("", Empty)
		if i > 0:
			gram1 = line[i-1]
		token1 = gram1[1]

		gram2 = line[i]
		token2 = gram2[1] 

		print "(%s, %s)" % (gram2[0], token_description_verbose[token2])
				
		if gram2[0][0].isdigit():
			tuple_probability[token1][token2][0] += 1
		else:
			tuple_probability[token1][token2][1] += 1

# Print out the probability results
print "\nProbabilities: "
for i in range(len(tuple_probability)):
	#print token_description[i] +"  E   U   Q   F   M   T   D   B"
	print token_description[i] +"\t   N  ~N"
	for j in range(len(tuple_probability[i])):
		row = tuple_probability[i][j]
		print ("\t" +token_description[j]),
		for num in row:
			print("%2d " % num),
		print ""
	print "---------------------------"

# Try to parse the untagged recipes
untagged_files = os.listdir("recipes")
tagged_tuple_lines = []
for f in untagged_files:
	text = open("recipes/" + f)
	for line in text:
		tagged_tuples = []
		words = line.split()
		prev_tag = Empty
		for i in range(len(words)):
			word = words[i]
			array = tuple_probability[prev_tag]
			best_tag = Boring
			match = 0
			for x in range(len(array)):
				if word[0].isdigit():
					if array[x][0] > match:
						match = array[x][0]
						best_tag = x
				else:
					if array[x][1] > match:
						match = array[x][1]
						best_tag = x
			prev_tag = best_tag
			tagged_tuples.append((word, best_tag))
		tagged_tuple_lines.append(tagged_tuples)

for line in tagged_tuple_lines:
	for pair in line:
			print("(%s, %s)" % (pair[0], token_description_verbose[pair[1]])),
	print "\n"

