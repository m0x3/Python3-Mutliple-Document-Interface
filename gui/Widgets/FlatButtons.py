from tkinter import *
import time
from iconPath import path

class Flatbutton(Label):
    def __init__(self, parent, imagefile=None, command=None, statushelp='', balloonhelp='',
                 statusbar=None, balloon=None, orient='horz', ht=21, wd=21, bd=1, 
                 activebackground='lightgrey', padx=0, pady=0, state='normal'):
        Label.__init__(self, parent, height=ht, width=wd, relief='flat', bd=bd)
        self.bg = self.cget('bg')
        self.activebackground = activebackground
        if imagefile != None:
            self.Icon = PhotoImage(file=imagefile)
            self.config(image=self.Icon)
        self.command = command
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<ButtonPress-1>", self.b1down)
        self.bind("<ButtonRelease-1>", self.b1up)
        if statusbar != None:
            statusbar.bind(self, statushelp)
        if balloon != None:
            balloon.bind(self, balloonhelp)
        if orient == 'horz':
            self.pack(side='left', anchor=NW, padx=padx, pady=pady)
        elif orient == 'vert':
            self.pack(side='top', anchor=NW, padx=padx, pady=pady)     
        self.state = state    
      
    def enter(self, event):
        if self.state != 'disabled':
            self.config(relief='raised', bg=self.bg)

    def leave(self, event):
        if self.state != 'disabled':
            self.config(relief='flat', bg=self.bg)

    def b1down(self, event):
        if self.state != 'disabled':
            self.config(relief='sunken', bg=self.activebackground)
    
    def b1up(self, event):
        if self.state != 'disabled':
            if self.command != None:
                self.command()
            time.sleep(0.05)
            self.config(relief='raised', bg=self.bg)  

    def enable(self):
        self.state = 'normal'

    def disable(self):
        self.state = 'disabled'


class FlatRadiobutton(Label):  
    def __init__(self, parent, group=None, imagefile=None, command=None, value=None, 
                 statushelp=None, balloonhelp=None, orient='horz', buttonMenu=None, 
                 state='normal'):
        Label.__init__(self, parent)
        self.bg = self.cget('bg')
        self.imagefile = imagefile
        self.parent, self.command  = parent, command
        self.group, self.value = group, value
        self.orient = orient
        self.buttonMenu, self.down = buttonMenu, 'false'
        self.Icon = PhotoImage(file=imagefile)
        self.config(image=self.Icon, height=group.bht, width=group.bwd, bd=1)
        if self.value == self.group.variable.get():
            self.config(relief='sunken', bg=group.activebackground)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<ButtonPress-1>", self.b1down)
        self.bind("<ButtonRelease-1>", self.b1up)
        #if group.statusbar != None:
        #    group.statusbar.bind(self.Button, statushelp)
        #if group.balloon != None:
        #    group.balloon.bind(self.Button, balloonhelp)
        if orient == 'horz':
            self.pack(side='left', anchor=NW)
        elif orient == 'vert':
            self.pack(side='top', anchor=NW)
        self.state = state

    def enter(self, event):
        if self.group.variable.get() != self.value and self.state != 'disabled':
            self.config(relief='raised', bg=self.bg)

    def leave(self, event):
        if self.group.variable.get() != self.value and self.state != 'disabled':
            self.config(relief='flat',  bg=self.bg)

    def b1down(self, event):
        if self.group.variable.get() != self.value and self.state != 'disabled':
            self.down = 'true'
            self.command()
            self.group.variable.set(self.value)
            self.config(relief='sunken', bg=self.group.activebackground)
            self.group.poprest(self) 
            #self.update_idletasks()
            #self.after(2000, self.buttonMenu)

    def b1up(self, event):
        if self.group.variable.get() == self.value and self.state != 'disabled':
            self.down = 'false'
            #print 'up'
        
    def buttonMenu(self):
        # after time interval from b1press pop up button menu
        # print 'call buttonMenu'
        if self.down == 'true':
            pass #print 'buttonMenu'

    def enable(self):
        self.state = 'normal'

    def disable(self):
        self.state = 'disabled'
        self.config(relief='flat',  bg=self.bg)
     
  
class FlatRadiogroup:
    def __init__(self, variable, statusbar=None, balloon=None, 
                 bht=21, bwd=21, activebackground='lightgrey'):
        self.buttonList = []
        self.variable = variable
        self.statusbar = statusbar
        self.balloon = balloon
        self.bht = bht
        self.bwd = bwd
        self.activebackground = activebackground

    def addButton(self, parent, imagefile, command, value, statushelp='', balloonhelp='', orient='horz'):
        newButton = FlatRadiobutton(parent, self, imagefile, command, value, statushelp, balloonhelp, orient)
        self.buttonList.append(newButton)
        return newButton     
  
    def poprest(self, pushed):
        for button in self.buttonList:
            if button != pushed:
                button.config(relief='flat', bg='grey')


def printhi():
    print('hi')

if __name__ == '__main__':
    root = Tk()
    root.title('Flatbuttons test')
    from MDI import OrientedFrame
    frame = OrientedFrame(root)
    frame.pack(side=LEFT, anchor=NW)
    open=Flatbutton(frame, imagefile=path+'open.gif', command=printhi)
    v=IntVar()
    v.set(1)
    group = FlatRadiogroup(variable=v)
    open2=group.addButton(frame, imagefile=path+'draw.gif', command=printhi, value=1)
    open3=group.addButton(frame, imagefile=path+'select.gif', command=printhi, value=2)
    root.mainloop()

