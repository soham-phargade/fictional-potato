import sys

def get_lines(input):
    out = []
    with open(input, 'r') as file: 
        for l in file:
            out.append(l.rstrip("\n"))
    #print(out)
    return out

def solve4():
    grid = get_lines("4.txt")
    m = len(grid)
    n = len(grid[0])
    for i in range(m):
        grid[i] = list(grid[i])
    dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    res = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] != "@":
                continue
            adj = 0
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if(0 <= nr < m and 0 <= nc < n):
                    if grid[nr][nc] == "@":
                        adj +=1
            if adj < 4:
                res +=1
    print(res)
    # p2
    old_res = -1
    new_res = 0
    while(old_res < new_res):
        old_res = new_res
        for r in range(m):
            for c in range(n):
                if grid[r][c] != "@":
                    continue
                adj = 0
                for dr, dc in dirs:
                    nr, nc = r+dr, c+dc
                    if(0 <= nr < m and 0 <= nc < n):
                        if grid[nr][nc] == "@":
                            adj +=1
                if adj < 4:
                    new_res +=1
                    grid[r][c] = "."
    
    print(new_res)

def solve5():
    raw_intervals = get_lines("intervals.txt")
    #raw_intervals = get_lines("test.txt")
    points = get_lines("input5.txt")
    #points = get_lines("test2.txt")
    intervals = []
    for interval in raw_intervals:
        curr = interval.split('-')
        intervals.append(curr)
    fresh = 0
    for p in points:
        b = False
        for i in range(len(intervals)):
            start = int(intervals[i][0])
            end = int(intervals[i][1])
            if start <= int(p) <= end:
                b = True
        if b:
            fresh += 1
    
    valid = set()
    for i in range(len(intervals)):
        s = int(intervals[i][0])
        e = int(intervals[i][1])
        if s <= e:
            intervals[i] = [s,e]
        else:
            intervals[i] = [e,s]
    intervals.sort()

    s = intervals[0][0]
    e = intervals[0][1]

    ings = 0
    for i in range(len(intervals)):
        s1, e1 = intervals[i][0], intervals[i][1]
        if e < s1:
            ings += e-s+1
            s = s1
            e = e1
        else:
            e = max(e, e1)
    ings += e-s+1
    print(ings)
    #print(intervals)

    # print(fresh)
    # print(len(valid))

def solve():
    arr = get_lines("input.txt")
    res = 0
    curr = 50
    for comb in arr:
        dir = comb[0]
        num = int(comb[1:])

        if dir == "L":
            curr = (curr - num)%100
        else:
            curr = (curr + num)%100
        
        if curr == 0:
            res += 1
    
    return res

def solve2():
    arr = get_lines("input.txt")
    turns = [None] * len(arr)

    for i, comb in enumerate(arr):
        if comb[0] == "L":
            turns[i] = -int(comb[1:])
        else:
            turns[i] = int(comb[1:])

    res = 0
    curr = 50

    for t in turns:
        d = t/abs(t)
        i = 0
        while i < abs(t):
            curr += 1*d
            curr = curr % 100
            if curr == 0:
                res += 1
            i += 1

    return res
from math import prod

def solve6():
    input = get_lines("input6.txt")
    for i in range(len(input)-1):
        input[i] = input[i].split()
    ops = input[-1].split()
    input.pop()
    res = []
    for i, op in enumerate(ops):
        if op == "+":
            s = 0
            for j in range(len(input)):
                s += int(input[j][i])
        if op == "*":
            s = 1
            for j in range(len(input)):
                s *= int(input[j][i])
        res.append(s)
    
    # return sum(res)
    # p2

    input = get_lines("input6.txt")
    ops = input[-1].split()
    input.pop()
    tmp = max(len(cell) for cell in input)
    for r in input:
        r = r.ljust(tmp)
    op = 0
    j = 0
    res = []
    print(input)
    while(op < len(ops)):
        empty = False
        curr = []
        while not empty and j < tmp:
            empty = True
            num = []
            for i in range(len(input)):
                if input[i][j] != " ":
                    empty = False
                    num.append(input[i][j])
            if not empty:
                num = int("".join(num))
                curr.append(num)
            j += 1

        if ops[op] == "+":
            res.append(sum(curr))

        if ops[op] == "*":
            res.append(prod(curr))

        op += 1
    print(res)
    return sum(res)

def solve7():
    input = get_lines("input7.txt")

if __name__ == "__main__":
    # print(solve())
    # print(solve2())
    #print(solve5())
    #print(solve4())
    print(solve6())