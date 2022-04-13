import pygame
from pygame.locals import *
import random
pygame.init()

clock = pygame.time.Clock()
fps = 30

windowSize = 800
screenheight= 800

screen = pygame.display.set_mode((windowSize, windowSize))

pygame.display.set_caption("Minesweeper")

length = 8
numMines = 8
boarddata = []
font = pygame.font.Font('freesansbold.ttf', int(windowSize/length/2))
img = [font.render(str(i), True, (200, 200, 200)) for i in range(9)]
img.append(font.render("X", True, (200, 200, 200)))

def incSquare(board, a, b):
		if board[a][b]!=-1:
			board[a][b]+=1

def genMine(ls):
		a = (random.randrange(0,length-1),random.randrange(0,length-1))
		if a not in ls: 
			ls.append(a)
		else:
			genMine(ls)
			
def setboard():
	board = []
	mines = []
	for i in range(numMines):
		genMine(mines)

	for i in range(length):
		board.append([])
		for j in range(length):
			board[i].append(0)

	for i in mines:
		(a,b) = i
		board[a][b]=-1
		if a>0:
			incSquare(board, a-1,b)
			if b>0:
				incSquare(board, a-1,b-1)
			if b<length:
				incSquare(board, a-1,b+1)
		if a<length:
			incSquare(board, a+1,b)
			if b>0:
				incSquare(board, a+1,b-1)
			if b<length:
				incSquare(board, a+1,b+1)
		if b>0:
			incSquare(board, a,b-1)
		if b<length:
			incSquare(board, a,b+1)
	return board

def rendersquare(a,b):
	size = windowSize/length
	renderqueue.append(((0,0,200),pygame.Rect(a*size+5,b*size+5, size-10,size-10)))
	renderqueue.append((img[boarddata[a][b]],(int(size*(0.35+a)),int(size*(0.25+b)))))
	

def drawStyleRect(i,j):
	size = windowSize/length
	scol = (200,200,200)
	bcol = (100,100,100)
	renderqueue.append((scol,pygame.Rect(i*size+5,j*size+5, size,size)))
	renderqueue.append((bcol,pygame.Rect(i*size,j*size, size,5)))
	renderqueue.append((bcol,pygame.Rect(i*size,(j+1)*size-5, size,5)))
	renderqueue.append((bcol,pygame.Rect(i*size,j*size, 5,size)))
	renderqueue.append((bcol,pygame.Rect((i+1)*size-5,j*size, 5,size)))

def setboarddisplay(renderqueue):
	board = []	
	for i in range(length):
		board.append([])
		for j in range(length):
			board[i].append(False)
			drawStyleRect(i,j)
	return board

def printboard(board):
	for i in board:
		for j in i:
			print(j, end="\t")
		print("")

def reveal(board, a, b):
	if boarddata[a][b]==0 and not board[a][b]:
		board[a][b]=True
		rendersquare(a,b)
		revealsquare(board, a,b)
	else:
		board[a][b]=True
		rendersquare(a,b)
	
		

def revealsquare(board, a, b):
	reveal(board,a,b)
	if a>0:
		reveal(board, a-1,b)
		if b>0:
			reveal(board, a-1,b-1)
		if b<length-1:
			reveal(board, a-1,b+1)
	if a<length-1:
		reveal(board, a+1,b)
		if b>0:
			reveal(board, a+1,b-1)
		if b<length-1:
			reveal(board, a+1,b+1)
	if b>0:
		reveal(board, a,b-1)
	if b<length-1:
		reveal(board, a,b+1)

def render(screen, queue):
	#pygame.Rect(x,y,width,height)
	for (a,b) in queue:
		if type(b)==pygame.Rect:
			pygame.draw.rect(screen, a, b)
		else:
			screen.blit(a, b)
	pygame.display.update()
	return []

def click(pos):
	x = int(float(pos[0]/windowSize)*length)
	y = int(float(pos[1]/windowSize)*length)
	if not boarddisplay[x][y]:
		revealsquare(boarddisplay, x,y)
		if boarddata[x][y]==-1:
			print("Game Over")
			return True
	return False
renderqueue = []
boarddata = setboard()
boarddisplay = setboarddisplay(renderqueue)

run = True
end = False
#printboard(boarddata)
#revealsquare(boarddisplay, 5,5)
#printboard(boarddisplay)


pygame.display.update()
while run:
	clock.tick(fps)
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN: 
			if not end:
				end = click(pygame.mouse.get_pos())
	#tick
	
	#render
	renderqueue = render(screen, renderqueue)
	
