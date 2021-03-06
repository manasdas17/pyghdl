import curses
import math

stdscr = None
processWindow = None
msgWindow = None
dataWindow = None

def formatString(msg, width, indent) :
  lIndent = " "*(indent)
  newmsg = ""
  loopIndex = int(len(msg) / width)
  if loopIndex < 1 :
    return 0, msg
  for i in range(0, loopIndex) :
    if i == loopIndex :
      newmsg += (lIndent+msg[width*i:])
    else :
      newmsg += (msg[width*i : (i+1)*width])
      newmsg += "\n"+lIndent
  return loopIndex, newmsg


def killCurses() :
  global stdscr
  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()


def initCurses() :
  global stdscr
  stdscr = curses.initscr()
  curses.start_color()
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)

  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
  
  global processWindow
  processWindow = curses.newwin(10,curses.COLS,0,0)
  processWindow.idlok(1)
  processWindow.scrollok(1)
  processWindow.refresh()

  py, px = processWindow.getmaxyx()
  py = int(py)
  px = int(px)
  global msgWindow
  msgWindow = curses.newwin(curses.LINES - py - 2
      , int(curses.COLS/3)
      , int(py + 1), 0)
  msgWindow.idlok(1)
  msgWindow.scrollok(1)
  msgWindow.refresh()

  global dataWindow
  dataWindow = curses.newwin(curses.LINES - py -2, int(curses.COLS*2/3),
      py+1, int(curses.COLS/3)+1)
  dataWindow.idlok(1)
  dataWindow.scrollok(1)
  dataWindow.refresh()

def writeOnWindow(win, msg, indent=1, overwrite=False
    , raw = True
    , appendNewLine=False, opt=None) :
  y, x = win.getyx()
  if appendNewLine :
    win.addstr(y, x, "\n")
    win.refresh()
  maxY, maxX = win.getmaxyx()
  y, x = win.getyx()
  
  if not raw :
    lines, msg = formatString(msg, maxX-indent, indent)
  if overwrite : 
    x = 0
    y -= 2
  assert y >= 0, x >= 0
  
  if opt :
    win.addstr(int(y),int(x+1+indent),str(msg), opt)
  else :
    win.addstr(int(y),int(x+1+indent),str(msg))
  win.refresh()

