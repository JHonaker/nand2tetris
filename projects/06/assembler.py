from parser import Parser
from code import *
import sys

def main():
	inFile = sys.argv[1]
	outFile = inFile.split('.')[0] + '.hack'
	
	p = Parser(inFile)

	lines = []
	for i in range(0, len( p.commands )):
		line = ''
		if p.commandType(i) == "C_COMMAND":
			line += '111'
			line += encodeComp(p.comp(i))
			line += encodeDest(p.dest(i))
			line += encodeJump(p.jump(i))
		elif p.commandType(i) == "A_COMMAND":
			line += '0'
			line += "{0:015b}".format(int(p.symbol(i)))
		elif p.commandType(i) == "L_COMMAND":
			pass
		else:
			print "Error on line: " + i + ": " + p.commands[i]
			break
		line += '\n'
		lines.append(line)

	of = open(outFile, 'w')
	of.writelines(lines)
	of.close()
	print lines



if __name__ == "__main__":
	main()
