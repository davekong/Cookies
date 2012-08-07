Chocolate Chip Cookies
======================

This is a series of recipe parsing scripts for chocolate chip cookies. 

Using a hidden markov model, the parser identifies the salient features of a recipe. For example, given the line "1 tbsp baking powder", it will output a structured Ingredient object with a quantity of 1.0, a unit of TBSP and the food "baking powder". Ingredient objects are collected into Recipe objects, which can then be compared with one another.

Dependencies
============
Build dependencies are listed in requirements.txt, which can be used with ```pip install -r requirements.txt```.

Using the Parser
==================
To see the parser in action, run
```
python cookies.py tagged_recipes recipes
```
This will train the parser on the recipes placed in /tagged_recipes and then process all recipes in /recipes. Cookies.py simply prints all of returned Recipe objects; however, the ```recipe_parser.py``` script (which does the heavy lifting) is easy to integrate with other projects.

Tagging Training Data
=====================
Training files are recipes that have the recipe's "parts of speech" appended to each word. This information is used to train the parser. See tagged_recipes/README.md for a detailed explanation of the tagging format.

Recipe Comparison and Graphing
=============================
The Recipe class includes a recipe comparison method. This calculates the difference between two recipes by comparing the relative ratios of ingredients that the recipes share. For example, two identical recipes will have a comparison score of 1.0; two recipes that share no ingredients will have a comparison score of 0.0.

The script ```graph.py``` parses a series of recipes, then uses the gexf library to create an undirected graph representing the recipes. Each node is a recipe, while each weighted edge represents the similarity between those two recipes. The gexf file can be imported into Gephi to generate a graph of the recipe space. See cooks_3000_recipes.png for an example. Large nodes are nodes with multiple duplicates. Nodes which are very close are similar recipes, while nodes that are far away are more different.

Recipe Scraper
==============
The ```html.py``` script uses BeautifulSoup used to scrape recipes from the internet. (Currently, it points at cooks.com.) It then places each recipe in a text file in the specified folder. To use, in the python command line type:
```
import html as html
html.download_from_sites("target_directory")
```
target_directory must currently not exist.

Known Issues and Further Work
=============================
Due to the limited training data, the parser sometimes fails to parse novel ingredients. When viewing the parsed results in Gephi, these poorly parsed recipes will usually show up as an extreme outlier. Further work is needed to help the parser clean up input (such as making sure "eggs" is equal to "egg"), improve the training data and improve recognition of untrained ingredients.
