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

token_description = ["e", "u", "q", "f", "m", "t", "d", "b"]

parsed_lines = []
token_incidence = {}
tuple_probability = []

for row in range(8):
	tuple_probability.append([])
	for col in range(8):
		tuple_probability[row].append(0)

f = open("tagged_recipes/1.txt", "r")
for line in f:
	parsed_line = []
	for word in line.split():
		word_parts = word.split("_")
		if (len(word_parts) > 1):
			token = tokens[word_parts[1][0]]
			parsed_line.append((word_parts[0], token))
		else:
			parsed_line.append((word_parts[0], Boring))
	parsed_lines.append(parsed_line)

for line in parsed_lines:
	for i in range(len(line)):
		gram1 = ("", Empty)
		if i > 0:
			gram1 = line[i-1]
		token1 = gram1[1]

		gram2 = line[i]
		token2 = gram2[1] 

		print gram1
		print gram2

		prob = tuple_probability[token1][token2]
		tuple_probability[token1][token2] = prob+1

print "   e   u   q   f   m   t   d   b"
for i in range(len(tuple_probability)):
	row = tuple_probability[i]
	print (token_description[i]),
	for num in row:
		print("%2d " % num),
	print ""


