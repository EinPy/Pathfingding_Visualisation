import pygame
import random
import math


pygame.init()

xSize = 1280
ySize = 780

white = (255,255,255)
grey = (178, 218, 248)

win = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pathfinding Algorithms")
clock = pygame.time.Clock()


class Grid:

	def __init__(self, xStart, yStart, cols):
		"""
		will contain rows an colums filled with objects of cubes
		"""
		self.xStart = xStart
		self.yStart = yStart
		self.rows = 0
		self.cols = cols
		self.cubes = []
		self.selected = (0,0)
		self.visited = {}
		self.queue = []
		self.graph = {}
		self.HORIZONTAL = 0
		self.VERTICAL = 1
		self.noGo = {}

	def createGrid(self):
		self.cubes = [[0 for _ in range(self.rows)] for _ in range(self.cols)]


	def fillCubes(self):
		gapX = (xSize - self.xStart) // self.cols
		print("gapX is: ", gapX, "\n")
		gapY = (ySize - self.yStart) / ((ySize - self.yStart) // gapX)
		print("gapY is: ", gapY, "\n")
		self.rows = int ((ySize - self.yStart) // gapY)
		print("amount of rows are: ", self.rows, "\n")

		self.cubes = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j] = Cube(self.xStart + (gapX* j), self.yStart + (gapY * i), j, i, gapX, gapY)

	def drawCubes(self, win):
		for row in self.cubes:
			for cube in row:
				cube.draw(win)

	def select(self,row,col):
		#reset other cubes from being selected
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].selected = False

		self.cubes[row][col].selected = True
		self.selected = (row,col)

	def move_selected(self,change_row,change_col):
		row, col = self.selected
		self.cubes[row][col].selected = False
	#		print(f'trying to change from {row},{col} to {row - change_row}, {col - change_col}')
		if row  - change_row <= self.rows and row  - change_row >= 0:
			row -= change_row
		if col  + change_col <= self.cols and col + change_col >= 0:
			col += change_col
		self.cubes[row][col].selected = True
		self.selected = (row,col)

	def click(self, pos):
		"""
		detects a click
		param: pos
		return: row, col
		"""
		if pos[0] > self.xStart and pos[0] < xSize:
			if pos[1] > self.yStart:
				gapX = (xSize - self.xStart) // self.cols
				print("gapX is: ", gapX, "\n")
				gapY = (ySize - self.yStart) / ((ySize - self.yStart) // gapX)
				print("gapY is: ", gapY, "\n")
				x = (pos[0] - self.xStart) // gapX
				y = (pos[1] - self.yStart) // gapY
				print(x, y)
				return (int(y), int(x))
			else:
				return None
		else:
			return None

	def makeWall(self):
		row, col = self.selected
		self.cubes[row][col].state = 3

	def resetGrid(self):
		self.cubes = []
		self.selected = ()
		self.visited = {}
		self.queue = []
		self.graph = {}
		self.noGo = {}
		self.fillCubes()
		self.fillGraph()


	def fillGraph(self):
		#fyfaen for noe jævlig spagettikode
		for i in range(len(self.cubes)):
			for j in range(len(self.cubes[0])):
				node = (i,j)
				self.graph[node] = []
				if (i - 1) >= 0:
					self.graph[node].append((i-1, j))
				if (j - 1) >= 0:
					self.graph[node].append((i,j-1))
				if (i + 1) <= len(self.cubes) - 1:
					self.graph[node].append((i+1,j))
				if (j + 1) <= len(self.cubes[0]) - 1:
					self.graph[node].append((i,j+1))


	def bfs(self, start):
		node = start
		self.visited[node] = True
		self.queue.append(node)

		while self.queue:
			s = self.queue.pop(0)
			if s == "layer":

				if len (self.queue) == 0:
#					for cube in self.visited:
#						self.cubes[cube[0]][cube[1]].state = 2
					break
				self.queue.append("layer")
				redrawGameWindow(win)
				redrawGameWindow(win)

			else:
				self.cubes[s[0]][s[1]].state = 4

				if s == self.selected:
					self.queue.append("layer")

				for neighbour in self.graph[s]:

					if neighbour not in self.visited and (self.cubes[neighbour[0]][neighbour[1]].state != 3  and self.cubes[neighbour[0]][neighbour[1]].state != 5):
						self.visited[neighbour] = True
						self.queue.append(neighbour)
		print("done")

	def dfs(self, node):
		if node in self.visited or self.cubes[node[0]][node[1]].state == 3:
			return

		self.visited[node] = True

		self.cubes[node[0]][node[1]].state =  4

		for neighbour in self.graph[node]:
			redrawGameWindow(win)
			self.dfs(neighbour)

	def divide(self, x, y, width, height):

		#distance x and distance y
		dx = width - x
		dy = height - y

		#bottom layer of stack
		if dx < 2 or dy < 2:
			return

		if dx < dy:
			orientation = self.HORIZONTAL
		elif dy < dx:
			orientation = self.VERTICAL
		else:
			orientation = random.choice([self.HORIZONTAL, self.VERTICAL])

		if orientation == self.VERTICAL:
			wall = random.randint(x + 1, width - 1)
			hole = random.randint(y, height - 1)
			self.noGo[(hole, wall + 1)] = True
			self.noGo[(hole, wall - 1)] = True
			for i in range(y, height + 1):
				if i < self.rows:
					print(f"trying to make location ({i}, {wall}) into a wall")
					if i != hole and (i, wall) not in self.noGo:
						if wall != 0 and wall != self.cols - 1:
							if self.cubes[i][wall + 1].state != 3 and self.cubes[i][wall - 1].state != 3:
								self.cubes[i][wall].state = 3
						else:
							self.cubes[i][wall].state = 3
					redrawGameWindow(win, buttons)

			print(f" x for right: {wall + 1}, y: {y}, width: {width}, height: {height}")
			#left
			self.divide(x, y, wall - 1, height)
			#right
			self.divide(wall + 1, y, width, height)
			

		else:
			print(f"wall will be at {y} + {dy} / 2")
			wall = random.randint(y + 1, height -1)
			hole = random.randint(x, width)
			self.noGo[(wall + 1, hole)] = True
			self.noGo[(wall - 1, hole)] = True
			for j in range(x, width + 1):
				if j < self.cols:
					print(f"trying to make location ({wall}, {j}) into a wall")
					if j != hole and (wall, j) not in self.noGo:
						if wall != 0 and wall != self.rows - 1:
							if self.cubes[wall + 1][j].state != 3 and self.cubes[wall - 1][j].state != 3:
								self.cubes[wall][j].state = 3
						else:
							self.cubes[wall][j].state = 3
					redrawGameWindow(win)
			#over
			self.divide(x, y, width, wall - 1)
			#under
			self.divide(x, wall + 1, width, height)


class Cube:

	def __init__(self, x, y, col, row, width, height):
		"""
		the cubes that will make up the grid.
		Attributes:
		-width
		-height
		-selected
		-path
		-start
		-goal
		-wall
		"""
		self.x = x
		self.y = y
		self.col = col
		self.row = row
		self.width = width
		self.height = height
		self.state = 1 #wall, path, start, searching finsih
		self.selected = False
		self.circleCount = 0
		self.initialRad = 2
		self.count = 0
		self.gold = [255,208,23] #grey is (178, 218, 248) -77, +6, +225

	def draw(self,win):
		if self.state == 1:
			pygame.draw.rect(win, grey, (self.x, self.y, self.width, self.height), 1)
		if self.state == 2:
			pygame.draw.rect(win, grey, (self.x, self.y, self.width, self.height))
		if self.state == 3:
			if self.initialRad * self.circleCount < (self.height / 2):
				pygame.draw.circle(win, (169,169,169),(int(self.x + (self.width // 2)), int(self.y + (self.height // 2))), self.initialRad * self.circleCount)
				self.circleCount += 1
			else:
				pygame.draw.rect(win, (169,169,169), (self.x, self.y, self.width, self.height))
		if self.state == 4:
			if self.initialRad * self.circleCount < (self.height / 2) and self.gold[2] <= 255:
				print(self.gold)
				pygame.draw.circle(win, (self.gold[0], self.gold[1], self.gold[2]), (int(self.x + (self.width // 2)), int(self.y + (self.height // 2))), self.initialRad * self.circleCount)
				self.circleCount += 1
				self.gold[0] = int(self.gold[0] - self.circleCount * 1.28)
				self.gold[1] = int(self.gold[1] + self.circleCount * 0.1)
				self.gold[2] = int(self.gold[2] + self.circleCount * 3.75)
			elif self.gold[0] > 217:
				pygame.draw.rect(win, (self.gold[0], self.gold[1], self.gold[2]), (self.x, self.y, self.width, self.height))
				self.count += 1
				self.gold[0] = int(self.gold[0] - self.count * 1.28)
				self.gold[1] = int(self.gold[1] + self.count * 0.1)
				self.gold[2] = int(self.gold[2] + self.count * 3.75)
			else:
				#grey is (178, 218, 248) 77, 6, 225
				pygame.draw.rect(win, grey, (self.x, self.y, self.width, self.height))
		if self.state == 5:
			if self.initialRad * self.circleCount < (self.height / 2):
				pygame.draw.circle(win, (0,128,0),(int(self.x + (self.width // 2)), int(self.y + (self.height // 2))), self.initialRad * self.circleCount)
				self.circleCount += 1
			else:
				pygame.draw.rect(win, (0,128,0), (self.x, self.y, self.width, self.height))
		if self.selected:
			pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.width, self.height), 1)


class Interface:

	def __intit__(self):
		"""
		different texts that will explain the functions to the user
		"""

class Button:

	def __init__(self, x, y, width, height, color, text = ''):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.color = color

	def draw(self, win, outline = None):
		#if outline, draw slightly larger rectangle around it
		if outline:
			pygame.draw.rect(win, outline, (self.x - 2, self.y - 2,self.width + 4, self.height + 4), 0)

		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

		if self.text != '' :
			font = pygame.font.SysFont('comicsans', self.height  - 20)
			text = font.render(self.text, True, (200, 200, 200))
			win.blit(text, (self.x + (self.width /2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

	def is_over(self,pos):
		#pos is a tuple of (x,y) coordinates of the mouse
		x, y = pos
		if x > self.x and x < self.x + self.width:
			if y > self.y and y < self.y + self.height:
				return True

		return False


class Visualize:

	def __init__(self):
		"""
		will containt the different pathfindnig algos and execute the
		animations during the pathfinding on the board
		"""

def redrawGameWindow(win, buttons = []):
	"""
	takes all the elemts that will be drawn and draws them on the screen
	"""
	win.fill(white)
	grid.drawCubes(win)
	clock.tick(30)
	pygame.draw.rect(win, (255,0,0), (10, 19, 10 ,10))
	if buttons: 
		for button in buttons:	
			button.draw(win)
	pygame.display.update()
	pygame.event.pump()




grid = Grid(3, ySize / 4, 55)
grid.fillCubes()
grid.fillGraph()
clear_button = Button(1000, 50, 150, 50, (121,158,196), "Clear matrix")
maze_button = Button(700, 50, 200, 50, (121,158,196), "Recursive maze")
bfs_but = Button(400, 50, 225, 50, (121,158, 196), "Breadth first search")
buttons = [clear_button, maze_button, bfs_but]
running = True



while running:

	for event in pygame.event.get():
		pos = pygame.mouse.get_pos()
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:	
				grid.bfs(grid.selected)
			if event.key == pygame.K_2:
				grid.dfs(grid.selected)
			if event.key == pygame.K_3:
				grid.makeWall()
			if event.key == pygame.K_4:
				grid.resetGrid()
			if event.key == pygame.K_5:
				print("printing grid.rows")
				print(grid.rows)
				print("printed grid.rows")
				grid.divide(0, 0, grid.cols, grid.rows)
			if event.key == pygame.K_6:
				print("printing grid.rows")
				print(grid.rows)
			if event.key == pygame.K_RIGHT:
				grid.move_selected(0, 1)
				print('right')
			if event.key == pygame.K_LEFT:
				grid.move_selected(0, -1)
				print('left')
			if event.key == pygame.K_UP:
				grid.move_selected(1,0)
				print('up')
			if event.key == pygame.K_DOWN:
				grid.move_selected(-1,0)
				print('down')

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = grid.click(pos)
			if clicked != None:
				grid.select(clicked[0], clicked[1])
			if maze_button.is_over(pos):
				grid.resetGrid()
				grid.divide(0, 0, grid.cols, grid.rows)
			if bfs_but.is_over(pos):
				grid.bfs(grid.selected)


		if event.type == pygame.MOUSEMOTION:	
			if pygame.mouse.get_pressed()[0]:
				clicked = grid.click(pos)
				if clicked != None:
					grid.select(clicked[0] , clicked[1])
					grid.makeWall()

			for button in buttons:
				if button.is_over(pos):
					button.color = (0, 128, 0)
				else:
					for button in buttons:
						button.color = (121,158,196)


	redrawGameWindow(win, buttons)
