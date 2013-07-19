def commandType(com):
	if com[0] == '@':
		return "A_COMMAND"
	elif com[0] == '(':
		return "L_COMMAND"
	else: 
		return "C_COMMAND"

class Parser:

	def __init__(self, filename):
		"Opens the input file and prepares it for parsing."
		
		f = open(filename)
		self.commands = f.readlines()
		f.close()
		# Remove newline char from the input string
		self.commands = [com.strip() for com in self.commands]
		self.commands = self._trimLines()

	def _trimLines(self):
		tempCommands = []
		for i in range(0, len(self.commands)):
			if self.commands[i] != '' and self.commands[i][0:2] != '//':
				tempCommands.append(self.commands[i])
		return tempCommands

	def symbol(self, comNum):
		com = self.commands[comNum]
		comType = commandType(com)
		if comType == "C_COMMAND":
			return "INVALID COMMAND TYPE"
		elif comType == "A_COMMAND":
			return com[1:]
		elif comType == "L_COMMAND":
			return com[1:-1]
		else:
			return "INVALID COMMAND TYPE"

	def dest(self, comNum):
		com = self.commands[comNum]
		comType = commandType(com)
		if comType == "C_COMMAND":
			index = com.find('=')
			if index != -1:
				dest = ''
				dest_raw = com[0:index]
				if dest_raw.find('A') != -1:
					dest += 'A'
				if dest_raw.find('M') != -1:
					dest += 'M'
				if dest_raw.find('D') != -1:
					dest += 'D'
				if dest != '':
					return dest
				else:
					return "INVALID DEST"
			else:
				return "NO DEST FOUND"
		else:
			return "INVALID COMMAND TYPE"

	def comp(self, comNum):
		comp_raw = self.commands[comNum]
		comType = commandType(comp_raw)
		if comType == 'C_COMMAND':
			eqIndex = comp_raw.find('=')
			scIndex = comp_raw.find(';')
			
			if eqIndex != -1:
				comp_raw = comp_raw[eqIndex+1:]
			if scIndex != -1:
				comp_raw = comp_raw[:scIndex]

			return comp_raw

		else:
			return "INVALID COMMAND TYPE"

	def jump(self, comNum):
		jump_raw = self.commands[comNum]
		comType = commandType(jump_raw)
		if comType == 'C_COMMAND':
			scIndex = jump_raw.find(';')

			if scIndex != -1:
				jump_raw = jump_raw[scIndex+1:]
				return jump_raw
			else:
				return "NO JUMP FOUND"
		else:
			return "INVALID COMMAND TYPE"
