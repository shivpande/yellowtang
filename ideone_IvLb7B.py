# Solver for "Flow Free" puzzle (phone app)
# App Website - http://a...content-available-to-author-only...p.net/flowfree
# Demo - https://w...content-available-to-author-only...e.com/watch?v=QwGBXO2XMdE\
"""
Sample Input:
.....de
.ac.ca.
....f..
...f..e
b.....d
......b
.......
 
Sample Output:
[1] Generating paths...
d done
e done
a done
c done
f done
b done
a: 20982
c: 1126
b: 7980
e: 2
d: 2966
f: 18869
[2] Finding set cover...
True
a
[(1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (3, 5), (2, 5), (1, 5)]
c
[(1, 2), (1, 3), (1, 4)]
b
[(4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6)]
e
[(0, 6), (1, 6), (2, 6), (3, 6)]
d
[(0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (4, 5), (4, 6)]
f
[(2, 4), (2, 3), (3, 3)]
"""
 
def isValid(grid,r,c):
        return r>=0 and c>=0 and r<len(grid) and c<len(grid[r])
 
# find all possible valid paths from one node to another
def getPaths(grid, node, r, c):
        D = []
        getPaths2(grid, node, r, c, D, [], r, c)
        return D
 
# grid: 2x2 list of input grid
# node: character identifier for pipe ('A', 'B', etc)
# r, c: current row, column of exploration algorithm
# D:    list of all found paths
# S:    stack to store current path
dirs = [(1,0), (-1,0), (0,1), (0,-1)]
def getPaths2(grid, node, r, c, D, S, initR, initC):
        if grid[r][c] == '#': return    # already traversed cell
 
        # empty cell or initial cell, add to stack, etc
        S.append((r,c)) # record cell
        if grid[r][c] == '.' or (r == initR and c == initC):
                lastVal = grid[r][c]
                grid[r][c] = '#'
 
                # explore all 4 directions
                for d in dirs:
                        if not isValid(grid, r+d[0], c+d[1]): continue
                        getPaths2(grid, node, r+d[0], c+d[1], D, S, initR, initC)
 
                grid[r][c] = lastVal
        elif grid[r][c] == node:
                D.append(list(S)) # copy the list you dum dum >.>
                #print("added path for " + node)
        S.pop() # done with cell, remove
 
# find the path (set) of each path pipe that cover all elements and dont intersect
def findCover(P, grid, solution):
        return findCover2(P, grid, P.keys(), 0, [], solution)
 
def intersects(A, B):
        for x in A:
                if x in B:
                        return True
        return False
 
# P: dictionary of pipe sets
# k: list of keys
# i: index of 'k'
# S: running set
QQ = -1
def findCover2(P, grid, k, i, S, solution):
        global QQ
        if len(S) > QQ:
                QQ = len(S)
        if i == len(k):
                return len(S) == len(grid)*len(grid[r])
        for j in range(0, len(P[k[i]])):
                path = P[k[i]][j]
                if intersects(path, S) == True: continue
                solution.append(j)
                if findCover2(P, grid, k, i+1, S+path, solution) == True:
                        return True
                solution.pop()
        return False
 
if __name__ == "__main__":
 
        # read grid from file
        f = open('7x7.txt', 'r')
        grid = []
        for line in f:
                L = list(line)
                grid.append(L[:len(L)-1]) # remove newline character
 
        # create paths structure
        paths = {} # list of potential paths for each pipe
 
        # locate nodes and begin exploring
        print("[1] Generating paths...")
        for r in range(0,len(grid)):
                for c in range(0, len(grid[r])):
                        if grid[r][c] == '.': continue
                        if grid[r][c] in paths: continue
                        paths[grid[r][c]] = getPaths(grid, grid[r][c], r, c)
                        print(str(grid[r][c]) + " done")
 
        # print number of found paths for each pipe
        for k in paths.keys():
                print(str(k) + ": " + str(len(paths[k])))
 
        # find a sort of 'set cover'
        print("[2] Finding set cover...")
        y = []
        sol = findCover(paths, grid, y)
        print(sol)
 
        k = paths.keys()
        for i in range(0, len(k)):
                print(k[i])
                print(paths[k[i]][y[i]])