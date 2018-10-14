class Node:

	def __init__(self, name, parents, table):
		self.name = name
		self.parents = parents
		self.table = table

	def getParents(self):
		return self.parents

	def addParentandTable(self, parentTable):
		self.table = parentTable
