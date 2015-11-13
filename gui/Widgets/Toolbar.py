from tkinter import *
from FlatButtons import Flatbutton, FlatRadiogroup
from iconPath import path

class OrientedToplevel(Toplevel):
    def __init__(self, orient='horz'):
        Toplevel.__init__(self)
        self.orient = orient

class Toolbar:
    def __init__(self, parent, dockingspaces=None, title=None):
        self.parent = parent
        self.dockingspaces = dockingspaces
        self.title = title
        self.buttons = []
        self.docked = 'true'
        self.frame = Frame() 
        self.float = Toplevel()
        self.float.withdraw()
        self.horztab = PhotoImage(file=path+'horztab.gif')
        self.activehorztab = PhotoImage(file=path+'activehorztab.gif')
        self.verttab = PhotoImage(file=path+'verttab.gif')
        self.activeverttab = PhotoImage(file=path+'activeverttab.gif')
        self.horzsep = PhotoImage(file=path+'horzsep.gif')
        self.vertsep = PhotoImage(file=path+'vertsep.gif')
        self.none = lambda: None

    def dock(self, space):
        self.docked = 'true'
        self.parent = space
        self.attach(space)
        self.float.destroy()

    def undock(self, event):
        self.docked = 'false'
        self.float = OrientedToplevel()
        self.float.orient = self.parent.orient
        self.float.transient(self.parent)
        self.float.resizable(0,0)
        self.attach(self.float)
        self.float.focus_set()
        x, y = self.parent.winfo_rootx(), self.parent.winfo_rooty()
        self.float.geometry("+%d+%d" % (x+event.x, y+event.y))

    def b1down(self, event):
        if self.docked == 'true':
            self.undock(event)

    def b1motion(self, event):
        if self.docked == 'false':
            x, y = self.float.winfo_x(), self.float.winfo_y()
            if x != 0:
                self.float.geometry("+%d+%d" % (x+event.x, y+event.y))
         
    def b1up(self, event):
        if self.docked == 'false':
            for space in self.dockingspaces:
                if self.insideSpace(space) == 'true':
                    self.dock(space)
                    break

    def insideSpace(self, space):
        spacex0, spacey0 = space.winfo_rootx(), space.winfo_rooty()
        spacex1, spacey1 = spacex0 + space.winfo_width(), spacey0 + space.winfo_height()        
        x, y = self.float.winfo_rootx(), self.float.winfo_rooty()
        if x > spacex0 and x < spacex1 and y > spacey0 and y < spacey1:
            return 'true'
        else:
            return 'false'   

    def entertab(self, event):
        if self.parent.orient == 'horz':
            self.tab.config(image=self.activehorztab)
        else:
            self.tab.config(image=self.activeverttab)

    def leavetab(self, event):
        if self.parent.orient == 'horz':
            self.tab.config(image=self.horztab)
        else:
            self.tab.config(image=self.verttab)
             
    def attach(self, space):
        self.frame.destroy()
        self.frame = Frame(space)
        if space.orient == 'horz':
            self.float.title(self.title) 
            self.frame.pack(side='left', anchor=NW)
            self.tab = Label(self.frame, image=self.horztab)
            self.tab.pack(side='left', anchor=NW)
        else:
            self.float.title('')
            self.frame.pack(side='top', anchor=NW)
            self.tab = Label(self.frame, image=self.verttab)
            self.tab.pack(side='top', anchor=NW)
        self.tab.bind("<Enter>", self.entertab)
        self.tab.bind("<Leave>", self.leavetab)
        self.tab.bind("<ButtonPress-1>", self.b1down)
        self.tab.bind("<B1-Motion>", self.b1motion)
        self.tab.bind("<ButtonRelease-1>", self.b1up)
        for line in self.buttons: 
            #print line
            exec(line)

    def addFlatbutton(self, imagefile=None, commandname=None):
        line = "Flatbutton(self.frame, imagefile='%s', command=self.%s, \
            orient=self.parent.orient)" % (imagefile, commandname)
        self.buttons.append(line)
        self.attach(self.parent)

    def addFlatRadiobutton(self, groupname=None, imagefile=None, commandname='none', valuename=None):
        # before you create a new Modebutton, 
        # delete reference to old one in its group.buttonList
        # use imagefile as identifier
        line =        "for button in self.%s.buttonList[:]:      \n" % groupname
        line = line + "    if button.imagefile == '%s':          \n" % imagefile 
        line = line + "        self.%s.buttonList.remove(button) \n" % groupname 
        self.buttons.append(line)         
        self.buttons.append( "self.%s.addButton(self.frame, imagefile='%s', command=self.%s, value='%s', \
            orient=self.parent.orient)" % (groupname, imagefile, commandname, valuename) )
        self.attach(self.parent)

    def addSeparator(self):
        self.buttons.append( "if space.orient == 'horz': \
            Label(self.frame, image=self.horzsep).pack(side='left', anchor=NW)" )
        self.buttons.append( "if space.orient == 'vert': \
            Label(self.frame, image=self.vertsep).pack(side='top', anchor=NW)" )
        self.attach(self.parent)

    def sendFlatRadioGroup(self, groupname=None, group=None):
        exec("self.%s = group" % groupname)

    def sendCommand(self, commandname=None, command=None):
        exec("self.%s = command" % commandname)
        
def printhi():
    print('hi')

if __name__ == '__main__':
    from MDI import MDIParent

    App = MDIParent(title='MDI')
    spaces = [App.topspace, App.leftspace, App.rightspace]

    t1 = Toolbar(App.topspace, dockingspaces=spaces, title='File')
    t1.sendCommand(commandname='printhi', command=printhi)
    t1.addFlatbutton(imagefile=path+'new.gif', commandname='printhi')
    t1.addFlatbutton(imagefile=path+'open.gif', commandname='printhi')
    t1.addFlatbutton(imagefile=path+'save.gif', commandname='printhi')

    v=IntVar()
    v.set(1)
    t2 = Toolbar(App.leftspace, dockingspaces=spaces, title='Edit')
    viewGroup = FlatRadiogroup(variable=v)
    t2.sendFlatRadioGroup(groupname='viewGroup', group=viewGroup)
    t2.sendCommand(commandname='printhi', command=printhi)
    t2.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'draw.gif', commandname='printhi', valuename='1')
    t2.addSeparator() 
    t2.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'select.gif', commandname='printhi', valuename='2')
    t2.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'rect.gif', commandname='printhi', valuename='3')
    t2.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'circle.gif', commandname='printhi', valuename='4')

    d=IntVar()
    d.set(1)
    t3 = Toolbar(App.rightspace, dockingspaces=spaces, title='Display')
    displayGroup = FlatRadiogroup(variable=d)
    t3.sendFlatRadioGroup(groupname='displayGroup', group=displayGroup)
    t3.sendCommand(commandname='printhi', command=printhi)
    t3.addFlatRadiobutton(groupname='displayGroup', imagefile=path+'wire.gif', commandname='printhi', valuename='1')
    t3.addFlatRadiobutton(groupname='displayGroup', imagefile=path+'stick.gif', commandname='printhi', valuename='2')
    t3.addFlatRadiobutton(groupname='displayGroup', imagefile=path+'ballstick.gif', commandname='printhi', valuename='3')
    t3.addFlatRadiobutton(groupname='displayGroup', imagefile=path+'sphere.gif', commandname='printhi', valuename='4')
    t3.addFlatRadiobutton(groupname='displayGroup', imagefile=path+'surface.gif', commandname='printhi', valuename='5')

    t4 = Toolbar(App.topspace, dockingspaces=spaces, title='View')
    t4.sendCommand(commandname='printhi', command=printhi)
    t4.sendFlatRadioGroup(groupname='viewGroup', group=viewGroup)
    t4.addFlatbutton(imagefile=path+'toscreen.gif', commandname='printhi')
    t4.addFlatbutton(imagefile=path+'toselection.gif', commandname='printhi')
    t4.addSeparator()
    t4.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'zoomToArea.gif', commandname='printhi', valuename='5')
    t4.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'zoom.gif', commandname='printhi', valuename='6')
    t4.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'rotate.gif', commandname='printhi', valuename='7')
    t4.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'rotz.gif', commandname='printhi', valuename='8')
    t4.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'trans.gif', commandname='printhi', valuename='9')
    t4.addFlatRadiobutton(groupname='viewGroup', imagefile=path+'zclip.gif', commandname='printhi', valuename='10')  

    App.mainloop()