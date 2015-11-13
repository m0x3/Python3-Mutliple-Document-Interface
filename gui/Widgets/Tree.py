from tkinter import *
import Pmw
from iconPath import path

class Node:
    def __init__(self, parent, tree, menu=None, icon=None, 
                 activeicon=None, name=None, command=None):
        self.parent, self.tree = parent, tree
        self.menu = menu
        self.icon = PhotoImage(file=icon)
        self.activeicon = PhotoImage(file=activeicon)
        self.width, self.height = 1.5*self.icon.width(), 1.5*self.icon.height()
        self.name = name
        self.var = StringVar()
        self.var.set(name)
        self.text = Entry(tree, textvariable=self.var, bg=tree.bg, bd=0, width=len(name)+2, 
            font=tree.font, fg=tree.textcolor, insertwidth=1, highlightthickness=1, 
            highlightbackground=tree.bg, selectbackground="#044484", selectborderwidth=0,
            selectforeground='white')
        self.command = command
        self.x = self.y = 0  #where you draw expandable node, or icon if root or leaf
        self.child = []
        self.state = 'contracted'
        self.selected = 'false'

    def addChild(self, tree, menu=None, icon=None, activeicon=None, name=None, command=None):    
        child = Node(self, tree, menu, icon, activeicon, name, command) 
        self.child.append(child)
        self.tree.display()
        return child         

    def deleteChild(self, child):    
        self.child.remove(child)
        self.tree.display()

    def textForget(self):
        self.text.place_forget()
        for child in self.child:
            child.textForget()                

    def deselect(self):
        self.selected = 'false'
        for child in self.child:
            child.deselect()

    def showmenu(self, event=None):
        x = int(self.tree.winfo_rootx()+self.x)
        y = int(self.tree.winfo_rooty()+self.y)
        self.menu.tk_popup(x, y)

    def boxpress(self, event=None):
        if self.state == 'expanded':
            self.state = 'contracted'
        elif self.state == 'contracted':
            self.state = 'expanded'
        self.tree.display()
 
    def invoke(self, event=None):
        if self.selected == 'false':
            self.tree.deselectall()
            self.selected = 'true'
            self.tree.display()
            self.command()
        self.name = self.text.get()
        self.text.config(width=len(self.name)+2)

    def displayIconText(self):
        tree, text = self.tree, self.text
        if self.selected == 'true':
            self.pic = tree.create_image(self.x, self.y, image=self.activeicon)
        else:
            self.pic = tree.create_image(self.x, self.y, image=self.icon)
        text.place(x=self.x+self.width/2, y=self.y, anchor=W)
        text.bind("<ButtonPress-1>", self.invoke)
        tree.tag_bind(self.pic, "<ButtonPress-1>", self.invoke, "+")
        text.bind("<ButtonPress-3>", self.showmenu)
        tree.tag_bind(self.pic, "<ButtonPress-3>", self.showmenu, "+")
        text.bind("<Double-Button-1>", self.boxpress)
        tree.tag_bind(self.pic, "<Double-Button-1>", self.boxpress, "+")

    def displayRoot(self):
        if self.state == 'expanded':                        
            for child in self.child:
                child.display()            
        self.displayIconText()

    def displayLeaf(self):
        self.tree.hline(self.y, self.parent.x+1, self.x)
        self.tree.vline(self.parent.x, self.parent.y, self.y)
        self.displayIconText()

    def displayBranch(self):
        parent, tree = self.parent, self.tree
        x, y = self.x, self.y            
        tree.hline(y, parent.x, x)           
        tree.vline(parent.x, parent.y, y)
        if self.state == 'expanded' and self.child != []:           
            for child in self.child:
                child.display()                
            box = tree.create_image(parent.x, y, image=tree.minusnode)    
        elif self.state == 'contracted' and self.child != []: 
            box = tree.create_image(parent.x, y, image=tree.plusnode) 
        tree.tag_bind(box, "<ButtonPress-1>", self.boxpress, "+")
        self.displayIconText()

    def findLowestChild(self, node):
        if node.state == 'expanded' and node.child != []:
            return self.findLowestChild(node.child[-1])
        else:
            return node        

    def display(self):
        parent, tree = self.parent, self.tree
        n = parent.child.index(self)
        self.x = parent.x + self.width
        if n == 0:
            self.y = parent.y + (n+1)*self.height
        else:    
            previous = parent.child[n-1]            
            self.y = self.findLowestChild(previous).y + self.height
        if parent == tree:
            self.displayRoot()
        elif parent.state == 'expanded':
            if self.child == []:
                self.displayLeaf() 
            else:        
                self.displayBranch()
            tree.lower('line')


class Tree(Canvas):
    def __init__(self, parent, icon, activeicon, name, menu, command, bg='white', relief='sunken', bd=2, 
                 linecolor='#808080', textcolor='black', font=('MS Sans Serif', 8)):
        Canvas.__init__(self, parent, bg=bg, relief=relief, bd=bd, highlightthickness=0)
        self.pack(side='left', anchor=NW, fill='both', expand=1)
        self.bg, self.font= bg, font
        self.linecolor, self.textcolor= linecolor, textcolor
        self.parent = parent 
        self.plusnode = PhotoImage(file=path+'plusnode.gif')
        self.minusnode = PhotoImage(file=path+'minusnode.gif')
        self.child = []
        self.x = self.y = -10
        self.child.append( Node( self, self, menu=menu, command=command,
            icon=icon, activeicon=activeicon, name=name) )      

    def display(self):
        self.delete(ALL)
        for child in self.child:
            child.textForget()
            child.display()

    def deselectall(self):
        for child in self.child:
            child.deselect()

    def vline(self, x, y, y1):
        for i in range(0, int(abs(y-y1)), 2):
            self.create_line(x, y+i, x, y+i+1, fill=self.linecolor, tags='line')
         
    def hline(self, y, x, x1):
        for i in range(0, int(abs(x-x1)), 2):
            self.create_line(x+i, y, x+i+1, y, fill=self.linecolor, tags='line')


class ScrolledTree(Pmw.ScrolledCanvas):
    def __init__(self, parent, icon, activeicon, name, menu, command, bg='white', 
                 relief='sunken', bd=2, linecolor='#808080', textcolor='black', 
                 font=('MS Sans Serif', 8)):
        Pmw.ScrolledCanvas.__init__(self, parent)
        self.component['canvas'] = Tree(parent, icon=icon, activeicon=activeicon, name=name, menu=menu, command=command)


def printhi():
    print('hi')

if __name__ == "__main__":
    root=Tk()

    m = Pmw.MenuBar(hull_borderwidth = 0, hotkeys=1)
    m.addmenu('File', '')
    m.addmenuitem('File', 'command', label = 'New')
    m.addmenuitem('File', 'command', label = 'Open')
    File = m.component('File-menu')

    f = path+'folder.gif'
    of = path+'openfolder.gif'
    tree = Tree(root, icon=f, activeicon=of, name='tree', menu=File, command=printhi)
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

    root.mainloop()