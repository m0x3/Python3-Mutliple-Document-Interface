from tkinter import *
import time

class ProgressBar(Label):
    def __init__(self, parent, totalticks=1, spacing=4, color="#00008b", 
                 relief='sunken', bd=1, width=120, height=12, bg='grey',
                 textcolor='white', font=("MS Sans Serif", 8), **kw):
        Label.__init__(self, parent, kw, relief=relief, bd=bd, bg=bg)
        self.pack(side='left', anchor=NW, padx=2)       
        self.parent = parent
        self.canvas = Canvas(self, width=width, height=height)        
        self.canvas.pack(side='left', anchor=NW)
        self.totalticks, self.spacing = totalticks, spacing
        self.percentage = self.ticks = 0         
        self.color, self.bg = color, bg
        self.textcolor, self.font = textcolor, font

    def checkIfDone(self):
        self.canvas.update_idletasks()
        if self.percentage >= 0.99 or self.ticks >= self.totalticks:
            time.sleep(0.05)
            self.canvas.delete(ALL)
            self.canvas.update_idletasks()

    def doPercentage(self, percentage=None, showText='true'):
        self.canvas.delete(ALL)
        w, h = self.winfo_width(), self.winfo_height()
        self.canvas.create_rectangle(0, 0, w*percentage, h,
            fill=self.color, outline=self.color)
        if showText == 'true':
            msg = str(int(percentage*100)) + "%"
            self.canvas.create_text(w/2+1, h/2, text=msg, fill='black', 
                font=self.font)
            self.canvas.create_text(w/2, h/2-1, text=msg, fill=self.textcolor, 
                font=self.font)
        self.checkIfDone()

    def doTicks(self, ticks=None):
        self.canvas.delete(ALL)
        sp = self.spacing
        w = self.winfo_width()/self.totalticks - sp
        h = self.winfo_height()
        self.ticks = ticks
        for i in range(0,self.ticks):
            self.canvas.create_rectangle(i*(w+sp), 0, (i+1)*w + i*sp, h, 
                fill=self.color, outline=self.color)      
        self.checkIfDone()

    def addTick(self):
        self.canvas.delete(ALL)          
        sp = self.spacing
        w = self.winfo_width()/self.totalticks - sp
        h = self.winfo_height()
        self.ticks = self.ticks + 1
        for i in range(0,self.ticks):
            self.canvas.create_rectangle(i*(w+sp), 0, (i+1)*w + i*sp, h, 
                fill=self.color, outline=self.color) 
        self.checkIfDone()


def testpercentage(increment=0.01, totaltime=2):
    steps = totaltime/increment
    for i in range(steps):
        bar.doPercentage(i/steps)
        time.sleep(increment)

def testticks(increment=0.3, totalticks=10):
    bar.totalticks = totalticks
    for i in range(totalticks):
        bar.doTicks(i)
        time.sleep(increment)

def testaddtick(increment=0.3, totalticks=15):
    bar.totalticks = totalticks
    bar.ticks = 0
    for i in range(totalticks):
        bar.addTick()
        time.sleep(increment)

def tests():
    testpercentage()
    time.sleep(0.1)
    testticks()
    time.sleep(0.1)
    testaddtick()

if __name__ == '__main__':
    root = Tk() 
    root.title('ProgressBar test')
    bar = ProgressBar(root)
    bar.after(1, tests)
    root.mainloop()