import traceback
from tkinter import *
from tkinter import messagebox
from os_project import hrrn,round_robin,fifo,srt,sjf,sortp,waiting,avg

def show_error(self, *args):
    err = str(traceback.format_exception(*args))
    messagebox.showwarning("showwarning", 'Warning!')
def setlabel(text,r,c,rs,cs):
    label = Label(root,text=text)
    label.grid(row=r,column=c,rowspan=rs,columnspan=cs)
    return
def forget(wid):
    for i in wid:
        i.destroy()
    return

def showres(ent,op):
    lbs = []
    process = []
    n = len(ent)
    for i in range(len(ent)-1):
        process.append([int(ent[i][1].get()),int(ent[i][2].get()),0,0,i])
        forget(ent[i])
    if op == 'HRRN':
        hrrn(process)
    elif op == 'RR-2':
        round_robin(2,process)
    elif op == 'RR-4':
        round_robin(4,process)
    elif op == 'FIFO':
        fifo(process)
    elif op == 'SRT':
        srt(process)
    elif op == 'SJF':
        sjf(process)
    forget(ent[n-1])
    sortp(4, -1, process)
    process = waiting(process)
    av = avg(process)
    
    lb1 = Label(root,text='Process Number',width=12)
    lb2 = Label(root,text='CBT',width=12)
    lb3 = Label(root,text='Arrival Time',width=12)
    lb4 = Label(root,text='Response Time',width=12)
    lb5 = Label(root,text='Waiting Time',width=12)
    
    lb1.grid(row=1,column=0)
    lb2.grid(row=1,column=1)
    lb3.grid(row=1,column=2)
    lb4.grid(row=1,column=3)
    lb5.grid(row=1,column=4)
    
    for i in range(n-1):
        lb11 = Label(root,text=f'Process {process[i][4]+1}',borderwidth= 2, relief= 'groove',width=10)
        lb12 = Label(root,text=process[i][0],borderwidth= 2, relief= 'groove',width=10)
        lb13 = Label(root,text=process[i][1],borderwidth= 2, relief= 'groove',width=10)
        lb14 = Label(root,text=process[i][2],borderwidth= 2, relief= 'groove',width=10)
        lb15 = Label(root,text=process[i][3],borderwidth= 2, relief= 'groove',width=10)
        
        lb11.grid(row=2+i,column=0,pady=(15,0))
        lb12.grid(row=2+i,column=1,pady=(15,0))
        lb13.grid(row=2+i,column=2,pady=(15,0))
        lb14.grid(row=2+i,column=3,pady=(15,0))
        lb15.grid(row=2+i,column=4,pady=(15,0))
    lb = Label(root,text='Average of waiting time: ',width=30)
    lb.grid(row=2+n,column=0,columnspan=2,pady=(15,0))
    lb = Label(root,text=format(av[0], ".3f"),width=10)
    lb.grid(row=2+n,column=2,pady=(15,0))
    lb = Label(root,text='Average of response time: ',width=30)
    lb.grid(row=3+n,column=0,columnspan=2,pady=(15,0))
    lb = Label(root,text=format(av[1], ".3f"),width=10)
    lb.grid(row=3+n,column=2,pady=(15,0))
    btn3 = Button(root,text='Close',command=lambda:exit())
    btn3.grid(row=0,column=0,pady=(15,0))

def getentry():
    entries= []
    try:
        n = int(e1.get())
        if n > 15:
            messagebox.showwarning("showwarning", 'Process Number Should Be Less Than 16!')
            return
        ch = c.get()
        lb2 = Label(root,text='Process Number',width = 15)
        lb3 = Label(root,text='Process CBT',width = 15)
        lb4 = Label(root,text='Process Arrival Time',width = 15)
        lb4.grid(row=2,column=2,pady=(5,0))
        lb2.grid(row=2,column=0,pady=(5,0))
        lb3.grid(row=2,column=1,pady=(5,0))
        
        
        forget([lb1,e1,c1,btn1])
        for i in range(int(n)):
            lb = Label(root,text=f'Process {i+1}')
            en1 = Entry(root,width = 10, justify= 'center')
            en2 = Entry(root,width = 10, justify= 'center')
            if not ch:
                en2.insert(0,'0')
            en2.grid(row = 3+i, column=2,pady=(5,0))
            entries.append([lb,en1,en2])
            lb.grid(row = 3+i, column=0,pady=(5,0))
            en1.grid(row = 3+i, column=1,pady=(5,0))
        btn2 = Button(root, text='Calculate',width=10,command=lambda:showres(entries,vari.get()))
        btn2.grid(row=int(n)+3,column=0,pady=(15,0))
        
        vari = StringVar(root)
        vari.set('HRRN')
        w = OptionMenu(root,vari,'HRRN','RR-2','RR-4','FIFO','SRT','SJF')
        w.grid(row=n+3,column=1,pady=(15,0),sticky='ew')
        entries.append([btn2,w,lb2,lb3,lb4])
    except :
        Tk.report_callback_exception = show_error
        setlabel('Number Only!',3,3,0,6)

root = Tk()
# Tkinter window size value
w,h = 700,600
# Set desired Tkinter Window Size.
root.geometry(f'{w}x{h}')
root.maxsize(w, h)
root.minsize(w, h)
# calculate coordination of screen and window form
x = int(root.winfo_screenwidth()/2 - w/2)
y = int(root.winfo_screenheight()/2 - h/2)
# Write following format for center screen
root.geometry(f'+{x}+{y}')
root.title('Process Scheduling Calculator')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(30, weight=5)

root.grid_columnconfigure(6, weight=1)

c = IntVar()
lb1 = Label(root, text='Enter number of processes: ')
e1 = Entry(root, width=10, justify= 'center')
c1 = Checkbutton(root, text = 'set arrival time',variable=c)
btn1 = Button(root, text='click me!', command=getentry)

lb1.grid(row=1, column=0,columnspan=2,pady=(10,0))
e1.grid(row=1,column=1,pady=(10,0))
c1.grid(row=2,column=0,columnspan=2,pady=(5,0))
btn1.grid(row=2,column=1,pady=(5,0))

root.mainloop()