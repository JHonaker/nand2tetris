# Testing script for the parser

from parser import *

p = parser('StackArithmetic/SimpleAdd/SimpleAdd.vm')

print 'Testing SimpleAdd'
while(p.hasMoreCommands()):
    p.advance()

q = parser('./StackArithmetic/StackTest/StackTest.vm')

print '\nTesting StackTest'
while(q.hasMoreCommands()):
    q.advance()
