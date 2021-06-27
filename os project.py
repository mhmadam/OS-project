# # # # # # # # # # # # # # # # START # # # # # # # # # # # # # # #
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

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


Builder.load_file('kvdesign/OS_project.kv')

class layout(Widget):
    pass
        

class OSproject(App):
    def build(self):
        return mylayout()




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# process = [[1, 6, 0, 0, 0], [5, 7, 0, 0, 1], [3, 0, 0, 0, 2], [4, 2, 0, 0, 3], [2, 2, 0, 0, 4], [4, 8, 0, 0, 5], [3, 7, 0, 0, 6]]
# process = [[1, 6, 0, 0, 0], [2, 2, 0, 0, 1], [3, 0, 0, 0, 2], [4, 10, 0, 0, 3], [5, 7, 0, 0, 4], [6, 5, 0, 0, 5]]
# process = [[8, 0, 0, 0, 0], [1, 1, 0, 0, 1], [4, 3, 0, 0, 2], [6, 3, 0, 0, 3], [2, 3, 0, 0, 4]]
# process = [[9, 0, 0, 0, 0], [4, 2, 0, 0, 1], [8, 0, 0, 0, 2], [2, 3, 0, 0, 3], [1, 5, 0, 0, 4]]
# process = [[1, 0, 0, 0, 0], [3, 0, 0, 0, 1], [2, 2, 0, 0, 2], [4, 9, 0, 0, 3], [3, 8, 0, 0, 4]]
# process = [[3, 0, 0, 0, 0], [5, 6, 0, 0, 1], [4, 8, 0, 0, 2], [2, 10, 0, 0, 3]]
# process = [[8, 3, 0, 0, 0], [4, 4, 0, 0, 1], [9, 5, 0, 0, 2], [5, 6, 0, 0, 3]]
# process = [[2, 0, 0, 0, 0], [3, 0, 0, 0, 1], [2, 0, 0, 0, 2]]
# process = [[9, 0, 0, 0, 0], [2, 0, 0, 0, 1], [2, 0, 0, 0, 2]]
# process = [[3, 1, 0, 0, 0], [2, 5, 0, 0, 1], [4, 9, 0, 0, 2]]
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# pr = True
# process = []
# n = int(input('Number of process: '))
# for i in range(n):
#     
#     cbt = float(input(f'Process no {i+1} cpu burst time: '))
#     if (cbt - int(cbt) == 0):
#         cbt = int(cbt)
#     if cbt == 0:
#         pr = False
#         print('Wrong cpu burst time!')
#         break
#     process.append([cbt])
#     
#     artime = float(input(f'Process no {i+1} arrival time: '))
#     if (artime - int(artime) == 0):
#         artime = int(artime)
#     process[i].append(artime)
#     
#     process[i].extend([0, 0, i])
# 
# if pr:
#     a = int(input('Enter algoritm number: \n1.SJF\n2.FIFO\n3.Round Robin\n4.SRT\n5.HRRN\n'))
#     if a == 3:
#         t = float(input('Enter time quantum: '))
#         if (t - int(t) == 0):
#             t = int(t)
# 
#     print('ok!')
# 
# # # # # SJF algorithm # # # #
#     if a == 1:
#         sjf(process)
# 
# # # # # FIFO algorithm # # # #
#     elif a == 2:
#         fifo(process)
# 
# # # # # RR algorithm # # # #
#     elif a == 3:
#         round_robin(t, process)
# 
# # # # # SRT algorithm # # # #
#     elif a == 4:
#         srt(process)
# 
# # # # # HRRN algorithm # # # #
#     elif a == 5:
#         hrrn(process)
# 
#     else:
#         pr = False
#         print('Algoritm not available!')
# 
#     if pr:
# #         calculate process waiting time
#         process = waiting(process)
# #         print process
#         printprocess(process)
# #         calculate and print average
#         av = avg(process)
#         print('Average of waiting time:', format(av[0], ".3f"))
#         print('Average of response time:', format(av[1], ".3f"))
        

if __name__ == '__main__':
    OSproject().run()
