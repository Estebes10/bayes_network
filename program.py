# -*- coding: utf-8 -*-

# =============================================================================
# Juan Carlos Estebes González
# Salomón Olivera Abud
# =============================================================================
from methods import *

def bayes(nodes, probabilities, queries):
	nodes_list = create_nodes(nodes)
	probabilities_list = parse_probabilities(probabilities)
	add_parents(nodes_list, probabilities_list)
	resolve_queries(queries, nodes_list)

def main():
	nodes_names = input()
	number_p = int(input())

	probabilities = []
	for x in range(0, number_p):
		probabilities.append(input())

	number_q = int(input())
	queries = []

	for x in range(0, number_q):
		queries.append(input())

	bayes(nodes_names, probabilities, queries)

if __name__ == "__main__":
	main()
