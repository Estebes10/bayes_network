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
