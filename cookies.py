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

# Initialize a table to hold probability relationships
for row in range(8):
	tuple_probability.append([])
	for col in range(8):
		tuple_probability[row].append(0)

# Load all the tagged_recipes file
files = os.listdir("tagged_recipes")
for f in files:
	parse_learning_data(open("tagged_recipes/" + f))

# Calculate the probability of a tuple occurance
for line in parsed_lines:
	for i in range(len(line)):
		gram1 = ("", Empty)
		if i > 0:
			gram1 = line[i-1]
		token1 = gram1[1]

		gram2 = line[i]
		token2 = gram2[1] 

		print "(%s, %s)" % (gram2[0], token_description_verbose[token2])

		prob = tuple_probability[token1][token2]
		tuple_probability[token1][token2] = prob+1

# Print out the probability results
print "\nProbabilities: "
print "   E   U   Q   F   M   T   D   B"
for i in range(len(tuple_probability)):
	row = tuple_probability[i]
	print (token_description[i]),
	for num in row:
		print("%2d " % num),
	print ""


