from parser import Parser
from code import *
from symboltable import *
import sys

def main():
	inFile = sys.argv[1]
	outFile = inFile.split('.')[0] + '.hack'
	
	p = Parser(inFile)

	st = SymbolTable()

	lines = []
	lineno = 0
	for i in range(0, len( p.commands )):
		line = ''
		if p.commandType(i) == "C_COMMAND":
			lineno += 1
		elif p.commandType(i) == "A_COMMAND":
			lineno += 1
		elif p.commandType(i) == "L_COMMAND":
			st.addEntry(p.symbol(i), lineno)
		else:
			print "Error on line: " + i + ": " + p.commands[i]
			break

	for i in range(0, len( p.commands )):
		line = ''
		if p.commandType(i) == "C_COMMAND":
			line += '111'
			line += encodeComp(p.comp(i))
			line += encodeDest(p.dest(i))
			line += encodeJump(p.jump(i))
		elif p.commandType(i) == "A_COMMAND":
			if (not st.contains(p.symbol(i))) and p.symbol(i).isalpha():
				st.addVariable(p.symbol(i))
			
			line += '0'
			line += st.getAddress(p.symbol(i))

		elif p.commandType(i) == "L_COMMAND":
			continue
		else:
			print "Error on line: " + i + ": " + p.commands[i]
			break
		line += '\n'
		lines.append(line)


	of = open(outFile, 'w')
	of.writelines(lines)
	of.close()



if __name__ == "__main__":
	main()
