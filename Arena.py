from Tkinter import *
import itertools
from Board import *

arena = None
    
class Arena(Frame):
    """This class provides the user interface for an arena of turtles."""

    def __init__(self, parent, puz, width=750, height=750, **options):
        Frame.__init__(self, parent, **options)
        self.parent = parent
        self.width, self.height = width, height
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack()
    	
    	self.n = puz.size
    	self.puz = puz
	
        parent.title("Flow Solver - Shiv Pande")
        Button(self, text='trunks', command=self.trunks).pack(side=LEFT)
        Button(self, text='brute', command=self.brute).pack(side=LEFT)
        Button(self, text='quit', command=parent.quit).pack(side=LEFT)
        Button(self, text='reset', command=self.reset).pack(side=LEFT)
        Button(self, text='prev', command=self.loadprev).pack(side=LEFT)
        Button(self, text='next', command=self.loadnext).pack(side=LEFT)
        
    	self.colordict = {'*':'white',
    			  'A':'red',#red
    			  'B':'#009900',#dark green
    			  'C':'blue',#blue
    			  'D':'yellow',#yellow
    			  'E':'orange',#orange
    			  'F':'#8FD8D8',#light blue
    			  'G':'#FF0099',#pink
    			  'H':'#5E2605',#brown
    			  'I':'#9900CC',#purple
    			  'J':'#A8A8A8',#white
    			  'K':'#585858',#dark grey
    			  'L':'#66FF66',#lime green
    			  'M':'#999900',#dirty yellow
    			  'N':'#000099',#navy
    			  'O':'#00FFFF',#cyan
    			  'P':'#FF66FF'}#hot pink

        self.colortostring = {'*':'white',
                  'A':'red',#red
                  'B':'dark green',#dark green
                  'C':'blue',#blue
                  'D':'yellow',#yellow
                  'E':'orange',#orange
                  'F':'light blue',#light blue
                  'G':'pink',#pink
                  'H':'brown',#brown
                  'I':'purple',#purple
                  'J':'white',#white
                  'K':'dark grey',#dark grey
                  'L':'lime green',#lime green
                  'M':'dirty yellow',#dirty yellow
                  'N':'navy',#navy
                  'O':'cyan',#cyan
                  'P':'hot pink'}#hot pink

    	self.updateArena()

    def trunks(self):
    	self.puz.fillrequiredcorners('trunk')
    	self.puz.developTrunks()
    	self.updateArena()
    	f=sorted(self.puz.remainingcolors)
    	if not f: f = "None, This level has been solved!"
            #self.colsrem.set(f)

    def loadprev(self):
        self.loadboard(self.puz.boardnum-1)

    def loadnext(self):
        self.loadboard(self.puz.boardnum+1)

    def loadboard(self, boardnum):
        self.puz = Board(self.puz.infile, boardnum)
        self.reset()

    def getpaths(self, grid, start, end, maxdistance = float("Inf")):
        
        curpaths = []
        adjempt = self.getadjacentempty(grid, start[0], start[1])
        for node in adjempt:
            newpath = [node]
            curpaths.append(newpath)
        retpaths = []
        while curpaths:
            path = curpaths.pop()
            if len(path) <= maxdistance:
                if self.iscompletepath(grid, start, end, path):
                    retpaths.append(path)
                successorpaths = self.getsuccessorpaths(grid, path)
                curpaths += successorpaths
        return sorted(retpaths, key=len)

    def getsuccessorpaths(self, grid, path):
        if not path:
            print 'path is empty, this shouldnt happen'
            return
        successors = self.getadjacentempty(grid, path[-1][0], path[-1][1])
        ret = []
        for successor in successors:
            sr, sc = successor[0], successor[1]
            if successor not in path and grid[sr][sc] == '*':
                newpath = path+[successor]
                ret.append(newpath)
        return ret

    #returns a list of points
    def getadjacentempty(self, grid, r, c):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        ret = []
        for dir in dirs:
            r2, c2 = r+dir[0], c+dir[1]
            if r2<0 or c2<0 or r2>=len(grid) or c2>=len(grid):
                continue
            if grid[r2][c2] == '*':
                ret.append((r2,c2))
        return ret

    def iscompletepath(self, grid, start, end, path):
        for node in path:
            nr, nc = node[0], node[1]
            if grid[nr][nc] != '*':
                return False
        startadj = self.getadjacentempty(grid, start[0], start[1])
        endadj = self.getadjacentempty(grid, end[0], end[1])
        if path[0] in startadj and path[-1] in endadj:
            return True

    #returns true if when all of the paths in paths are added to the board it is
    #a legal, solved board
    #paths is a list of lists of points that make a path
    #assume trunks are set up correctly.
    #the list of points in a path does not need to be in order
    def issolved(self,emptytiles, paths):
        #will make a megalist of potential paths
        #will remove elements from emptytiles to make sure they are all used
        newtiles = set()
        for path in paths:
            for tile in path:
                if tile in newtiles:#if there are duplicates, return false
                    return False
                newtiles.add(tile)
                if tile not in emptytiles:
                    return False
                emptytiles.remove(tile)
        return True

    def solveit(self,board):
        emptytiles = board.getallempty()
        print 'empty tiles: ', emptytiles
        allpaths = [] #list of getallpaths for each color. paths[i] corresponds to getallpaths for board.remainingcolors[i]
        
        grid = []
        for i in range(board.size):
            ls = []
            for j in range(board.size):
                if board.get(i,j).isempty():
                    ls.append('*')
                else:
                    ls.append('#')
            grid.append(ls)

            
        mindists = {}
        maxdists = {}
        totalmindists = 0
        for col in board.remainingcolors:
            coline = board.colors[col]
            p1, p2 = (coline.trunk1.row,coline.trunk1.col) , (coline.trunk2.row,coline.trunk2.col)
            md = board.mindist(p1, p2)
            mindists[col] = md
            totalmindists += md
        for col in board.remainingcolors:
            maxdists[col] = len(emptytiles)-(totalmindists-mindists[col])
            
        for col in board.remainingcolors:
            coline = board.colors[col]
            colpaths = self.getpaths(grid, (coline.trunk1.row,coline.trunk1.col) , (coline.trunk2.row,coline.trunk2.col), maxdists[col])
            if len(colpaths) == 0: print 'this level cant be solved because this color has no path to the goal: ', col
            allpaths.append(colpaths)
            print 'all paths found for color: \t%d \t%s' % (len(allpaths[board.remainingcolors.index(col)]), self.colortostring[col])

        #for col in board.remainingcolors:
        #    print 'color: ', col, '  numpaths: ', len(allpaths[board.remainingcolors.index(col)])

        
        count = 1
        numpermutations = 1
        for x in allpaths:
            numpermutations*=len(x)
        if not allpaths:
            print 'i think this board is already solved'
            return
        #now choose one path from each color, and check if solved
        print 'found all possible paths for each color, now we will have to try up to %s different combos of them' % "{:,}".format(numpermutations)
        for item in itertools.product(*allpaths):
            if (count % 100000) == 0:
                print '%f percent: %s of %s' % (float(count)/float(numpermutations)*100.0, "{:,}".format(count), "{:,}".format(numpermutations))
            count+=1
            if self.issolved(list(emptytiles), item):
                #we found a solution, time to finalize the board
                print 'checked %s of %s path combos before finding a solution' % ("{:,}".format(count), "{:,}".format(numpermutations))
                for i in range(len(board.remainingcolors)):
                    for j in range(len(item[i])):
                        pt = item[i][j]
                        board.board[pt[0]][pt[1]] = board.newtile(pt[0], pt[1], board.remainingcolors[i], 'finalpath')
                return True
        print 'i dont think this can be solved'
        return False

    def brute(self):
        self.solveit(self.puz)
	self.updateArena()

    def updateArena(self):
	for x in range(self.n):
	    for y in range(self.n):
		a,b = y*60, x*60
		self.canvas.create_rectangle(a,b,a+60,b+60,fill=self.colordict[self.puz.get(x,y).color])
		if self.puz.get(x,y).kind == 'root':
		    self.canvas.create_rectangle(a+20,b+20,a+40,b+40,fill='black')

    def reset(self):
	b = self.puz.__class__
        self.puz = b(self.puz.infile, self.puz.boardnum)
	self.updateArena()
