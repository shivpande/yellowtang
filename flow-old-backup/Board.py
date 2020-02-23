class Tile:
    def __init__(self, a, b, col = '*', kin = '*'):
        self.row, self.col = a, b
        self.color = col
        self.kind = kin

    # '*' means empty, is valid
    # 'wall' means a wall, is invalid
    # 'root' means this tile is one of the starting or ending positions
    # 'trunk' means this tile is absoloutely required to be taken up by its color.
        
    def isempty(self): return self.kind == '*' or self.color == '*'
    def iswall(self): return self.kind == 'wall'
    def isroot(self): return self.kind=='root'
    def tostring(self): return '{' + str((self.row,self.col,self.color,self.kind))+'}'
#end of Tile class

class ColorLine:
    def __init__(self, r1, r2, clr):
        self.root1 = r1
        self.root2 = r2
        self.color = clr
        self.connection = 'disconnected'
        self.trunk1 = r1
        self.trunk2 = r2

    def tostring(self):
        return '(%d,%d), (%d,%d), %s, %s, (%d,%d) (%d,%d)' % (self.root1.row, self.root1.col, self.root2.row, \
                self.root2.col, self.color, self.connection, self.trunk1.row, self.trunk1.col, self.trunk2.row, self.trunk2.col)
#end of ColorLine class

class Board:
    def __init__(self, infile, boardnum):
        #boardnum represents the index of which board in the infile we want to get.

        f = open(infile)
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            lines[i]=lines[i].replace('\n','')
        self.infile, self.boardnum  = infile, boardnum
        curboardnum = 1
        curlnnum = 0
        while curboardnum<boardnum:
            curlnnum += len(lines[curlnnum]) +1
            curboardnum +=1
        self.size = len(lines[curlnnum])
        self.colors = {}
        self.board = [[Tile(x,y,'*','*') for y in range(self.size)]for x in range(self.size)]
        self.roots = []
        #set roots and colors
        for a in range(self.size):
            ln =lines[curlnnum+a]
            for b in range(self.size):
                if ln[b]!='*':
                    self.board[a][b] = Tile(a,b,ln[b], 'root')
                    self.roots.append(self.board[a][b])
                    if ln[b] in self.colors:
                        if self.colors[ln[b]].root2!=None:
                            print 'you have a problem with your roots in the input. check the root: %s at %d,%d' % (ln[b], a, b)
                        else:
                            self.colors[ln[b]].root2=self.board[a][b]
                            self.colors[ln[b]].trunk2=self.board[a][b]
                    else: self.colors[ln[b]] = ColorLine(self.board[a][b], None, ln[b])
        
        self.remainingcolors = self.colors.keys()

    def get(self, row, col):
        if row<0 or col<0 or row>=self.size or col>=self.size:
            return Tile(row,col,'wall', 'wall')
        return self.board[row][col]

    
    def printBoard(self, txt='BOARD'):
        print '~~~~~~~~~~~~%s~~~~~~~~~~~~' % txt
        for i in range(self.size):
            ln=''
            for j in range(self.size):
                ln +=self.board[i][j].color
            print ln
        print '~~~~~~~~~~~~%s~~~~~~~~~~~~' % ('~'*len(txt))

    def getadjacent(self, thetile):#return list of adj tiles, not including "walls"
        nort = self.get(thetile.row-1,thetile.col )
        sout = self.get(thetile.row+1,thetile.col )
        west = self.get(thetile.row  ,thetile.col-1)
        east = self.get(thetile.row  ,thetile.col+1)
        ret = []
        for x in (nort, sout, west, east):
            if not x.iswall(): ret.append(x)
        return ret

    def getadjacentempty(self, r, c):#return list of adj ampty tiles
        nort = self.get(r-1,c )
        sout = self.get(r+1,c )
        west = self.get(r  ,c-1)
        east = self.get(r  ,c+1)
        ret = []
        for x in (nort, sout, west, east):
            if x.isempty(): ret.append(x)
        return ret

    #returns a list of coodinates of all valid adjacent (empty or not) coordinates
    def getadjacentcoords(self, thetile):
        nort = self.get(thetile.row-1,thetile.col )
        sout = self.get(thetile.row+1,thetile.col )
        west = self.get(thetile.row  ,thetile.col-1)
        east = self.get(thetile.row  ,thetile.col+1)
        ret = []
        for x in (nort, sout, west, east):
            if not x.iswall(): ret.append((x.row, x.col))
        return ret
        

    def getPossibleBranches(self, thetile):#return list of _empty_ adjavent tiles.
        nort = self.get(thetile.row-1,thetile.col )
        sout = self.get(thetile.row+1,thetile.col )
        west = self.get(thetile.row  ,thetile.col-1)
        east = self.get(thetile.row  ,thetile.col+1)
        ret = []
        for x in (nort, sout, west, east):
            if x.isempty(): ret.append(x)
        return ret

    #helpter function for develop trunks. it repeatedly makes trivial (one option) decisions
    #for a particular color 
    def setUntilFork(self, start, connectnode, setkind, connectkind):
        if start.isempty() or start.iswall():
            print 'you are trying to setUntilFork for a piece that is either empty or a wall'
            exit()
        avail = self.getPossibleBranches(start)
        theoldtile = start
        if len(avail)==0 and start.kind == 'root' and connectnode not in self.getadjacent(theoldtile):
            print 'this root doesnt have any available moves.the input board is invalid'
        while len(avail) == 1 or connectnode in self.getadjacent(theoldtile):
            if connectnode in self.getadjacent(theoldtile):
                if len(avail)==0:
                    #this connection is required
                    self.colors[theoldtile.color].connection = connectkind
                    if connectkind == 'finalized':
                        self.remainingcolors.remove(theoldtile.color)
                    return connectnode
                else:
                    #this connection is not yet required
                    self.colors[theoldtile.color].connection = connectkind
                    if connectkind == 'finalized':
                        self.remainingcolors.remove(theoldtile.color)
                    return connectnode
            else:
                theoldtile = avail[0]
                theoldtile.color = start.color
                theoldtile.kind = setkind
                avail = self.getPossibleBranches(theoldtile)
                if len(avail) == 0 and connectnode not in self.getadjacent(theoldtile): print 'i think we have a dead end situation here'
                if len(avail) != 1: return theoldtile
        return None
               
    def developTrunks(self):
        hasdeveloped = 1
        while hasdeveloped:
            hasdeveloped = 0
            for cul in self.remainingcolors:
                if cul in self.remainingcolors:
                    a = self.setUntilFork(self.colors[cul].trunk1, self.colors[cul].trunk2, 'trunk', 'finalized')
                    if a:
                        self.colors[cul].trunk1 = a
                        hasdeveloped = 1
                if cul in self.remainingcolors:
                    a = self.setUntilFork(self.colors[cul].trunk2, self.colors[cul].trunk1, 'trunk', 'finalized')
                    if a:
                        self.colors[cul].trunk2 = a
                        hasdeveloped=1


    def fillrequiredcorners(self, setkind):
        for color in self.remainingcolors:
            n=self.size-1
            til = self.colors[color].root1
            if (til.row, til.col) in [(0,1),(1,0)] and self.get(0,0).isempty():
                self.board[0][0] = Tile(0,0,color, setkind)
                self.colors[color].trunk1 = self.get(0,0)
            if (til.row, til.col) in [(0,n-1),(1,n)] and self.get(0,n).isempty():
                self.board[0][n] = Tile(0,n,color, setkind)
                self.colors[color].trunk1 = self.get(0,n)
            if (til.row, til.col) in [(n-1,0),(n,1)] and self.get(n,0).isempty():
                self.board[n][0] = Tile(n,0,color, setkind)
                self.colors[color].trunk1 = self.get(n,0)
            if (til.row, til.col) in [(n,n-1),(n-1,n)] and self.get(n,n).isempty():
                self.board[n][n] = Tile(n,n,color, setkind)
                self.colors[color].trunk1 = self.get(n,n)
            til = self.colors[color].root2
            if (til.row, til.col) in [(0,1),(1,0)] and self.get(0,0).isempty():
                self.board[0][0] = Tile(0,0,color, setkind)
                self.colors[color].trunk2 = self.get(0,0)
            if (til.row, til.col) in [(0,n-1),(1,n)] and self.get(0,n).isempty():
                self.board[0][n] = Tile(0,n,color, setkind)
                self.colors[color].trunk2 = self.get(0,n)
            if (til.row, til.col) in [(n-1,0),(n,1)] and self.get(n,0).isempty():
                self.board[n][0] = Tile(n,0,color, setkind)
                self.colors[color].trunk2 = self.get(n,0)
            if (til.row, til.col) in [(n,n-1),(n-1,n)] and self.get(n,n).isempty():
                self.board[n][n] = Tile(n,n,color, setkind)
                self.colors[color].trunk2 = self.get(n,n)


    def getallempty(self):
        ret = []
        for row in range(self.size):
            for col in range(self.size):
                t = self.get(row,col)
                if t.isempty():
                    pt = (self.board[row][col].row, self.board[row][col].col)
                    ret.append(pt)
        return ret

    def newtile(self, a, b, col = '*', kin = '*'):
        return Tile (a, b, col, kin)

    def mindist(self,p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) -1
            

#end of Board class
    

