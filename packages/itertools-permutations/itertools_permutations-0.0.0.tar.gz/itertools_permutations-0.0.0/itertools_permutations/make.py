from itertools import permutations

def make(length):
    number = [i+1 for i in range(length)]
    a=[]
    b=[]
    for i in map(list,permutations(number)):
        b.append(i)
        tmp=i.copy()
        for _ in range(length):
            tmp[_]=-i[_]
            a.append(tmp.copy())
    a = a + b
    return a, a