import node

sep = "|||"
dep_table = dict()
desc_table = dict()
nodes = list()


# NOTE: coroutine
def sink():
	global dep_table
	global desc_table
	while True:
		data = (yield)
		n = node.Node(list(), list(), data["text"])
		for dep_key in data["associations"]["dependencies"]:
			x = dep_table.get(dep_key, list())
			x.append(n)
			dep_table[dep_key] = x
		for desc_key in data["associations"]["descriptions"]:
			x = desc_table.get(desc_key, list())
			x.append(n)
			desc_table[desc_key] = x
		nodes.append(n)


# NOTE: coroutine
def parse_cmd():
	declared_entities = list()
	associations = None
	while True:
		assoc, line = (yield associations)
		line = line[3:]
		line = line.strip(" ")
		if line.startswith("DEP"):  # dependency on known entity
			cmd = line[3:].strip(": ")
			if cmd not in declared_entities:
				raise Exception(f"entity `{cmd}` not declared before use as a "
								f"dependency")
			assoc["dependencies"].append(cmd)
			associations = assoc
		elif line.startswith("DESC"):  # description of known entity
			cmd = line[4:].strip(": ")
			if cmd not in declared_entities:
				raise Exception(f"entity `{cmd}` not declared before use as a "
								f"description")
			assoc["descriptions"].append(cmd)
			associations = assoc
		elif line.startswith("DEC"):  # declarations of an entity
			cmd = line[3:].strip(": ")
			declared_entities.append(cmd)
			associations = assoc
		elif line.startswith("OPEN"):
			raise Exception("Not yet implemented")
		elif line.startswith("CLOSE"):
			raise Exception("Not yet implemented")
		else:
			raise Exception(f"unknown command: {line}")


# NOTE: coroutine
def chunker(parser, sink):
	text = list()
	associations = {"dependencies": list(), "descriptions": list()}
	count = 0
	while True:
		line = (yield)
		if line is None:
			sink.send({"text": text, "associations": associations})
		elif not text and line.startswith(sep):
			associations = parser.send((associations, line))
		elif line.startswith(sep):
			sink.send({
				"text": text,
				"associations": associations,
				"position": count
			})
			count += 1
			text = list()
			associations = {"dependencies": list(), "descriptions": list()}
			associations = parser.send((associations, line))
		else:
			text.append(line)


# NOTE: coroutine
def splitlines(string):
	group = ""
	for x in string:
		if x == "\n":
			yield group
			group = ""
		else:
			group += x
	yield group


# NOTE: coroutine
def read_annotated_file(rel_path: str, chunker):
	with open(rel_path, "r") as f:
		contents = f.read()
		for line in splitlines(contents):
			chunker.send(line)
		chunker.send(None)


def write_final_file(rel_path: str, ordering, melzi_data=True):
	with open(rel_path, "w+") as f:
		if melzi_data:
			for entity in {**desc_table, **dep_table}:
				f.write(f"||| DEC {entity}\n")
			for desc in desc_table:
				f.write(f"||| DESC {desc}\n")
			for dep in dep_table:
				if dep not in desc_table:
					f.write(f"||| DEP {dep}\n")
		for node in ordering:
			for line in node.content:
				f.write(line)
