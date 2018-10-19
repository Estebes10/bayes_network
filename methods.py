import itertools
import json
import decimal
import math
from node import *

def add_parents(list_nodes, probabilities_list):
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

def print_node_values(list_nodes):
    for node in list_nodes:
        print("Node attributes")
        print("Name = "+node.name)
        print("Values")
        print(node.table)
        print("Is parent? ")
        print(node.parents)

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
			find_node = get_node(parent, list_nodes)
			get_ancestors(find_node, list_nodes, ancestors)
	else:
		if node.name not in ancestors:
			ancestors.append(node.name)

def resolve_queries(query, node_list): # change probability to conditional probability form
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

def conditional_probability(numerator, denominator, node_list):
	hidden_numerator = []
	numerators = numerator.split(',')
	for element in numerators:

		if "+" in element:
			aux = element.replace('+', "")
		elif "-" in element:
			aux = element.replace('-', "")

		node = get_node(aux, node_list)
		ancestors = []
		if node.parents:
			get_ancestors(node, node_list, ancestors)

		for ancestor in ancestors:
			if not "+" + ancestor in numerators and not "-" + ancestor in numerators and not ancestor in hidden_numerator:
				hidden_numerator.append(ancestor)
	if hidden_numerator:
		permu_numer = create_permutations(hidden_numerator)
		number_enumerators = append_values(numerators, permu_numer)
	else:
		number_enumerators = numerators

	value_numerators = chain_rule(number_enumerators, node_list)
	if denominator:
		hidden_denominator = []
		denominators = denominator.split(',')
		for den in denominators:

			if "+" in den:
				aux = den.replace('+', "")
			elif "-" in den:
				aux = den.replace('-', "")
			node = get_node(aux, node_list)
			ancestors = []
			if node.parents:
				get_ancestors(node, node_list, ancestors)

			for ancestor in ancestors:
				if not "+" + ancestor in denominators and not "-" + ancestor in denominators and not ancestor in hidden_denominator:
					hidden_denominator.append(ancestor)

		if hidden_denominator:
			permu_deno = create_permutations(hidden_denominator)
			number_denominators = append_values(denominators, permu_deno)
		else:
			number_denominators = denominators

		value_denominator = chain_rule(number_denominators, node_list)
		# Add up all permutations
		if(value_denominator == 0.0):
			value_denominator = 1.0
	else: # if there is not denominators
		value_denominator = 1.0

	result = round(value_numerators / value_denominator, 7)
	print(result)

def save_parents_array(list_nodes, node, probabilities, list, val, element = '3'):
	var = node.replace("+", "")
	name = var.replace("-", "")
	find_node = get_node(name, list_nodes)

	if find_node.parents:
		posibilities = itertools.permutations(range(0, len(find_node.parents)))

		for p in posibilities:
			parents_array = []
			for l in p:
				if val == 1:
					if "+" + find_node.parents[l] in element:
						parents_array.append("+"+find_node.parents[l])

					elif "-" + find_node.parents[l] in element:
						parents_array.append("-"+find_node.parents[l])
				else:
					if "+" + find_node.parents[l] in list:
						parents_array.append("+"+find_node.parents[l])
					elif "-" + find_node.parents[l] in list:
						parents_array.append("-"+find_node.parents[l])
			string = node+"|"

			for i in range(len(parents_array)):
				string += parents_array[i]
				if i < len(parents_array) - 1:
					string += ","

			if string in find_node.table:
				value = find_node.table[string]
				probabilities.append(value)
	else:
		value = find_node.table[node]
		probabilities.append(value)

def chain_rule(list_combinations, node_list):
	probability = 0.0
	flag = True

	multiplier = 1.0
	proba = []
	probabilities = []
	for element in list_combinations:
		probabilities = []
		if type(element) is list:
			for item in element:
				save_parents_array(node_list, item, probabilities, list_combinations, 1, element)
			proba.append(probabilities)
		else:
			if element:
				save_parents_array(node_list, element, probabilities, list_combinations, 2)
				proba.append(probabilities[0])

	multiplier = 1.0
	for element in proba: # calculate probability for each node
		if type(element) is list:
			flag = True
			multiplier = 1.0
			for item in element:
				multiplier *= item
			probability += multiplier
		else:
			flag = False
			multiplier *= element
	if flag:
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

def create_permutations(variables):
	combinations = []
	positives = copy.deepcopy(variables)
	negatives = copy.deepcopy(variables)
	combination_list = []
	number = 0
	flag = True
	for i in range(len(positives)):
		positives[i] = "+" + positives[i]
	for i in range(len(negatives)):
		negatives[i] = "-" + negatives[i]

	for i in range(2**(len(variables) - 1)):
		number = math.ceil(math.sqrt(i))
		if number == 0:
			number = 1
		combination_list = []
		for j in range(len(variables)):

			if j == (number - 1):
				if flag:
					combination_list.append(positives[j])
					flag = False
				else:
					combination_list.append(negatives[j])
					flag = True
			else:
				combination_list.append(positives[j])

		combinations.append(combination_list)
	reverse_combinations = reverse(combinations)
	for element in reverse_combinations:
		combinations.append(element)

	return combinations

def append_values(given, combinations):
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
