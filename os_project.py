# # # # # # # # # # # # # # # # START # # # # # # # # # # # # # # #

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

if __name__ == '__main__':
    round_robin()
    waiting()
    hrrn()
    fifo()
    srt()
    sjf()
    avg()