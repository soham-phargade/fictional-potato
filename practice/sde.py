def p1():
    R = "BAABA"
    V=[2,4,1,1,2]
    min_a, min_b = float('inf'), float('inf')
    if (len(V) == 0): return [-min_a, -min_b]

    bal_a, bal_b = 0, 0
    for i in range(len(V)):
        if(R[i]=='B'):
            bal_a -= V[i]
            bal_b += V[i]
            min_a = min(min_a, bal_a)

        if(R[i]=='A'):
            bal_a += V[i]
            bal_b -= V[i]
            min_b = min(min_b, bal_b)
    return [-min_a,-min_b]

def p2(A, B, C):
    def checker(i, j, k) -> bool:
        max_val = max([i,j,k])
        if max_val == i:
            return ((i//3) <= k+j)
        if max_val == j:
            return ((j//3) <= k+i)
        if max_val == k:
            return ((k//3) <= i+j)
            
    ans = []
    while A+B+C > 0:
        if(A and checker(A-1,B,C)):
            ans.append('a')
            A-=1
        elif(B and checker(A,B-1,C)):
            ans.append('b')
            B-=1
        elif(C and checker(A,B,C-1)):
            ans.append('c')
            C-=1
    return ''.join(ans)

def p3(input):
    # input = input + [0]
    # matrix = [[0 for _ in range(2)] for _ in range(len(input))]
    
    # for i in range()
    def backtrack(arr):
        sum = 0
        for i in range(len(arr)-1):
            curr = arr[i]
            merge = curr + arr[i+1]
            sum = max(backtrack(arr[i+1:]) + curr, backtrack(arr[i+2:]) + merge)
        return sum
    
    input = input + [0]
    return backtrack(input)

'''
1. merge 
2. stay
compute 



0,9,9
'''

def p4():
    arr = [5,2,4,6,3,7]
    




def main():
    #print(p1())
    #print(p2(1,3,0))
    print(p3([22,35,40]))
    return

if __name__ == "__main__":
    main()
'''
a 1 
b 3

a?
checker for valid diverse word 
length = 3
a=0 b=3



'''