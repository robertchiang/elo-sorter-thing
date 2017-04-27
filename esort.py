#oh man it's been a really long time since I've done any coding whatsoever

import csv
import os
import random

#global variables woo
data = [] #the matrix
elo = [] #elo storage
empty = []

#didn't write this; forget who did
def getch():
    import sys, tty, termios 
    fd = sys.stdin.fileno() 
    old = termios.tcgetattr(fd) 
    try: 
        tty.setraw(fd) 
        return sys.stdin.read(1) 
    finally: 
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

#why are you defining this as a function when it's basically just one line?
def clear():
	os.system('clear') #because it's easier to type

#it, uh, reads the data
def readData():
	global data #I'm sure I've been warned about global variables for some reason or other

	inputfile = open('input.csv', 'r+')

	data = list(csv.reader(inputfile))
	for i in range(len(data)):
		print data[i]

#sets the appropriate length and sets initial values
def initElo():
	global data
	global elo #but I care not

	elo = [0]*(len(data)-1) #The start value is arbitrary, right? Isn't 0 sort of a logical start point, then? Why does chess or whatever use like 1000?

#expected score
def expectation(A, B):
	return (1 / (1 + 10**((float(B)-float(A))/1000))) #I think these numbers are arbitrary too, actually

#produce the new elo value based on the old and the expected and actual scores
def updateElo(old, exp, act): 
	return (old + (act - exp) * 100) #So I just picked round numbers

#calculates Elo using the matchup data in the matrix
def calcElo():
	global data
	global elo 
	filledData = []

	oldA, oldB, expA, expB, actA, actB = (0.0,)*6 #is this how memory works in python? Not like it matters at this scale

	for i in range(2,len(data)): #the rows with data in them
			for j in range(1,i): #the columns with data in them, since the matrix's lower triangular
				temp = data[i][j]
				if (temp == '1') or (temp == '0') or (temp == '-1'): #if it's filled, add it to the list
					filledData.append((i, j))

	random.shuffle(filledData) #shuffles our collection of filled entries

	for index in filledData: #and now update the elo in that random order
		temp = data[index[0]][index[1]]

		oldA = elo[index[0]-1]
		oldB = elo[index[1]-1]

		expA = expectation(oldA, oldB)
		expB = expectation(oldB, oldA) #more efficient, but less clear, to use 1-expA

		#update elo according to result, and if it's empty or * just don't do anything
		temp = float(temp) #python and its variable typing
		actA = .5+(temp/2);
		actB = .5-(temp/2);

		elo[index[0]-1] = updateElo(oldA, expA, actA)
		elo[index[1]-1] = updateElo(oldB, expB, actB) 


#calcElo randomizes the order because a single matchup matrix set produces a number of different final Elo results depending on the order the matchups are run
#one solution is to just run it like a hundred times and average it out
def averageElo():
	global elo #actually, i can see how this could bite me
	iterations = 10000
	aElo = [0]*(len(data)-1)

	for i in range(0, iterations): #add up all the iterations
		initElo()
		calcElo()
		aElo = [x+y for x, y in zip(aElo, elo)]

	aElo = [int(x/iterations) for x in aElo] #and reduce them at the end, to an int so it's prettier
	
	elo = aElo

#find the empty entries in the matrix
def getEmpty():
	global data
	global empty

	for i in range(2,len(data)): #the rows with data in them
			for j in range(1,i): #the columns with data in them, since the matrix's lower triangular
				if data[i][j] == '': #if there's no data
					empty.append([i,j]) #add it to the list

#fill the empty entries
def fillEmpty():
	global data
	global empty
	entry = [] #i really don't know if this is how python memory works

	for i in range(len(empty)): #for each empty spot
			entry = empty[i]

			clear()
			print str(i) + " down, " + str(len(empty)-i) + " to go."
			print 'Matchup: ' + data[0][entry[1]]+ ' vs. ' + data[entry[0]][0] #print the names (reversed for alphabetization)
			print 'q to favour the former, w to tie, e the latter, r to refuse comparison, y to quit'
			print entry

			ch = 0
			while (ch != 'q') and (ch != 'w') and (ch != 'e') and (ch != 'r') and (ch != 'y'): #get input
				ch = getch()

			if ch == 'q': #then update the matrix as appropriate
				data[entry[0]][entry[1]] = -1
			elif ch == 'w':
				data[entry[0]][entry[1]] = 0
			elif ch == 'e': 
				data[entry[0]][entry[1]] = 1
			elif ch == 'r': 
				data[entry[0]][entry[1]] = '*'
			else:
				break

def main():
	global data
	global elo
	global empty #why don't I just pass this around instead of making it global? Laziness, I guess
	choice = 0

	readData()

	print 'Pick one.'
	print '1. Update the matrix.'
	print '2. Calculate rankings.'

	while (choice != 1) and (choice != 2):
		choice = input();
		if choice == 1:
			clear()
			print 'Updating matrix.'
		elif choice == 2:
			clear()
			print 'Calculating rankings.'
		else: 
			clear()
			print '1 or 2, can\'t you read?' #rude

	if choice == 1: 
				
		getEmpty()
		random.shuffle(empty) #shuffle the list
		fillEmpty()

		outputfile = open('output.csv', 'w')

		writer = csv.writer(outputfile)
		writer.writerows(data)
	else:
		initElo()
		averageElo()

		for i in range(len(elo)):
			print data[i+1][0] + ': ' + str(elo[i])

		eloOutput = open('ranking.csv', 'w')

		data[0].pop(0) #remove the first (blank) entry in the first row of data, producing just a list of names

		writer = csv.writer(eloOutput)
		writer.writerows(zip(data[0], elo)) #output names and elo

main()