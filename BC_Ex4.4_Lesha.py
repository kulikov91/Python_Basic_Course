n = int(input()) # кол-во элементов в массиве
n2 = list(map(int,input().split())) # элементы массива

total = sum(n2) # считаем сумму элементов

if total != 0:
    print("YES")
    print(1)
    print(1, n)
else:
    idx = -1
    for i in range(n):
        if n2[i] != 0:
            idx = i
            break

    if idx == -1: # если все элементы равны нулю
        print("NO")
    else:
        print("YES")
        print(2)
        print(1, idx + 1)
        print(idx + 2, n)