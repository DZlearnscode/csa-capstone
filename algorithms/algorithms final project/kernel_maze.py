def build_maze(m,n,swag):
  from random import randint  
  grid = []
  for l in range(m):
    row = []
    for d in range(n):
      row.append("wall")
    grid.append(row)
  start_i = randint(0, m-1)
  start_j = randint(0, n-1)
  grid[start_i][start_j] = "start"
  mow(grid, start_i, start_j)
  start = (start_i, start_j)
  explore_maze(grid, start_i, start_j, swag)
  return grid
  
def print_maze(grid):
  for row in grid:
    printable_row = ""
    for cell in row:
      if cell == "wall":
        char = "|"
      elif cell == "empty":
        char = " "
      elif cell == "start":
        char = "S"
      else:
        char = cell[0]
      printable_row += char
    print(printable_row)
    
def mow(grid, i, j):
  from random import randint
  directions = ["U","D","L","R"]
  while (len(directions) > 0):
    directions_index = randint(0, len(directions)-1)
    direction = directions.pop(directions_index)    
    if direction == 'U':
      if i - 2 < 0:
        continue
      elif grid[i - 2][j] == 'wall':
        grid[i - 1][j] = 'empty'
        grid[i - 2][j] = 'empty'
        mow(grid, i - 2, j)
    elif direction == 'D':
      if i + 2 >= len(grid):
        continue
      elif grid[i + 2][j] == 'wall':
        grid[i + 1][j] = 'empty'
        grid[i + 2][j] = 'empty'
        mow(grid, i + 2, j)
    elif direction == 'L':
      if j - 2 < 0:
        continue
      elif grid[i][j-2] == 'wall':
        grid[i][j-1] = 'empty'
        grid[i][j-2] = 'empty'
        mow(grid, i, j - 2)
    else:
      if j + 2 >= len(grid[0]):
        continue
      elif grid[i][j+2] == 'wall':
        grid[i][j+1] = 'empty'
        grid[i][j+2] = 'empty'
        mow(grid, i, j + 2)

def explore_maze(grid, start_i, start_j, swag):
  from random import randint
  copy_grid = [row[:] for row in grid]
  bfs_queue = [[start_i, start_j]]
  directions = ['U', 'D', 'L', 'R']
  while bfs_queue:
    i, j = bfs_queue.pop(0)
    if grid[i][j] != "start" and randint(1,10) == 1:
      grid[i][j] = swag[randint(0,len(swag)-1)]
    copy_grid[i][j] = "visited"
    for direction in directions:
      explore_i = i
      explore_j = j
      if direction == 'U':
          explore_i = i - 1
      elif direction == 'D':
        explore_i = i + 1
      elif direction == 'L':
        explore_j = j - 1 
      else:
        explore_j = j + 1
      if explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0]):
        continue
      elif copy_grid[explore_i][explore_j] != 'visited' and copy_grid[explore_i][explore_j] != 'wall':
        bfs_queue.append([explore_i, explore_j])
  grid[i][j] = "END"
  start = (start_i, start_j)
  end = (i, j)
  print_maze(grid)
  a_star(grid, start, end, swag)
  
#calculates heuristic distance from current position to end
  
#current, end are tuple of coordinates of the current and end positions.

def heuristic(current, end):
  from math import sqrt
  i_distance = abs(current[0] - end[0])
  j_distance = abs(current[1] - end[1])
  return sqrt(i_distance**2 + j_distance**2)

#start, end are tuple of coordinates of the start and end positions.

def a_star(grid, start, end, swag):
  from heapq import heappush, heappop
  from math import inf
  paths_distances = {}  
  items = {}
  path = [start]
  for item in swag:
    items[item] = 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      paths_distances[(i,j)] = inf
  paths_distances[start] = 0
  cells_to_explore = [[0, start]]
  while paths_distances[end] == inf and cells_to_explore:
    current_distance, current_cell = heappop(cells_to_explore)
    U = (current_cell[0] - 1, current_cell[1])
    D = (current_cell[0] + 1, current_cell[1])
    L = (current_cell[0] , current_cell[1] - 1)
    R = (current_cell[0] , current_cell[1] + 1)
    directions = [U, D, L, R]
    while directions:
      direction = directions.pop()
      if direction[0] < 0 or direction[0] >= len(grid) or direction[1] < 0 or direction[1] >= len(grid[0]):
        continue
      elif grid[direction[0]][direction[1]] == "wall":
        continue
      else:
        d_to_e = heuristic([direction[0],direction[1]], end)
        d_from_s = heuristic(start, [direction[0],direction[1]])
        total_distance = d_to_e + d_from_s
        if total_distance < paths_distances[(direction[0],direction[1])]:
          paths_distances[(direction[0],direction[1])] = total_distance
          heappush(cells_to_explore, [total_distance, direction])
        paths = [start]  
        for path, distance in paths_distances.items():
          if distance != inf:
            paths.append(path)
        for loc in paths:
          if grid[loc[0]][loc[1]] != "END" and grid[loc[0]][loc[1]] != "start":
            if grid[loc[0]][loc[1]] in swag:
              items[grid[loc[0]][loc[1]]] += 1
            grid[loc[0]][loc[1]] = "."
  items_sorted = bubble_sort(items) 
  print("Items collected exploring the maze in decending order:\n{0}\n The path taken is shown below:".format(items_sorted))
  print_maze(grid)
          
def bubble_sort(items):
  items_list = []
  n = len(items_list) 
  for item, count in items.items():
    items_list.append([count, item])  
  n = len(items_list)
  for y in range(n):
    for x in range(n-y-1):
      if items_list[x][0] < items_list[x+1][0]:
        items_list[x], items_list[x+1] = items_list[x+1], items_list[x]  
  return items_list
          
#test run:      
       
grid = build_maze(30, 55, ['candy corn', 'werewolf', 'pumpkin'])









"""
Moving two cells at a time we set the minimum distance between each turn to be at least 3 cells, current cell + 2 cell towards the chosen cell. Increasing this number will increase the minimum distance between each turn [U,D,L,R].
If the movement variable was not constant the minimum distance between each turn would be more random thus would randomise the paths in the maze.

Breadth First Search (BFS) and Depth First Search (DFS) algorithms can both be used to traverse through the graph to find a path between the point A and point B. DFS could find a path faster by just seeing through one path from start to end but it wont necessarly be the shortest path. Whereas BFS will first check every neighbor of the current cell before moving to the next cell, unlike DFS that stick to one path to its end, BFS might take longer but it will find all possible path from point A to B including the shortest one. 

By knowing the algoritm used to generate the maze we can better optimise our algorithm to fallow the rules of the maze construction, we can also know if there is more then one solution or not.

The best way to store the items picked up would be a dictionary mapping items to amount of time you came acroos them. By using a dictionary you can in a very simple way increment the count of an items with the '+=' operator ie 
    item_dict[item] += 1
where with a nested list, which is easier to sort, it would be more dificult to increment the count. Further more, in order to sort the items, its quite easy to translate the dictionary to a nested list of items and counts.

To sort the items collect we could use a variety of algorithms like bubble sort, merge sort and quick sort.
I choose to implement bubble sort as the number of items we were given to test with was small and often will be partly sorted due to that i decided to implemant the simplest sorting algorithm; bubble sort - another reason for me choosing this algorithm quite frankly, is that I was short on time.

If the swag list was larger in size and variety I would have used merge sort algorithm with a little twist to it, ultimately turning it into a quick sort algorithm to deal with larger quantities of variables.
"""
    