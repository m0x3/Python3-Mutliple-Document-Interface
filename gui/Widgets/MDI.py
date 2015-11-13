from tkinter import *
import Pmw, sys
from ProgressBar import ProgressBar
from iconPath import path


class MDIChild(Canvas):
    def __init__(self, parent, title='', iconfile=path+'tk.gif', topcolor=None,
                 flickerbg=None, inactivetopcolor=None):
        Canvas.__init__(self, parent.interior, relief='raised', bd=2, 
            width=300, height=200, highlightthickness=0, cursor='arrow')
        if flickerbg == None:
            self.flickerbg = self.cget('bg')
        if sys.platform == 'win32': 
            if topcolor == None:         topcolor='SystemActiveCaption'
            if inactivetopcolor == None: inactivetopcolor='SystemInactiveCaption'
        if topcolor == None:             topcolor="#00008b"           #like win98
        if inactivetopcolor == None:     inactivetopcolor="#808080"   #like win98
        self.topcolor, self.inactivetopcolor = topcolor, inactivetopcolor
        self.id = parent.interior.create_window(0, 0, window=self, anchor="nw")
        self.bind("<Motion>", self.startResize)
        self.bind("<ButtonPress-1>", self.setFocus)
        self.bind("<B1-Motion>", self.resize)
        self.bind("<ButtonRelease-1>", self.stopResize)
        self.parent = parent
        self.state = "normal"
        self.b1motionState = "translating"
        self.lastx = self.lasty = 0

        self.top = self.create_rectangle(3, 3, 700, 20, outline=self.topcolor, fill=self.topcolor)  
        self.tag_bind(self.top, "<ButtonPress-1>", self.press)
        self.tag_bind(self.top, "<Double-Button-1>", self.maximize)
        self.tag_bind(self.top, "<B1-Motion>", self.move)
        self.tag_bind(self.top, "<ButtonPress-3>", self.showmenu)
        self.tag_bind(self.top, "<Motion>", self.arrow)
        self.image = PhotoImage(file=iconfile)
        self.icon = self.create_image(5, 7, image=self.image, anchor=NW)
        self.tag_bind(self.icon, "<ButtonPress-1>", self.showmenu, "+")
        self.tag_bind(self.icon, "<ButtonPress-3>", self.showmenu, "+")
        self.tag_bind(self.icon, "<Motion>", self.arrow, "+")
        if sys.platform == 'win32': ypos=5; font=('MS Sans Serif', 8, 'bold')
        else:                       ypos=7; font=('Helvetica', 9, 'bold')
        self.title = self.create_text(23,ypos, text=title, fill='white', 
            anchor=NW, font=font)
        self.tag_bind(self.title, "<ButtonPress-1>", self.press, "+")
        self.tag_bind(self.title, "<Double-Button-1>", self.maximize)
        self.tag_bind(self.title, "<B1-Motion>", self.move, "+")
        self.tag_bind(self.title, "<ButtonPress-3>", self.showmenu, "+")
        self.tag_bind(self.title, "<Motion>", self.arrow, "+")

        self.closeIcon = PhotoImage(file=path+'close.gif')
        self.closeButton = Button(self, image=self.closeIcon, 
            command=self.close, width=9, height=7)
        self.closeButton.bind("<Motion>", self.arrow)
        self.maximizeIcon = PhotoImage(file=path+'maximize.gif')
        self.maximizeButton = Button(self, image=self.maximizeIcon, 
            command=self.maximize, width=9, height=7)
        self.maximizeButton.bind("<Motion>", self.arrow)
        self.restoreIcon = PhotoImage(file=path+'restore.gif')
        self.restoreButton = Button(self, image=self.restoreIcon, 
            command=self.restore, width=9, height=7)
        self.restoreButton.bind("<Motion>", self.arrow)
        self.minimizeIcon = PhotoImage(file=path+'minimize.gif')
        self.minimizeButton = Button(self, image=self.minimizeIcon, 
            command=self.minimize, width=9, height=7)
        self.minimizeButton.bind("<Motion>", self.arrow)

        w, h = self.winfo_width(), self.winfo_height()
        self.interior = Frame(self, cursor='arrow', bg=self.flickerbg)
        self.interior.place(x=3, y=22, anchor=NW, width=w-7, height=h-27) 
        self.interior.bind("<ButtonPress-1>", self.setFocus)
        self.paint()

        self.parentclose = Button(self.parent.menubar, image=self.closeIcon, 
            command=self.close, width=9, height=7)
        self.parentrestore = Button(self.parent.menubar, image=self.restoreIcon, 
            command=self.restore, width=9, height=7)
        self.parentminimize = Button(self.parent.menubar, image=self.minimizeIcon, 
            command=self.minimize, width=9, height=7)

        m = Pmw.MenuBar(hull_borderwidth = 0, hotkeys=1)
        m.addmenu('State', '')
        m.addmenuitem('State', 'command', label = 'Restore', command=self.restore)
        m.addmenuitem('State', 'command', label = 'Move')
        m.addmenuitem('State', 'command', label = 'Size')
        m.addmenuitem('State', 'command', label = 'Minimize', command=self.minimize)
        m.addmenuitem('State', 'command', label = 'Maximize', command=self.maximize)
        m.addmenuitem('State', 'separator')
        m.addmenuitem('State', 'command', label = 'Close', command=self.close, 
            accelerator="Alt+F4")
        self.menu = m.component('State-menu')
        self.setRestoreState()
        self.setFocus()

    def widgetSetFocus(self, widget):    #Use this after you put pack (etc) children in MDIChild!!
        widget.bind("<ButtonPress-1>", self.setFocus)

    def setFocus(self, event=None):
        print("setFocus")
        p = self.parent
        p.unFocusChildren()
        self.itemconfig(self.top, fill=self.topcolor, 
            outline=self.topcolor)
        p.activechild = self
        Misc.tkraise(self)   

    def showmenu(self, event):
        self.setFocus()
        x = int(self.winfo_rootx()+event.x)
        y = int(self.winfo_rooty()+event.y)
        self.menu.tk_popup(x, y)

    def paint(self, event=None):
        self.update() 
        w, h = self.winfo_width(), self.winfo_height()
        if self.state == 'normal':
            self.restoreButton.place_forget()
            self.closeButton.place(x=w-5, y=5, anchor=NE) 
            self.maximizeButton.place(x=w-23, y=5, anchor=NE) 
            self.minimizeButton.place(x=w-39, y=5, anchor=NE) 
        else:
            self.minimizeButton.place_forget()
            self.closeButton.place(x=w-5, y=5, anchor=NE) 
            self.maximizeButton.place(x=w-23, y=5, anchor=NE) 
            self.restoreButton.place(x=w-39, y=5, anchor=NE) 
        self.interior.place(x=3, y=22, anchor=NW, width=w-7, height=h-27) 

    def arrow(self, event):
        self.config(cursor='arrow')

    def changeCursor(self, win32=None, other=None):
        if sys.platform == 'win32' and win32 != None: 
            self.config(cursor=win32)            
        else: 
            self.config(cursor=other) 
 
    def startResize(self, event):
        ex, ey = event.x, event.y
        w, h = self.winfo_width(), self.winfo_height()
        t = 5
        if (ey < 20 and ex < t) or (ey < t and ex < 20):			
            self.changeCursor(win32='size_nw_se', other='top_left_corner') 
            self.b1motionState = "topleft" 
        elif (ey > h-20 and ex > w-t) or (ey > h-t and ex > w-20):
            self.changeCursor(win32='size_nw_se', other='bottom_right_corner') 
            self.b1motionState = "bottomright" 	
        elif (ey < 20 and ex > w-t) or (ey < t and ex > w-20):		
            self.changeCursor(win32='size_ne_sw', other='top_right_corner')
            self.b1motionState = "topright"  
        elif (ey > h-20 and ex < t) or (ey > h-t and ex < 20):	
            self.changeCursor(win32='size_ne_sw', other='bottom_left_corner')	
            self.b1motionState = "bottomleft"  
        elif (ey < t):
            self.changeCursor(win32='sb_v_double_arrow', other='top_side')
            self.b1motionState = "top" 
        elif (ey > h-t):
            self.changeCursor(win32='sb_v_double_arrow', other='bottom_side')
            self.b1motionState = "bottom" 
        elif (ex < t):
            self.changeCursor(win32='sb_h_double_arrow', other='left_side')
            self.b1motionState = "left" 
        elif (ex > w-t):
            self.changeCursor(win32='sb_h_double_arrow', other='right_side')
            self.b1motionState = "right" 
        else:
            self.b1motionState = "translating" 

    def stopResize(self, event):
        self.b1motionState = "translating"

    def resize(self, event):
        if self.b1motionState == "translating":
            return
        canvas = self.parent.interior
        w, h = canvas.winfo_width(), canvas.winfo_height()
        xmouse, ymouse = self.winfo_x()+event.x, self.winfo_y()+event.y
        if xmouse < 0 or xmouse > w or ymouse < 0 or ymouse > h: 
            return
        if self.b1motionState == "topleft":
            self.setSize(topPos=ymouse, leftPos=xmouse)
        elif self.b1motionState == "bottomleft":
            self.setSize(bottomPos=ymouse, leftPos=xmouse)
        elif self.b1motionState == "topright":
            self.setSize(topPos=ymouse, rightPos=xmouse)
        elif self.b1motionState == "bottomright":
            self.setSize(bottomPos=ymouse, rightPos=xmouse)
        elif self.b1motionState == "top":
            self.setSize(topPos=ymouse)
        elif self.b1motionState == "bottom":
            self.setSize(bottomPos=ymouse)
        elif self.b1motionState == "left":
            self.setSize(leftPos=xmouse)
        elif self.b1motionState == "right":
            self.setSize(rightPos=xmouse)

    def setSize(self, leftPos=None, rightPos=None, topPos=None, bottomPos=None):
        w, h = self.winfo_width()-4, self.winfo_height()-4
        x, y = self.winfo_x(), self.winfo_y()
        if rightPos == None:
            rightPos = x+w
        else:
            rightPos = max(rightPos, x+100) 
        if leftPos == None:
            leftPos = x
        else:
            leftPos = min(leftPos, rightPos-100)
        if bottomPos == None:
            bottomPos = y+h
        else:
            bottomPos = max(bottomPos, y+19)
        if topPos == None:
            topPos = y
        else:
            topPos = min(topPos, bottomPos-19)
        self.parent.interior.coords(self.id, leftPos, topPos)
        self.config(width=rightPos-leftPos, height=bottomPos-topPos)
        self.superUpdate()

    def superUpdate(self):
        self.setRestoreState()
        self.restore()        

    def press(self, event):
        self.lastx, self.lasty = event.x, event.y

    def move(self, event):
        if self.b1motionState == "translating":
            canvas = self.parent.interior
            w, h = canvas.winfo_width(), canvas.winfo_height()
            xmouse, ymouse = self.winfo_x()+event.x, self.winfo_y()+event.y
            if xmouse > 0 and xmouse < w and ymouse > 0 and ymouse < h:
                x = event.x_root - canvas.winfo_rootx() - self.lastx
                y = event.y_root - canvas.winfo_rooty() - self.lasty
                canvas.coords(self.id, x, y)

    def delIcons(self):
        self.parentclose.pack_forget()
        self.parentrestore.pack_forget()
        self.parentminimize.pack_forget()

    def setRestoreState(self):
        if self.state == 'normal':
            self.restoreX, self.restoreY = self.winfo_x(), self.winfo_y()
            self.restoreWidth, self.restoreHeight = self.winfo_width()-4, self.winfo_height()-4
            self.restoreState = self.state

    def minimize(self):
        self.setRestoreState()
        self.delIcons()
        p = self.parent
        p.nonMinimized.remove(self)
        p.minimizedChildren.append(self)
        p.repackMinimized()
        self.config(width=150, height=19)
        self.state = 'minimized'
        if len(p.childlist) > 0:
            p.childlist[0].setFocus()
        self.paint()

    def maximize(self, event=None):
        if self in self.parent.minimizedChildren:
            self.parent.minimizedChildren.remove(self)
        self.setRestoreState()
        self.state = 'maximized'
        canvas = self.parent.interior
        self.config(width=canvas.winfo_width()+7, height=canvas.winfo_height()+26)
        canvas.coords(self.id, -6, -25) 
        self.parentclose.pack(side='right', padx=2)
        self.parentrestore.pack(side='right')
        self.parentminimize.pack(side='right')
        self.parent.activechild = self
        self.paint()

    def restore(self):
        if self in self.parent.minimizedChildren:
            self.parent.minimizedChildren.remove(self)
            self.parent.nonMinimized.append(self)
        if self.restoreState == 'maximized':
            self.maximize()
        else:
            self.state = 'normal'
            self.delIcons()
            canvas = self.parent.interior
            canvas.coords(self.id, self.restoreX, self.restoreY)
            self.config(width=self.restoreWidth, height=self.restoreHeight)
            self.paint()

    def close(self):
        self.parentclose.destroy()
        self.parentrestore.destroy()
        self.parentminimize.destroy()
        p = self.parent
        p.childlist.remove(self)
        p.nonMinimized.remove(self)
        if len(p.childlist) > 0:
            p.childlist[0].setFocus()
        else:
            p.activechild = None
        self.image = self.minimizeIcon = None
        self.maximizeIcon = self.closeIcon = self.restoreIcon = None
        self.destroy()


class OrientedFrame(Frame):
    def __init__(self, parent, orient='horz', **kw):
        Frame.__init__(self, parent, kw)
        self.orient = orient
          

class MDIParent(Tk):
    def __init__(self, title='', interior_bg='#808080'):
        Tk.__init__(self)
        self.interior_bg = interior_bg
        self.title(title)
        self.lastx = self.lasty = None
        self.childlist = []
        self.activechild = None        

        self.menubar = Frame(self)
        self.menubar.pack(fill='x')

        self.topline = Canvas(self, bg='grey', height=2)
        self.topline.pack(fill='x')
        self.topline.create_line(0,2,1000,2, fill='#808080') 
        self.topline.create_line(0,3,1000,3, fill='white')      
        self.topspace = OrientedFrame(self, orient='horz')
        self.topspace.pack(fill='x')
        
        self.middle = Canvas(self, bg='grey', highlightthickness=0)
        self.middle.pack(fill='both', expand=1)
        self.middle.bind("<Configure>", self.paint)
        self.interior = Canvas(self.middle, bg=self.interior_bg, highlightthickness=0)
        self.leftspace = OrientedFrame(self.middle, orient='vert')
        self.leftspace.pack(side='left', fill='y', pady=4)
        self.rightspace = OrientedFrame(self.middle, orient='vert')
        self.rightspace.pack(side='right', fill='y', pady=4)

        self.statusbar = Frame(self)
        self.statusbar.pack(side='bottom', fill='x')
        self.cornerIcon = PhotoImage(file=path+'corner.gif')
        self.corner = Label(self.statusbar, image=self.cornerIcon)
        self.corner.pack(side='right', anchor=SE)        
        self.progress = ProgressBar(self.statusbar, height=12)
        self.progress.pack(side='right', padx=11, anchor=SE)   
        self.geometry("%dx%d" % (400,300))
        self.lastw = self.lasth = None
        self.minimizedChildren = []
        self.nonMinimized = []

    def paint(self, event=None):
        self.middle.delete(ALL)
        h = self.middle.winfo_height()
        w = self.middle.winfo_width()
        lw = self.leftspace.winfo_width()+1
        rw = self.rightspace.winfo_width()+2

        self.middle.create_line(0,2,w,2, fill='#808080') 
        self.middle.create_line(0,3,w,3, fill='white') 
        self.middle.create_line(lw,3,w-rw,3, fill='black') 

        self.middle.create_line(0,h-4,w,h-4, fill='#808080') 
        self.middle.create_line(lw,h-4,w-rw,h-4, fill='lightgrey') 
        self.middle.create_line(0,h-3,w,h-3, fill='white') 

        self.middle.create_line(lw-1,3,lw-1,h-4, fill='#808080') 
        self.middle.create_line(lw,3,lw,h-4, fill='black') 

        self.middle.create_line(w-rw,3,w-rw,h-3, fill='lightgrey') 
        self.middle.create_line(w-rw+1,3,w-rw+1,h-3, fill='white') 
        
        self.middle.create_rectangle(lw+1,4,w-rw-1,h-5, fill=self.interior_bg, 
            outline=self.interior_bg)
        self.interior.config(width=w-rw-lw-1, height=h-8)
        self.interior.place(x=lw+1, y=4, anchor=NW)  

        # make maximized children's w, h follow resizing in x and y
        if self.lastw != None:
            for child in self.childlist:
                if child.state == 'maximized':
                    cw, ch = child.winfo_width(), child.winfo_height()
                    child.config(width=cw+w-self.lastw, height=ch+h-self.lasth)
        self.repackMinimized()
        self.lastw, self.lasth = w, h

    def unFocusChildren(self):   
        for child in self.childlist:
            child.itemconfig(child.top, fill=child.inactivetopcolor, 
                outline=child.inactivetopcolor)
        
    def newChild(self, title='tk', iconfile=path+'tk.gif'):
        state = None
        if self.activechild != None:
            state = self.activechild.state
            if state == 'maximized':
                self.activechild.restore()
        self.activechild = MDIChild(self, title=title, iconfile=iconfile)
        if state == 'maximized': 
            self.activechild.maximize()
        self.childlist.append(self.activechild)
        self.nonMinimized.append(self.activechild)
        return self.activechild

    def repackMinimized(self):
        for window in self.minimizedChildren:
            index = self.minimizedChildren.index(window)
            w, h = self.interior.winfo_width(), self.interior.winfo_height()
            xslots = int(w/154)
            if xslots == 0: xslots = 1
            layer = int(index/xslots)     # from 0 and up
            xslot = index%xslots  		# from 0 to xslots-1
            ycoord = h-(layer+1)*23
            self.interior.coords(window.id, xslot*154, ycoord)
        if self.minimizedChildren == []:
            return self.interior.winfo_height()
        else:
            return ycoord

    def cascadeChildren(self):
        self.tileChildren()
        i = 0
        for child in self.nonMinimized:
            if child != self.activechild:
                self.interior.coords(child.id, i*21, i*21)                
                child.config(width=300, height=200)
                Misc.tkraise(child)
                child.superUpdate()
                i = i + 1
        self.interior.coords(self.activechild.id, i*21, i*21)
        self.activechild.config(width=300, height=200)
        Misc.tkraise(self.activechild)
        self.activechild.superUpdate()

    def tileChildrenSystematically(self):         
        tot = len(self.nonMinimized)
        slots = int(tot/2)  
        w = self.interior.winfo_width()/slots
        h = self.repackMinimized()/slots
        for window in self.nonMinimized:
            index = self.nonMinimized.index(window)
            layer = int(index/slots)         # from 0 and up
            slot = index%slots  		   # from 0 to slots-1           
            self.interior.coords(window.id, w*slot, h*layer)              
            window.config(width=w-4, height=h-4) 
            window.superUpdate()

    def tileChildren(self):
        w = self.interior.winfo_width()
        h = self.repackMinimized()        
        tot = len(self.nonMinimized)
        if tot == 1:
            for child in self.nonMinimized:
                self.interior.coords(child.id, 0, 0)                
                child.config(width=w-4, height=h-4)
        elif tot == 2:
            i = 0
            for child in self.nonMinimized:
                self.interior.coords(child.id, i*w/2, 0)                
                child.config(width=w/2-4, height=h-4)
                i = i + 1
        elif tot == 3:
            i = 0
            for child in self.nonMinimized:
                if i == 0:
                    self.interior.coords(child.id, 0, 0)                
                    child.config(width=w/2-4, height=h-4)
                elif i == 1 or i == 2:
                    self.interior.coords(child.id, w/2, (i-1)*h/2)                
                    child.config(width=w/2-4, height=h/2-4)
                i = i + 1
        elif tot == 4:
            i = 0
            for child in self.nonMinimized:
                if i == 0 or i == 1:
                    self.interior.coords(child.id, 0, i*h/2)                
                elif i == 2 or i == 3:
                    self.interior.coords(child.id, w/2, (i-2)*h/2)               
                child.config(width=w/2-4, height=h/2-4)
                i = i + 1
        for child in self.nonMinimized:
            child.superUpdate()
        if tot > 4:
            self.tileChildrenSystematically()


def printhi():
    print('hi')


def putTree(document):
    m = Pmw.MenuBar(hull_borderwidth = 0, hotkeys=1)
    m.addmenu('File', '')
    m.addmenuitem('File', 'command', label = 'New')
    m.addmenuitem('File', 'command', label = 'Open')
    File = m.component('File-menu')

    f = path+'folder.gif'
    of = path+'openfolder.gif'
    tree = Tree(document.interior, icon=f, activeicon=of, name='tree', menu=File, command=printhi)
    top=tree.child[0]
    top.state='expanded'
    t1=top.addChild(tree, menu=File, icon=f, activeicon=of, name='t1', command=printhi)
    t2=top.addChild(tree, menu=File, icon=f, activeicon=of, name='t2', command=printhi)
    t3=top.addChild(tree, menu=File, icon=f, activeicon=of, name='t3', command=printhi)
    c1=t1.addChild(tree, menu=File, icon=f, activeicon=of, name='c1', command=printhi)
    c2=t2.addChild(tree, menu=File, icon=f, activeicon=of, name='c2', command=printhi)
    c3=t3.addChild(tree, menu=File, icon=f, activeicon=of, name='c3', command=printhi)
    d1=c1.addChild(tree, menu=File, icon=f, activeicon=of, name='d1', command=printhi)  
    d3=c3.addChild(tree, menu=File, icon=f, activeicon=of, name='d3', command=printhi) 
    
    document.widgetSetFocus(tree)  ## important for setting focus to MDIChild ##



if __name__ == '__main__':
    from FlatButtons import FlatRadiogroup
    from Tree import Tree
    from Toolbar import Toolbar

    App=MDIParent(title='MDIParent')
    App.geometry("%dx%d" % (500,400))
    spaces = [App.topspace, App.leftspace, App.rightspace]

    v = StringVar()
    v.set("line")
    t = Toolbar(App.topspace, dockingspaces=spaces, title="Sketch")

    stateGroup = FlatRadiogroup(variable=v)
    t.sendFlatRadioGroup(groupname='stateGroup', group=stateGroup)
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'select.gif', valuename='select')
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'draw.gif', valuename='line')
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'circle.gif', valuename='circle')
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'rect.gif', valuename='rect')
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'cut.gif', valuename='cut')
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'zoomToArea.gif', valuename='toarea')
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'zoom.gif', valuename='zoom')  
    t.addFlatRadiobutton(groupname='stateGroup', imagefile=path+'trans.gif', valuename='translate')
    
    menuBar = Pmw.MenuBar(App.menubar, hull_borderwidth=0, hotkeys=1)
    menuBar.pack(side='left', fill='x')
    File = menuBar.addmenu('File', 'Hi')
    menuBar.addmenuitem('File', 'command', label='New', command=App.newChild)
    menuBar.addmenuitem('File', 'separator')
    menuBar.addmenuitem('File', 'command', label='Cascade', command=App.cascadeChildren)
    menuBar.addmenuitem('File', 'command', label='Tile', command=App.tileChildren)

    teststatusbar = Label(App.statusbar, text='Statusbar')
    teststatusbar.pack(side='left')    
    
    child1 = App.newChild(title='MDIChild1', iconfile=path+'tk.gif')
    putTree(child1)      
    child2 = App.newChild(title='MDIChild2', iconfile=path+'tk.gif') 
    putTree(child2) 

    App.mainloop()

