# # # # # # # # # # # # # # # # START # # # # # # # # # # # # # # #
import traceback
from tkinter import *
from tkinter import messagebox
# print process result
def printprocess(process):
#     sort processes by number 
    sortp(4, -1, process)
    print('----------------------------------------------------------------------------------')
    for i in range(len(process)):
        print('Process no', i+1)
        print('cpu burst time:', process[i][0], ', process arrival time:', process[i][1], ', response time:', process[i][2], ', waiting time:', process[i][3])
        print('----------------------------------------------------------------------------------')
    return
# make cpu burst time list
def getcbt(process):
    cbt = []
    for i in process:
        cbt.append(i[0])
    return cbt
# calculate sum of process cpu burst time
def calccbt(cbt):
    s = 0
    for i in cbt:
        s += i
    return s
# calculate waiting time
def waiting(process):
    for i in range(len(process)):
        wt = process[i][2] - process[i][0]
#         add waiting time to process list
        process[i][3] = wt
    return process
# find next arrival time
def findtt(tt, process, cbt):
    m = 0
    for i in range(len(process)):
#         check if cbt available
        if cbt[i]:
#             compare process arrival times
            if (process[i][1] < m) or (m == 0):
                m = process[i][1]
#     return remaining time to arrival time
    return m - tt
# sort process by n and m
def sortp(n, m, process):
    j = 0
    while j < len(process):
        for i in range(j, len(process)):
            if process[i][n] < process[j][n]:
                process[i], process[j] = process[j], process[i]
            if (process[i][n] == process[j][n]) and (m >= 0):
                if process[i][m] < process[j][m]:
                    process[i], process[j] = process[j], process[i]
        j += 1
    return process
# calculate average remainig and waiting time
def avg(process):
    w, r, n = 0, 0, len(process)
    for i in process:
        w, r = w + i[3], r + i[2]
    w, r = w/n, r/n
    return w,r
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # SJF # # # # # # # # # # # # # # # #
# 1. calculate SJF algorithm
def sjf(process):
#     sort process list by cbt and arrival time
    sortp(0, 1, process)
    cbt, tt, j = getcbt(process), 0, 0
    while calccbt(cbt):
        for i in range(len(process)):
#             check process availability
            if cbt[i]:
#                 if no more process available at the moment
                if j == 1:
#                     change tt to first arrival time
                    tt += findtt(tt, process, cbt)
#                 if process arrived
                elif process[i][1] <= tt:
                    tt, j, cbt[i] = tt + cbt[i], 0, 0
                    process[i][2] = tt - process[i][1]
                    break
            if i == len(process) - 1:
                j += 1
    return
# # # # # # # # # # # # # # # # FIFO # # # # # # # # # # # # # # # #
# 2. calculate FIFO algorithm
def fifo(process):
    sortp(1, -1, process)
    cbt, tt = getcbt(process), 0
    while calccbt(cbt):
        for i in range(len(process)):
#             check if process available
            if cbt[i]:
#                 check if process not arrived
                if process[i][1] > tt:
                    tt = process[i][1]
                tt, cbt[i] = tt + cbt[i], 0
                process[i][2] = tt - process[i][1]
    return
# # # # # # # # # # # # # # Round Robin # # # # # # # # # # # # # # #
# find next process arrival time
def findnext(process, cbt, tt):
    c, m1, m2 = 0, 0, 0
    for i in range(len(process)):
#         set m1 for first time
        if (m1 == 0) and (cbt[i]):
            m1 = process[i][1]
        if (process[i][1] <= m1) and (not process[i][1] == 0) and (not cbt[i] == 0):
            m2, m1 = m1, process[i][1]
        c += process[i][0] - cbt[i]
    return m1 - c
# 3. calculate round robin algorithm
def round_robin(time, process):
    cbt, tt, j = getcbt(process), 0, 0
    while calccbt(cbt) > 0:
        for i in range(len(process)):
#         check process availability
            if cbt[i]:
                if (process[i][1] < tt) or (process[i][1] == 0) or ((process[i][1] == tt) and (not j == 0)):
                    j = 0
#                     check burst time
                    if cbt[i] >= time:
                        cbt[i], tt = cbt[i] - time, tt + time
#                     cpu burst time bigger than time quantum
                    else:
                        tt += cbt[i]
                        cbt[i] = 0
#                     check if process finished
                    if cbt[i] == 0:
#                         calculate process response time
                        process[i][2] = tt - process[i][1]
#                 process not available!
                elif  i == len(process)-1:
#                     recheck the process list
                    if j == 0:
                        j += 1
                        break
#                     no available process at the moment
                    elif j:
                        tt, j = tt + findnext(process, cbt, tt), 0
                        break
                    continue
    return
# # # # # # # # # # # # # # # # SRT # # # # # # # # # # # # # # # #
# 4. calculate SRT algorithm
def srt(process):
#     sort process list by cbt and arrival time
    sortp(0, 1, process)
    cbt, tt, t, j = getcbt(process), 0, 0, 0
    while calccbt(cbt):
        for i in range(len(process)):
#             check process availability
            if cbt[i]:
#                 if process not arrived
                if process[i][1] > tt:
#                     check if other process arrive sooner
                    if (process[i][1] <= t) or ((t == 0) and (process[i][1] > 0)):
                        t = process[i][1]
#                     check all of the processes (no available process found!)
                    if i == len(process) - 1:
                        j += 1
#                     check all of the processes for 2nd time (no available process found!)
                    if j == 2:
                        tt += findtt(tt, process, cbt)
#                 if process arrived
                else:
#                     if there is no time limit
                    if t == 0:
                        tt, cbt[i] = tt + cbt[i], 0
                        process[i][2] = tt - process[i][1]
#                     if cpu burst time more than time limit
                    elif cbt[i] > t - tt:
                        cbt[i], tt, t = cbt[i] - t - tt, t, 0
                        break
#                     if cpu burst time less than time limit
                    else:
                        tt, cbt[i] = tt + cbt[i], 0
                        process[i][2] = tt - process[i][1]
    return
# # # # # # # # # # # # # # # # HRRN # # # # # # # # # # # # # # # #
# calculate priority
def calcpriority(tt, process, cbt):
    pr1, pr2, m = 0, 0, 0
    for i in range(len(process)):
#         check process availability
        if cbt[i]:
#             check if process arrived
            if process[i][1] <= tt:
                pr1 = (process[i][0] + (tt - process[i][1])) / process[i][0]
                if (pr1 > pr2) or (pr2 == 0):
                    m, pr2 = i, pr1
#     return larger priority
    return m
# 5. calculate HRRN algorithm
def hrrn(process):
    cbt, tt = getcbt(process), 0
    while calccbt(cbt):
#         get process number
        i = calcpriority(tt, process, cbt)
#         check if process not available (for wring process number!)
        if (process[i][1] > tt) or (cbt[i] == 0):
            tt += findtt(tt, process, cbt)
#         check if process available
        else:
            tt, cbt[i] = tt + cbt[i], 0
            process[i][2] = tt - process[i][1]
    return
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    print(process)
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
    lb4 = Label(root,text='Waiting Time',width=12)
    lb5 = Label(root,text='Response Time',width=12)
    
    lb1.grid(row=1,column=0)
    lb2.grid(row=1,column=1)
    lb3.grid(row=1,column=2)
    lb4.grid(row=1,column=3)
    lb5.grid(row=1,column=4)
    
    for i in range(n-1):
        lb11 = Label(root,text=f'Process {process[i][4]}',borderwidth= 2, relief= 'groove',width=10)
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