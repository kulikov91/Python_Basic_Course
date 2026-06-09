t = int(input()) # наборы входных данных

for _ in range(t):
    n = int(input()) # длина массива
    a = list(map(int, input().split())) # массив цифр
    gift = 0

    for i in range(n):
        b = a.copy()
        b[i] += 1
        mult = 1
        for x in b:
            mult *= x
        gift = max(gift, mult)

    print(gift)