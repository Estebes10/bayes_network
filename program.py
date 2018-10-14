# -*- coding: utf-8 -*-

# =============================================================================
# Juan Carlos Estebes González
# Salomón Olivera Abud
# =============================================================================

def bayes(nodes, probabilities, queries):
	return 0

if __name__ == "__main__":

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
