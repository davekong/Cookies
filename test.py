from recipe import Recipe
from ingredient import Ingredient, Unit
import copy as copy
# Test two recipes that are identical

flour = Ingredient(quantity=1, food="flour", unit=Unit.CUP)
choc_chips = Ingredient(quantity=2, food="chocolate chips", unit=Unit.ITEM)
sugar = Ingredient(quantity=3, food="sugar", unit=Unit.TBSP)

r1 = Recipe(ingredients=[flour, choc_chips, sugar], baking_time=15, temperature=350)

assert r1.compare(r1) == 1.0, "Identical recipe compared to %.2f" % r1.compare(r1)

# Two recipes that are scales of each other

r2 = Recipe(baking_time=15, temperature=350)
for ing in [flour, choc_chips, sugar]:
	newing = copy.deepcopy(ing)
	newing.quantity = ing.quantity * 2
	r2.add_ingredient(newing)

assert r1.compare(r2) == 1.0, "Scaled recipes compared to %.2f" % r1.compare(r2)

# Two recipes that are completely different (no shared ingredients)

salt = Ingredient(quantity=5, food="salt", unit=Unit.CUP)
butter = Ingredient(quantity=2, food="butter", unit=Unit.TBSP)
pud_mix = Ingredient(quantity=1, food="vanilla pudding mix", unit=Unit.ITEM)

r3 = Recipe(ingredients=[salt, butter, pud_mix], baking_time=10, temperature=400)

assert r1.compare(r3) == 0.0, "Completely different recipes compared to %.2f" % r1.compare(r3)

# Two recipes that share ingredients but have randomly different amounts

flour2 = copy.deepcopy(flour)
choc_chips2 = copy.deepcopy(choc_chips)
sugar2 = copy.deepcopy(sugar)

flour2.quantity = 7
choc_chips2.quantity = 8
sugar2.quantity = 9

r4 = Recipe(ingredients=[flour2, sugar2, choc_chips2])
r5 = Recipe(ingredients=[flour2, butter, choc_chips2])
r6 = Recipe(ingredients=[salt, butter, choc_chips2])

cmp1 = r1.compare(r4)
cmp2 = r1.compare(r5)
cmp3 = r1.compare(r6)

assert cmp1 > cmp2, "Recipe with same ingredients but different amounts should be more similar. %.2f > %.2f" % (cmp1, cmp2)
assert cmp2 > cmp3, "Recipe with two same ingredients should be more similar than recipe with one same ingredient. %.2f > %.2f" % (cmp2, cmp3)

# Comparing r1 to r2 = comparing r2 to r1

assert r1.compare(r4) == r4.compare(r1), "Comprison should work either way"