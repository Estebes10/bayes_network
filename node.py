import copy

class Node:

	def __init__(self, name, parents, table):
		self.name = name
		self.parents = parents
		self.table = table

	def getParents(self):
		return self.parents

	def addParentandTable(self, parentTable):
		self.table = parentTable

	def addParentandTable(self, dictionary):

		#get keys from dictionary
		for k in dictionary.keys(): # get keys from
			#replace '+' and '-' sings from string
			key = copy.deepcopy(k);
			k = k.replace("+", "")
			k = k.replace("-", "")
			var = k.split('|') # check if there are more than one params

			if self.name == var[0]: # find Node using param Name
				self.table[key] = dictionary[key] # add value to table
				#check for parents in the condition
				if len(var) == 2: # parent(s)|child
					for parent in var[1].split(","): # get parent names
						if not parent in self.parents: # verify uniq parent values
							self.parents.append(parent)
				elif len(var) == 1: # root node
					if self.name == var[0]:
						self.parents = None

	def completeTable(self):
		# save the opposite value of the given param
		temp = copy.deepcopy(self.table) # temp table
		for k in self.table:
			if k[0] == "+":
				key = k.replace("+", "-", 1)
				if not key in self.table:
					temp[key] = round(1.0 - self.table[k], 4)
			elif k[0] == "-":
				key = k.replace("-", "+", 1)

				if not key in self.table:
					temp[key] = round(1.0 - self.table[k], 4)

		self.table = temp
