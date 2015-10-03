from Board import *
from Arena import *
from optparse import OptionParser

myparser = OptionParser()
myparser.add_option("-f", dest="batchfile", default="boards",  help="-f for input file", type="string")
myparser.add_option("-n", dest="boardnum", default="0",  help="-n for board number", type="string")
(input, args) = myparser.parse_args(args=sys.argv)    
    
tk = Tk()                              # Create a Tk top-level widget
puz = Board(input.batchfile, int(input.boardnum))
arena = Arena(tk, puz)                      # Create an Arena widget, arena
arena.pack()                           # Tell arena to pack itself on screen
tk.mainloop()
