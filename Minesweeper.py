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
numMines = 10
boarddata = []
win = False
font = pygame.font.Font('freesansbold.ttf', int(windowSize/length/2))
img = [font.render(str(i), True, (200, 200, 200)) for i in range(9)]
img.append(font.render("X", True, (200, 200, 200)))

def incSquare(board, a, b):
		if board[a][b]!=-1:
			board[a][b]+=1

def genMine(ls):
		a = (random.randrange(0,length),random.randrange(0,length))
		if a not in ls: 
			ls.append(a)
		else:
			genMine(ls)
			
def setboard():
	global revealed
	global win
	win = False
	revealed=0
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
			if b<length-1:
				incSquare(board, a-1,b+1)
		if a<length-1:
			incSquare(board, a+1,b)
			if b>0:
				incSquare(board, a+1,b-1)
			if b<length-1:
				incSquare(board, a+1,b+1)
		if b>0:
			incSquare(board, a,b-1)
		if b<length-1:
			incSquare(board, a,b+1)
	return board

def rendersquare(a,b):
	size = windowSize/length
	color = (255,215,0) if win else (200,0,0) if boarddata[a][b]==-1 else (0,0,200)
	renderqueue.append((color,pygame.Rect(a*size+5,b*size+5, size-10,size-10)))
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
	if board[a][b] == False:
		global revealed
		revealed +=1
		board[a][b]=True
		rendersquare(a,b)
		revealsquare(board, a,b)
	else:
		board[a][b]=True
		rendersquare(a,b)
	
def flag(a,b):
	if not boarddisplay[a][b]:
		size = windowSize/length
		renderqueue.append(((0,200,0),pygame.Rect(a*size+5,b*size+5, size-10,size-10)))

def revealsquare(board, a, b):
	reveal(board,a,b)
	if boarddata[a][b]==0:
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

def gameover(board):
	for i in range(length):
		for j in range(length):
			if board[i][j]==-1:
				rendersquare(i,j)
	
def click(pos, right):
	global revealed
	global begin
	global boarddata
	global boarddisplay
	x = int(float(pos[0]/windowSize)*length)
	y = int(float(pos[1]/windowSize)*length)
	if right:
		flag(x,y)
		return False
	if not boarddisplay[x][y]:
		revealsquare(boarddisplay, x,y)
		if boarddata[x][y]==-1:
			if begin:
				#print("Reset")
				boarddata = setboard()
				boarddisplay = setboarddisplay(renderqueue)
				click(pos, False)
				return False
			gameover(boarddata)
			print("Game Over")
			return True
	if revealed+numMines==length*length:
		print("You Win!")
		global win
		win = True
		gameover(boarddata)
		return True
	begin=False
	return False
renderqueue = []
revealed=0
boarddata = setboard()
boarddisplay = setboarddisplay(renderqueue)
begin = True
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
				#print(pygame.mouse.get_pressed())
				end=click(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[2])
	#tick
	
	#render
	renderqueue = render(screen, renderqueue)
	
