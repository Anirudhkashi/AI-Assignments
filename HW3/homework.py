import copy


def has_not(var):
	if "~" in var:
		return True
	return False


def is_variable(val):
	if val[0] == val[0].lower():
		return True
	return False


def get_opposite_predicate(predicate):
	if has_not(predicate):
		predicate = predicate.replace("~", "")
	else:
		predicate = "~"+predicate
	return predicate


def variables_compatible(kb_variables, query_variables):
	kb_variable_substitutions = {}
	query_variable_substitutions = {}
	for i in range(len(kb_variables)):
		bool1 = is_variable(kb_variables[i])
		bool2 = is_variable(query_variables[i])
		# Both are not variables, then they should be equal
		if not bool1 and not bool2:
			if kb_variables[i] != query_variables[i]:
				return False, {}, {}
		# KB is variable, but not in query, then substitute in KB sentence
		elif bool1 and not bool2:
			if kb_variables[i] not in kb_variable_substitutions.keys():
				kb_variable_substitutions[kb_variables[i]] = query_variables[i]
		# KB is an Object, but in query, it is a variable, then substitution should happen everywhere in the query
		elif not bool1 and bool2:
			if query_variables[i] not in query_variable_substitutions.keys():
				query_variable_substitutions[query_variables[i]] = kb_variables[i]
		# Both are variables, then substitute those variable names
		else:
			if kb_variables[i] not in kb_variable_substitutions.keys():
				kb_variable_substitutions[kb_variables[i]] = query_variables[i]
			# if kb_variables[i] != query_variables[i]:
			# 	return False, kb_variable_substitutions, query_variable_substitutions

	return True, kb_variable_substitutions, query_variable_substitutions


class VariableException(Exception):
	def __init__(self, message):
		print message


class KnowledgeBase:
	def __init__(self):
		self.kb = {}

	def substitution(self, variable_substitutions, sentence_list):
		for i in range(len(sentence_list)):
			variables = sentence_list[i][1].split(",")
			for j in range(len(variables)):
				if is_variable(variables[j]) and variables[j] in variable_substitutions.keys():
					variables[j] = variable_substitutions[variables[j]]
			sentence_list[i] = (sentence_list[i][0], ",".join(variables))
		return sentence_list

	def ask(self, queries):
		done_queries = []
		return self.resolution(queries, done_queries, False)

	def perform_substitutions(self, kb_substitutions,
							query_substitutions, queries, query_variables, sentence_list):

		for i in range(len(sentence_list)):
			v_s = sentence_list[i][1].split(",")
			for j in range(len(v_s)):
				if is_variable(v_s[j]) and v_s[j] in kb_substitutions.keys():
					v_s[j] = kb_substitutions[v_s[j]]
			sentence_list[i] = (sentence_list[i][0], ",".join(v_s))

		for i in range(len(queries)):
			v_s = queries[i][1].split(",")
			for j in range(len(v_s)):
				if is_variable(v_s[j]) and v_s[j] in query_substitutions.keys():
					v_s[j] = query_substitutions[v_s[j]]
			queries[i] = (queries[i][0], ",".join(v_s))

		for j in range(len(query_variables)):
			if is_variable(query_variables[j]) and query_variables[j] in query_substitutions.keys():
				query_variables[j] = query_substitutions[query_variables[j]]

		return queries, query_variables, sentence_list

	def resolution(self, queries, done_queries, final_result):

		if len(queries) == 0:
			return True

		query = queries[0]
		if query in done_queries:
			del(queries[0])
			return False

		done_queries.append(query)
		del(queries[0])
		query_predicate = query[0]
		query_predicate_opposite = get_opposite_predicate(query_predicate)
		query_variables = query[1].split(",")
		query_variables_len = len(query_variables)
		if query_predicate_opposite in self.kb.keys():
			if query_variables_len in self.kb[query_predicate_opposite]:
				all_sentence_list = copy.deepcopy(self.kb[query_predicate_opposite][query_variables_len])
				for sentence_list in all_sentence_list:
					query_variables = query[1].split(",")
					result, kb_substitutions, query_substitutions = variables_compatible(
						sentence_list[0][1].split(","), query_variables)
					if not result:
						continue
					else:
						queries, query_variables, sentence_list = self.perform_substitutions(
							kb_substitutions, query_substitutions, queries, query_variables, sentence_list)

						to_remove = (query_predicate_opposite, ",".join(query_variables))
						if to_remove not in sentence_list:
							return False
						sentence_list.remove(to_remove)
						queries.extend(x for x in sentence_list if x not in queries)
						final_result = final_result or self.resolution(queries, done_queries, final_result)

						if final_result:
							return True
						else:
							queries = []

			else:
				return False
		return False

	def tell(self, sentence_list):
		for predicate, variables in sentence_list:
			temp_list = copy.deepcopy(sentence_list)
			temp_list.remove((predicate, variables))
			temp_list.insert(0, (predicate, variables))
			num_variables = len(variables.split(","))

			if predicate in self.kb.keys():
				if num_variables in self.kb[predicate].keys():
					self.kb[predicate][num_variables].append(temp_list)
				else:
					self.kb[predicate][num_variables] = [temp_list]
			else:
				self.kb[predicate] = dict({num_variables: [temp_list]})

	def pretty_dump(self, indent=3):
		for key, value in self.kb.items():
			print('\t' * indent + str(key))
			print('\t' * (indent + 1) + str(value))


class Parser:
	def __init__(self, file_name):
		self.file_name = file_name

	def read_input(self):
		sentences = []
		queries = []
		with open(self.file_name, "r") as f:
			inp = f.read().strip().split("\n")
			num_queries = int(inp[0])
			for i in range(1, num_queries + 1):
				queries.append(inp[i])

			for i in range(num_queries+2, len(inp)):
				sentences.append(inp[i])

		return sentences, queries

	def normalise(self, variables, num):
		variables = variables.split(",")
		for i in range(len(variables)):
			# Only normalise variables
			if is_variable(variables[i]):
				# Change variables to name + _ + sentence number
				variables[i] = variables[i] + "_" + str(num)
		return ",".join(variables)


	def parse(self, sentence, num):
		sentence = sentence.replace(" ", "")  # Replace spaces
		sentence = sentence.replace(")", "")  # Remove unrequired quotes
		sentence = sentence.split("|")
		sentence_tuple = []  # To store tuples [(Predicate, variables), .....]
		for t in sentence:
			p, v = t.split("(")
			v = self.normalise(v, num)
			sentence_tuple.append((p, v))
		return sentence_tuple


def main():
	parser = Parser("input.txt")
	sentences, queries = parser.read_input()
	kb = KnowledgeBase()
	i = 0
	for sen in sentences:
		t = parser.parse(sen, i)
		kb.tell(t)
		i += 1

	with open("output.txt", "w") as f:
		for query in queries:
			t = parser.parse(query, 10001)
			for i in range(len(t)):
				t[i] = (get_opposite_predicate(t[i][0]), t[i][1])
			result = kb.ask(t)
			print result
			f.write(str(result).upper() + "\n")



if __name__ == "__main__":
	main()