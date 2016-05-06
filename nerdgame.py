import random
from operator import sub, mul, add, truediv
from math import log
from itertools import permutations
permute = permutations

def root(a, b):
	#prevents complex numbers or raising to negative powers
	if b % 2 and a < 0:
		raise ValueError()
	if b < 0:
		raise ValueError()
	return pow(a, 1 / b)
def pows(a, b):
	#prevents overflow
	if b >= 7:
		raise ValueError()
	return pow(a, b)
OPERATIONS = [sub, mul, add, truediv, pows, log, root]

def check(cards, total):
	""" 
	Note: no error checking implemented yet
	A checker function that takes in the cards and sum total in order to see if it
	is possible to create an expression that evaluates to the number using operations
	in OPERATIONS.

	Parameters:
	cards - a list of length two to four of integers from 1 to 13 (inclusive) representing four
	playing cards to be used to create the total number through basic mathematical operations
	total - an integer from 3 to 60 (inclusive) representing the goal number to achieve

	Returns a tuple of (boolean, list of strings) where the boolean is whether or not it can be achieved 
	and the list of strings is the ways to achieve it.
	"""
	if len(cards) == 2:
		found_solution = False
		solutions = []
		for op in OPERATIONS:
			try:
				ans = op(cards[0], cards[1])
				if type(ans) == complex:
					raise ValueError()
				if int(ans) == ans:
					ans = int(ans)
				if ans == total:
					solution_string = str(cards[0]) + " " + op.__name__ + " " + str(cards[1]) + \
					" = " + str(ans) + ", the total!"
					found_solution = True
					solutions.append(solution_string)
			except (ZeroDivisionError, RuntimeError, ValueError, OverflowError):
				continue
		if not found_solution:
			return False, []
		return True, solutions
	elif len(cards) == 3:
		found_solution = False
		solutions = []
		for op in OPERATIONS:
			try:
				res = op(cards[0], cards[1])
				if type(res) == complex:
					raise ValueError()
				if int(res) == res:
					res = int(res)
				result_of_check = check([res, cards[2]], total)
				if result_of_check[0]:
					for solution_string in result_of_check[1]:
						solution_string = str(cards[0]) + " " + op.__name__ + " " + str(cards[1]) + \
						" = " + str(res) + ", " + solution_string
						found_solution = True
						solutions.append(solution_string)
			except (ZeroDivisionError, RuntimeError, ValueError, OverflowError):
				continue
		for op in OPERATIONS:
			try:
				res = op(cards[1], cards[2])
				if type(res) == complex:
					raise ValueError()
				if int(res) == res:
					res = int(res)
				result_of_check = check([cards[0], res], total)
				if result_of_check[0]:
					for solution_string in result_of_check[1]:
						solution_string = str(cards[1]) + " " + op.__name__ + " " + str(cards[2]) + \
						" = " + str(res) + ", " + solution_string
						found_solution = True
						solutions.append(solution_string)
			except (ZeroDivisionError, RuntimeError, ValueError, OverflowError):
				continue
		if not found_solution:
			return False, []
		return True, solutions
	elif len(cards) == 4:
		found_solution = False
		solutions = []
		for op in OPERATIONS:
			try:
				res = op(cards[0], cards[1])
				if type(res) == complex:
					raise ValueError()
				if int(res) == res:
					res = int(res)
				result_of_check = check([res, cards[2], cards[3]], total)
				if result_of_check[0]:
					for solution_string in result_of_check[1]:
						solution_string = str(cards[0]) + " " + op.__name__ + " " + str(cards[1]) + \
						" = " + str(res) + ", " + solution_string
						found_solution = True
						solutions.append(solution_string)
			except (ZeroDivisionError, RuntimeError, ValueError, OverflowError):
				continue
		for op in OPERATIONS:
			try:
				res = op(cards[1], cards[2])
				if int(res) == res:
					res = int(res)
				if type(res) == complex:
					raise ValueError()
				result_of_check = check([cards[0], res, cards[3]], total)
				if result_of_check[0]:
					for solution_string in result_of_check[1]:
						solution_string = str(cards[1]) + " " + op.__name__ + " " + str(cards[2]) + \
						" = " + str(res) + ", " + solution_string
						found_solution = True
						solutions.append(solution_string)
			except (ZeroDivisionError, RuntimeError, ValueError, OverflowError):
				continue
		for op in OPERATIONS:
			try:
				res = op(cards[2], cards[3])
				if int(res) == res:
					res = int(res)
				if type(res) == complex:
					raise ValueError()
				result_of_check = check([cards[0], cards[1], res], total)
				if result_of_check[0]:
					for solution_string in result_of_check[1]:
						solution_string = str(cards[2]) + " " + op.__name__ + " " + str(cards[3]) + \
						" = " + str(res) + ", " + solution_string
						found_solution = True
						solutions.append(solution_string)
			except (ZeroDivisionError, RuntimeError, ValueError, OverflowError):
				continue
		if not found_solution:
			return False, []
		return True, solutions
	print("Error - invalid number of cards")
	raise ValueError


### Start of the main function ###




function_mode = input('Type "Game" for game or "Check" for only the checker function\n')

if function_mode == "Game":
	deck = list(range(1,14)) * 4
	random.shuffle(deck)
	discard = []
	print("Game Start!")
	inp = "next"
	while inp == "next":
		dice = [random.randint(1, 20),  random.randint(1, 20),  random.randint(1, 20)]
		cards = []
		if not deck:
			random.shuffle(discard)
			deck = discard
			discard = []
		for i in range(4):
			cards.append(deck.pop())
		discard += cards
		found_solution = False
		permutations_of_cards = list(permute(cards))
		total = sum(dice)
		for card_instance in permutations_of_cards:
			found_solution, solutions_list = check(card_instance, total)
			if found_solution:
				break
		if not found_solution:
			print("Cards:", cards, "Sum:", sum(dice), \
				"\nImpossible combination - 20$ if you find one, 1$ for me if you don't :P")
			inp = "next"
			continue
		else:
			print("Cards:", cards, "Dice:", dice, "Sum:", sum(dice))
			inp = input('Type "show" for solution or "next" to play again!\n')
			if inp == "show":
				print("Number of Solutions: ", len(solutions_list))
				for solution in solutions_list:
					print(solution)
				inp = input('Type "next" to play again!\n')
elif function_mode == "Check":
	while True:
		cards = [int(i) for i in input("Please input the card values separated by spaces\n").split(" ")]
		total = int(input("Please input the sum of the dice values\n"))
		permutations_of_cards = list(permute(cards))
		found_solution = False
		for card_instance in permutations_of_cards:
			found_solution, solutions_list = check(card_instance, total)
			if found_solution:
				print("IT IS POSSIBLE, SCRUB")
				if input("If you would like to see the solution, type \"show\"\n") == "show":
					print("Number of Solutions: ", len(solutions_list))
					for solution in solutions_list:
						print(solution)
				break
		if not found_solution:
			print("It's okay. It wasn't possible.")
elif function_mode == "Alan":
	number_of_solutions = {}
	hardmode = []
	k = 0
	solvable = 0
	numtrials = int(input("number of trials?\n"))
	deck = list(range(1,14)) * 4
	random.shuffle(deck)
	discard = []
	while k < numtrials:
		if k % 100 == 0:
			print(k)
		dice = random.randint(1, 20) + random.randint(1, 20) + random.randint(1, 20)
		cards = []
		if not deck:
			random.shuffle(discard)
			deck = discard
			discard = []
		for i in range(4):
			cards.append(deck.pop())
		discard += cards
		permutations_of_cards = list(permute(cards))
		num_solutions = 0
		all_solutions = []
		for card_instance in permutations_of_cards:
			result_of_check = check(card_instance, dice)
			if result_of_check[0]:
				found_solution = True
				num_solutions += len(result_of_check[1])
				all_solutions += result_of_check[1]
		if num_solutions in number_of_solutions:
			number_of_solutions[num_solutions] += 1
		else:
			number_of_solutions[num_solutions] = 1
		if len(all_solutions) == 1:
				hardmode.append((cards, dice))
		if num_solutions != 0:
			solvable += 1
		k += 1
	print(solvable / k)
	print(number_of_solutions)
	print(hardmode)
	# print("Lots of solutions? Incorrect implementation but oh well")
	# for lots in cool:
	# 	print("NEW NEW NEW")
	# 	print(lots)
elif function_mode == "Hard":
	k = int(input("Max number of solutions?\n"))
	stored_sol = None
	while k > 5:
		print("Too many solutions for hard mode, we'll go with 2")
		k = 2
	forestcanthandle = int(input("Range? If 0, uses standard 3 dice\n"))
	deck = list(range(1,14)) * 4
	random.shuffle(deck)
	discard = []
	print("Game Start!")
	inp = "next"
	while inp == "next":
		if forestcanthandle:
			dice = random.randint(1, forestcanthandle)
		else:
			dice = random.randint(1, 20) + random.randint(1, 20) + random.randint(1, 20)
		cards = []
		if not deck:
			random.shuffle(discard)
			deck = discard
			discard = []
		for i in range(4):
			cards.append(deck.pop())
		discard += cards
		permutations_of_cards = list(permute(cards))
		num_solutions = 0
		all_solutions = []
		too_easy = False
		for card_instance in permutations_of_cards:
			result_of_check = check(card_instance, dice)
			if result_of_check[0]:
				found_solution = True
				num_solutions += len(result_of_check[1])
				all_solutions += result_of_check[1]
				if num_solutions > k:
					too_easy = True
					break
		if too_easy or num_solutions == 0:
		# or "2 pows" in all_solutions or "pows 2" in all_solutions \
		# or "2.0 pows" in all_solutions or "pows 2.0" in all_solutions:
			continue
		else:
			if stored_sol != None:
				inp = input()
				if inp == "show":
					for solution in stored_sol:
						print(solution)
			print("Cards:", cards, "Dice:", dice)
			print('Type "show" for solution or "next" to play again!')
			stored_sol = set(all_solutions)
			inp = "next"

