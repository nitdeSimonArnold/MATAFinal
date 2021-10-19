from __future__ import print_function
from copy import copy, deepcopy
import numpy as np

import array
from itertools import product, combinations

board = [
    [3, 1, 5, 4, 7, 8, 2, 6, 9],
    [9, 4, 2, 3, 5, 6, 7, 1, 8],
    [7, 8, 6, 0, 0, 0, 0, 3, 0],
    [2, 0, 3, 7, 8, 0, 0, 0, 0],
    [0, 0, 7, 0, 0, 0, 0, 9, 0],
    [4, 0, 0, 0, 6, 1, 0, 0, 2],
    [6, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 7],
    [0, 0, 0, 0, 3, 7, 9, 4, 0]
]

array = []
arrax = []
tst = []
fix = []
all = [1,2,3,4,5,6,7,8,9]
allk = [0,1,2,3,4,5,6,7,8]

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

def solve(bo):
    bord = deepcopy(bo)
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] != 0:
                fix.append(bo[i][j])
    l = len(fix)
    #naked_singels_row(bo)
    #naked_singels_column(bo)
    #naked_singels_box(bo)
    #overflow_row(bo)
    #overflow_column(bo)
    del fix[:]
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] != 0:
                fix.append(bo[i][j])
    if len(fix) == l:
        back(bord)
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    bo[i][j] = bord[i][j]
                    return bo

def naked_singels_row(bo):
    x = 0
    while x < 9:
        for a in range(len(bo[x])):
            if bo[x][a] == 0:
                array.append(a)
        if len(array) == 1:
            for b in all:
                if b not in bo[x]:
                    a = array[0]
                    bo[x][a] = b
        x += 1
        array.clear()

def naked_singels_column(bo):
    x = 0
    while x < 9:
        for a in range(9):
            if bo[a][x] == 0:
                array.append(a)
            else:
                c = bo[a][x]
                v = 70
                return v
                tst.append(c)
        if len(array) == 1:
            for b in all:
                if b not in tst:
                    a = array[0]
                    bo[a][x] = b
        x += 1
        array.clear()

def naked_singels_box(bo):
    s = 0
    t = 0
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                s, t = ident_box(j, i)
                del array[:]
                array.append(bo[s][t])
                array.append(bo[s+1][t])
                array.append(bo[s+2][t])
                array.append(bo[s][t+1])
                array.append(bo[s+1][t+1])
                array.append(bo[s+2][t+1])
                array.append(bo[s][t+2])
                array.append(bo[s+1][t+2])
                array.append(bo[s+2][t+2])
                zero = array.count(0)
                if zero >> 1:
                    break
                for a in all:
                    if a not in array:
                        bo[i][j] = a

def overflow_row(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                if i == 0 or i == 3 or i == 6:
                    for a in bo[i+1]:
                        if a in bo[i+2] and a not in bo[i]:
                            box_check(bo, j, i, a)
                            column_check(bo, j, i, a)
                            det_box_check(bo, j, i)
                            if bo[i][j] != 0:
                                return
                if i == 1 or i == 4 or i == 7:
                    for a in bo[i - 1]:
                        if a in bo[i + 1] and a not in bo[i]:
                            box_check(bo, j, i, a)
                            column_check(bo, j, i, a)
                            det_box_check(bo, j, i)
                            if bo[i][j] != 0:
                                return
                if i == 2 or i == 5 or i == 8:
                    for a in bo[i - 2]:
                        if a in bo[i - 1] and a not in bo[i]:
                            box_check(bo, j, i, a)
                            column_check(bo, j, i, a)
                            det_box_check(bo, j, i)
                            if bo[i][j] != 0:
                                return

def det_box_check(bo, j, i):
    if j == 0 or j == 3 or j == 6:
        if bo[i][j + 1] == 0 or bo[i][j + 2] == 0:
            bo[i][j] = 0
    elif j == 1 or j == 4 or j == 7:
        if bo[i][j + 1] == 0 or bo[i][j - 1] == 0:
            bo[i][j] = 0
    elif j == 2 or j == 5 or j == 8:
        if bo[i][j - 2] == 0 or bo[i][j - 1] == 0:
            bo[i][j] = 0

def column_check(bo, j, i, a):
    for k in allk:
        if k != i:
            if bo[k][j] == a:
                bo[i][j] = 0

def box_check(bo, j, i, a):
    s, t = ident_box(j, i)
    if bo[t][s] == a:
        bo[i][j] = 0
        return
    elif bo[t+1][s] == a:
        bo[i][j] = 0
        return
    elif bo[t+2][s] == a:
        bo[i][j] = 0
        return
    elif bo[t][s+1] == a:
        bo[i][j] = 0
        return
    elif bo[t+1][s+1] == a:
        bo[i][j] = 0
        return
    elif bo[t+2][s+1] == a:
        bo[i][j] = 0
        return
    elif bo[t][s+2] == a:
        bo[i][j] = 0
        return
    elif bo[t+1][s+2] == a:
        bo[i][j] = 0
        return
    elif bo[t+2][s+2] == a:
        bo[i][j] = 0
        return
    else:
        bo[i][j] = a

def ident_box(j,i):
    if i <= 2:
        if j <= 2:
            s = 0
            t = 0
            return(s,t)
        elif j <= 5:
            s = 3
            t = 0
            return(s,t)
        else:
            s = 6
            t = 0
            return(s,t)
    if i <= 5:
        if j <= 2:
            s = 0
            t = 3
            return(s,t)
        elif j <= 5:
            s = 3
            t = 3
            return(s,t)
        else:
            s = 6
            t = 3
            return(s,t)
    else:
        if j <= 2:
            s = 0
            t = 6
            return(s,t)
        elif j <= 5:
            s = 3
            t = 6
            return(s,t)
        else:
            s = 6
            t = 6
            return(s,t)

def overflow_column(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                o_column_check(bo, i, j)
                a = bo[i][j]
                bo[i][j] = 0
                box_check(bo, j, i, a)
                row_check(bo, i, j, a)
                deta_box_check(bo, j, i)
                if bo[i][j] != 0:
                    return

def o_column_check(bo, i, j):
    del array[:]
    del tst[:]
    del arrax[:]
    if j == 0 or j == 3 or j == 6:
        k = 0
        while k < 9:
            x = bo[k][j + 1]
            array.append(x)
            x = bo[k][j + 2]
            tst.append(x)
            x = bo[k][j]
            arrax.append(x)
            k += 1
        for a in array:
            if a in tst and a not in arrax and a != 0:
                bo[i][j] = a
                return a
    if j == 1 or j == 4 or j == 7:
        k = 0
        while k < 9:
            x = bo[k][j - 1]
            array.append(x)
            x = bo[k][j + 1]
            tst.append(x)
            x = bo[k][j]
            arrax.append(x)
            k += 1
        for a in array:
            if a in tst and a not in arrax and a != 0:
                bo[i][j] = a
                return a
    if j == 2 or j == 5 or j == 8:
        k = 0
        while k < 9:
            x = bo[k][j - 1]
            array.append(x)
            x = bo[k][j - 2]
            tst.append(x)
            x = bo[k][j]
            arrax.append(x)
            k += 1
        for a in array:
            if a in tst and a not in arrax and a != 0:
                bo[i][j] = a
                return a

def row_check(bo, i, j, a):
    for b in allk:
        if b != j:
            if bo[i][b] == a:
                bo[i][j] = 0

def deta_box_check(bo, j, i):
    if i == 0 or i == 3 or i == 6:
        if bo[i + 1][j] == 0 or bo[i + 2][j] == 0:
            bo[i][j] = 0
    elif i == 1 or i == 4 or i == 7:
        if bo[i + 1][j] == 0 or bo[i - 1][j] == 0:
            bo[i][j] = 0
    elif i == 2 or i == 5 or i == 8:
        if bo[i - 2][j] == 0 or bo[i - 1][j] == 0:
            bo[i][j] = 0

def arr_box_app(bo, i, j):
    s, t = ident_box(j, i)
    if bo[t][s] != 0:
        array.append(bo[t][s])
    if bo[t + 1][s] != 0:
        array.append(bo[t + 1][s])
    if bo[t + 2][s] != 0:
        array.append(bo[t + 2][s])
    if bo[t][s + 1] != 0:
        array.append(bo[t][s + 1])
    if bo[t + 1][s + 1] != 0:
        array.append(bo[t + 1][s + 1])
    if bo[t + 2][s + 1] != 0:
        array.append(bo[t + 2][s + 1])
    if bo[t][s + 2] != 0:
        array.append(bo[t][s + 2])
    if bo[t + 1][s + 2] != 0:
        array.append(bo[t + 1][s + 2])
    if bo[t + 2][s + 2] != 0:
        array.append(bo[t + 2][s + 2])

def back(bo):
    bord = deepcopy(bo)
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if back(bo):
                return True
            bo[row][col] = 0
    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None