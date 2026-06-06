import math

def input_data():
      d1 = float(input('Введите кратчайшее расстояние между спасателем и кромкой воды: '))
      d2 = float(input('Введите кратчайшее расстояние от утопающего до берега: '))
      h = float(input('Введите боковое смещение между спасателем и утопающим: '))
      v_sand = float(input('Введите скорость движения спасателя по песку: '))
      n = float(input('Введите коэффициент замедления спасателя при движении в воде: '))
      return d1, d2, h, v_sand, n

def calc_time(d1, d2, h, v_sand, n, theta1):
      d1_feet = d1 * 3
      h_feet = h * 3
      v_sand_fps = v_sand * 1.467
      theta1_rad = math.radians(theta1)

      x = d1_feet * math.tan(theta1_rad)
      L1 = math.sqrt(x ** 2 + d1_feet ** 2)
      L2 = math.sqrt((h_feet - x) ** 2 + d2 ** 2)
      return (L1 + n * L2) / v_sand_fps

def find_best_theta1(d1, d2, h, v_sand, n):
    best_time = float('inf')
    best_theta1 = 0
    for theta1 in range(0, 90):
        t = calc_time(d1, d2, h, v_sand, n, theta1)
        if t < best_time:
            best_time = t
            best_theta1 = theta1
    return best_theta1

def print_result(theta1):
      print(f'\nОптимальное значение угла движения спасателя: {int(theta1)} градусов.')

# Тестирование в этом задании опустил

d1, d2, h, v_sand, n = input_data()
theta1 = find_best_theta1(d1, d2, h, v_sand, n)
print_result(theta1)