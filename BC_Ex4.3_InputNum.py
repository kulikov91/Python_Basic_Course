t = int(input()) # количество наборов входных данных

for _ in range(t):
    n, d = map(int, input().split()) # длина числа + доп.цифра
    num = input() # изначальное число, строка

    d = str(d) # переводим в строку для последующего сравнения

    for i in range(n):
        if num[i] < d:
            num = num[:i] + d + num[i:]
            break
    else:
        num = num + d

    print(num)
