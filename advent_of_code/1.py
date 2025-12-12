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

from functools import lru_cache
def solve7():
    input = get_lines("input7.txt")
    input = input[1:]
    m = len(input[0])
    n = len(input)
    ray = [0]*m
    ray[m//2] = 1
    res = 0
    for i in range(n):
        for j in range(m):
            if ray[j] == 1 and input[i][j] == "^":
                res += 1
                ray[j] = 0
                if j != 0:
                    ray[j-1] = 1
                if j != m-1:
                    ray[j+1] = 1
    ray = [0]*m
    ray[m//2] = 1
    for i in range(n):
        for j in range(m):
            if ray[j] and input[i][j] == "^":
                if j != 0:
                    ray[j-1] += ray[j]
                if j != m-1:
                    ray[j+1] += ray[j]
                ray[j] = 0

    return sum(ray)

def solve2():
    input = get_lines("input2.txt")
    input = input[0].split(",")
    for i in range(len(input)):
        input[i] = input[i].split("-")
    res = 0
    for i in range(len(input)):
        s, e = int(input[i][0]), int(input[i][1])
        for j in range(s, e+1):
            s = str(j)
            if len(s)%2 == 1:
                continue
            if s[:len(s)//2] == s[len(s)//2:]:
                res += int(j)
    res = 0
    for i in range(len(input)):
        start, e = int(input[i][0]), int(input[i][1])
        for j in range(start, e+1):
            s = str(j)
            for k in range(1, len(s)//2 + 1):
                if len(s) % k != 0:
                    continue
                pat = s[:k]
                FLAG = True
                l = k
                while FLAG and l+k <= len(s):
                    if s[l:l+k] != pat:
                        FLAG = False
                    l += k
                if FLAG:
                    res += int(s)
                    break
    
    return res

def solve8():
    input = get_lines("input8.txt")
    pass
from functools import lru_cache

def solve10():
    input = get_lines("input10.txt")
    
    for i in range(len(input)):
        input[i] = input[i].split(" ")
    
    @lru_cache(None)
    def dp(curr, mask):
        if curr == TARGET:
            return 0
        ans = float("inf")
        new_mask = list(mask)
        for i in range(len(switches)):
            if mask[i]:
                continue
            new_curr = list(curr)
            new_mask[i] = 1
            for s in switches[i]:
                new_curr[int(s)] *= -1
            new_curr = tuple(new_curr)
            ans = min(ans, 1 + dp(new_curr, tuple(new_mask)))
            new_mask[i] = 0
        return ans
    
    res = 0
    for i in range(len(input)):
        TARGET = list(input[i][0][1:-1])
        for j in range(len(TARGET)):
            if TARGET[j] == ".":
                TARGET[j] = -1
            else:
                TARGET[j] = 1
        curr = [-1]*len(TARGET)
        switches = input[i][1:-1]
        for j in range(len(switches)):
            switches[j] = switches[j][1:-1]
            switches[j] = switches[j].split(",")
        mask = [0]*len(switches)
        compute = dp(tuple(curr), tuple(mask))
        print(compute)
        res += compute

    return res

from collections import defaultdict
def solve11():
    input = get_lines("input11.txt")
    for i in range(len(input)):
        input[i] = input[i].split(" ")
    adj = defaultdict(list)
    for i in range(len(input)):
        node = input[i][0][:-1]
        for j in range(1, len(input[i])):
            adj[node].append(input[i][j])
    
    visiting = set()
    # @lru_cache(None)
    # def dfs(node):
    #     if node == "out":
    #         return 1
    #     visiting.add(node)
    #     ans = 0
    #     for nei in adj[node]:
    #         if nei not in visiting:
    #             ans += dfs(nei)
    #     visiting.remove(node)
    #     return ans
    
    @lru_cache(None)
    def dfs(node, d, f):
        if node == "out" and d and f:
            return 1
        elif node == "out":
            return 0
        visiting.add(node)
        ans = 0
        for nei in adj[node]:
            if nei not in visiting and node == "dac":
                ans += dfs(nei, True, f)
            elif nei not in visiting and node == "fft":
                ans += dfs(nei, d, True)
            elif nei not in visiting:
                ans += dfs(nei, d, f)
        visiting.remove(node)
        return ans
    
    return dfs("svr", False, False)

def solve3():
    input = get_lines("input3.txt")
    res = 0
    # for i in range(len(input)):
    #     f = max(input[i][:-1])
    #     for j in range(len(input[i])):
    #         if input[i][j] == f:
    #             s = max(input[i][j+1:])
    #             num = f + s
    #             res += int(num)
    #             break
    
    for i in range(len(input)):
        num = []
        id = -1
        curr = "0"
        while (len(num) != 12):
            for j in range(id+1, len(input[i]) - 11 + len(num)):
                if input[i][j] > curr:
                    id = j
                    curr = input[i][id]
            num.append(input[i][id])
            curr = "0"
        num = "".join(num)
        res += int(num)
    
    return res

import heapq
def solve8():
    input = get_lines("input8.txt")
    for i in range(len(input)):
        input[i] = input[i].split(",")
    rank = [1]*len(input)
    par = [i for i in range(len(input))]
    h = []
    for i in range(len(input)):
        for j in range(i+1, len(input)):
            x, y, z = input[i]
            a, b, c = input[j]
            dist = ((int(x)-int(a))**2 + (int(y)-int(b))**2 + (int(z)-int(c))**2)
            h.append((dist, i, j))
    heapq.heapify(h)

    def find(n):
        res = n
        while res != par[res]:
            par[n] = par[par[n]]
            res = par[n]
        return res

    def union(n1, n2):
        p1, p2 = find(n1), find(n2)
        if p1 == p2:
            return
        
        if rank[p1] == rank[p2]:
            rank[p1] += 1
            par[p2] = p1
        elif rank[p1] > rank[p2]:
            par[p2] = p1
        elif rank[p1] < rank[p2]:
            par[p1] = p2
        return

    while True:
        d, n1, n2 = heapq.heappop(h)
        union(n1, n2)
        for i in range(len(input)):
            par[i] = find(i)
        conn = set()
        for i in range(len(par)):
            conn.add(par[i])
        if len(conn) == 1:
            x1, _, _ = input[n1]
            x2, _, _ = input[n2]
            return int(x1)*int(x2)
    # for _ in range(1000):
    #     d, n1, n2 = heapq.heappop(h)
    #     union(n1, n2)

    # size = defaultdict(int)
    # for i in range(len(input)):
    #     size[find(i)] += 1
    
    # arr = list(size.values())
    # arr.sort(reverse=True)
    # return prod(arr[:3])


def solve9():
    data = get_lines("input9.txt")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    
    res = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            x1, y1 = data[i]
            x2, y2 = data[j]
            hor = abs(x1-x2) + 1
            ver = abs(y1-y2) + 1
            res = max(res, hor*ver)
    
    return res

if __name__ == "__main__":
    # print(solve())
    # print(solve2())
    #print(solve5())
    #print(solve4())
    #print(solve7())
    #print(solve2())
    #print(solve11())
    #print(solve3())
    #print(solve8())
    print(solve9())
