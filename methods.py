import itertools
import json
import decimal
import math
from node import *

def set_parents(list_nodes, probabilities_list):
	for node in list_nodes:
		node.addParentandTable(probabilities_list)
		node.completeTable()

def create_nodes(node_names): # create nodes with given names
	nodes_list = []
	for var in node_names.split(','):
		nodes_list.append(Node(var, [], {}))

	return nodes_list

def parse_probabilities(probabilities_list):
	statement_list = {}
	for statement in probabilities_list:
		variables = statement.split('=') # separate probability value from params

		statement_list[variables[0]] = float(variables[1])

	return 	statement_list

def get_node(name, list_nodes): # find speciic Node using param Names
	for element in list_nodes:
		if element.name == name:
			return element
	return False

def get_ancestors(node, list_nodes, ancestors):
	if node.parents:
		for parent in node.parents:
			if parent not in ancestors:
				ancestors.append(parent)
			newnode = get_node(parent, list_nodes)
			get_ancestors(newnode, list_nodes, ancestors)
	else:
		if node.name not in ancestors:
			ancestors.append(node.name)

def parse_query(query, node_list): # change probability to conditional probability form
	for params in query:
		numerator = ""
		denominator = ""
		var = params.split("|")
		if len(var) == 2:
			numerator = var[0] + ',' + var[1]
			denominator = var[1]
		elif len(var) == 1:
			numerator = var[0]

		conditional_probability(numerator, denominator, node_list)
	return 0

def conditional_probability(numerator, denominator, node_list):
	numeratorhidden = []
	numeratorgiven = numerator.split(',')
	for element in numeratorgiven:

		if "+" in element:
			auxelement = element.replace('+', "")
		elif "-" in element:
			auxelement = element.replace('-', "")
		node = get_node(auxelement, node_list)

		ancestors = []
		if node.parents:
			get_ancestors(node, node_list, ancestors)

		for ancestor in ancestors:

			if not "+" + ancestor in numeratorgiven and not "-" + ancestor in numeratorgiven and not ancestor in numeratorhidden:
				numeratorhidden.append(ancestor)
	if numeratorhidden:
		permitationsnumerator = create_permutations(numeratorhidden)
		enumeratorNUvariables = appendgivenandhidden(numeratorgiven, permitationsnumerator)
	else:
		enumeratorNUvariables = numeratorgiven
	numeratorvalue = chain_rule(enumeratorNUvariables, node_list)

	if denominator:
		denominatorhidden = []
		denominatorgiven = denominator.split(',')
		for element in denominatorgiven:

			if "+" in element:
				auxelement = element.replace('+', "")
			elif "-" in element:
				auxelement = element.replace('-', "")
			node = get_node(auxelement, node_list)
			ancestors = []
			if node.parents:
				get_ancestors(node, node_list, ancestors)

			for ancestor in ancestors:

				if not "+" + ancestor in denominatorgiven and not "-" + ancestor in denominatorgiven and not ancestor in denominatorhidden:
					denominatorhidden.append(ancestor)

		if denominatorhidden:
			permitationsdenominator = create_permutations(denominatorhidden)
			enumeratorDEvariables = appendgivenandhidden(denominatorgiven, permitationsdenominator)
		else:
			enumeratorDEvariables = denominatorgiven

		denominatorvalue = chain_rule(enumeratorDEvariables, node_list)
	# Add up all permutations
		if(denominatorvalue == 0.0):
			denominatorvalue = 1.0
	else:
		denominatorvalue = 1.0

	result = round(numeratorvalue / denominatorvalue, 7)
	print(result)
	return 0

def chain_rule(list_combinations, node_list):
	probability = 0.0
	bandera = True

	multiplier = 1.0
	proba = []
	probabilities = []
	for element in list_combinations:
		probabilities = []
		if type(element) is list:
			for item in element:
				var = item.replace("+", "")
				name = var.replace("-", "")
				newnode = get_node(name, node_list)

				if newnode.parents:
					possible_movements = itertools.permutations(range(0, len(newnode.parents)))
					for p in possible_movements:
						parents_array = []
						for l in p:
							if "+" + newnode.parents[l] in element:
								parents_array.append("+"+newnode.parents[l])

							elif "-" + newnode.parents[l] in element:
								parents_array.append("-"+newnode.parents[l])
						string = item+"|"

						for i in range(len(parents_array)):
							string += parents_array[i]
							if i < len(parents_array) - 1:
								string += ","
						if string in newnode.table:
							value = newnode.table[string]
							probabilities.append(value)

				else:
					value = newnode.table[item]
					probabilities.append(value)
			proba.append(probabilities)
		else:
			if element:
				var = element.replace("+", "")
				name = var.replace("-", "")
				newnode = get_node(name, node_list)

				if newnode.parents:
					possible_movements = itertools.permutations(range(0, len(newnode.parents)))
					for p in possible_movements:
						parents_array = []
						for l in p:

							if "+" + newnode.parents[l] in list_combinations:
								parents_array.append("+"+newnode.parents[l])
							elif "-" + newnode.parents[l] in list_combinations:
								parents_array.append("-"+newnode.parents[l])
						string = element+"|"

						for i in range(len(parents_array)):
							string += parents_array[i]
							if i < len(parents_array) - 1:
								string += ","
						#print(string)
						if string in newnode.table:
							value = newnode.table[string]
							probabilities.append(value)

				else:
					value = newnode.table[element]
					probabilities.append(value)
				proba.append(probabilities[0])
	#print(proba)
	multiplier = 1.0
	for element in proba:
		if type(element) is list:
			bandera = True
			multiplier = 1.0
			for item in element:
				multiplier *= item
			probability += multiplier
		else:
			bandera = False
			multiplier *= element
		#calculate probabilities for each node in the permutation (multiplication)
		#consider all the parents of each node
		#check probability table to calculate each node's probability
	if bandera:
		return probability

	else:
		return multiplier

def reverse(combinations): # reverse combinations

	rev = []
	aux_list = []
	for element in combinations:
		aux_list =[]
		for item in element:
			if "+" in item:
				aux_list.append(item.replace("+", "-"))
			elif "-" in item:
				aux_list.append(item.replace("-", "+"))
		rev.append(aux_list)
	return rev

def create_permutations(hiddenvariables):
	combinations = []
	allpositive = copy.deepcopy(hiddenvariables)
	allnegative = copy.deepcopy(hiddenvariables)
	combination_list = []
	number = 0
	flag = True
	for i in range(len(allpositive)):
		allpositive[i] = "+" + allpositive[i]
	for i in range(len(allnegative)):
		allnegative[i] = "-" + allnegative[i]

	for i in range(2**(len(hiddenvariables) - 1)):
		number = math.ceil(math.sqrt(i))
		if number == 0:
			number = 1
		combination_list = []
		for j in range(len(hiddenvariables)):

			if j == number - 1:
				if flag:
					combination_list.append(allpositive[j])
					flag = False
				else:
					combination_list.append(allnegative[j])
					flag = True
			else:
				combination_list.append(allpositive[j])

		combinations.append(combination_list)
	reverse_combinations = reverse(combinations)
	for element in reverse_combinations:
		combinations.append(element)

	return combinations

def appendgivenandhidden(given, combinations):
	result = []
	aux = []
	for i in range(len(combinations)):
		aux = []
		for element in given:

			aux.append(element)
		for element in combinations[i]:
			aux.append(element)
		result.append(aux)
	return result