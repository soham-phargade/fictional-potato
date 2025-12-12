# implement a function, get nth string, with n as input 
# n = 1, return '00001'
# n = 100000, return '0000A'
# n = 37, return '00037'

# A is 0 
# B is 1
# ...
# Z is 25
def func(n:int):
    if n < 100000:
        arr = ["00000"] + [str(n)]
        res = "".join(arr)
        res = res[-5:]
        return res
    else:
        n = n - 100000
        res = []
        while True:
            rem = n % 26
            c = chr(ord('A') + rem)
            res.append(c)
            n = n // 26
            if not n:
                break
        res = res[::-1]
        res = ["00000"] + res
        res = "".join(res)    
        return res[-5:]

if __name__ == "__main__":
    print(func(1))
    print(func(100025))
    print(func(100026))
    print(func(37))

