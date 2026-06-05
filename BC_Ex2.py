import math
import doctest

def input_data():
      d1 = float(input('Введите кратчайшее расстояние между спасателем и кромкой воды: '))
      d2 = float(input('Введите кратчайшее расстояние от утопающего до берега: '))
      h = float(input('Введите боковое смещение между спасателем и утопающим: '))
      v_sand = float(input('Введите скорость движения спасателя по песку: '))
      n = float(input('Введите коэффициент замедления спасателя при движении в воде: '))
      theta1 = float(input('Введите направление движения спасателя по песку: '))
      return d1, d2, h, v_sand, n, theta1

def calc_time(d1, d2, h, v_sand, n, theta1):
      d1_feet = d1 * 3
      h_feet = h * 3
      v_sand_fps = v_sand * 1.467
      theta1_rad = math.radians(theta1)

      x = d1_feet * math.tan(theta1_rad)
      L1 = math.sqrt(x ** 2 + d1_feet ** 2)
      L2 = math.sqrt((h_feet - x) ** 2 + d2 ** 2)
      return (L1 + n * L2) / v_sand_fps

def print_result(theta1, t):
      print(f'\nЕсли спасатель начнет движение под углом, равным {int(theta1)} градусам, он'
            f'\nдостигнет утопающего через {t:.1f} секунды.')

def test_calc_time():
      """
      >>> round(calc_time(8, 10, 50, 5, 2, 39.413), 1)
      39.9

      >>> round(calc_time(3, 9, 48, 4, 1, 37.234), 1)
      25.4

      >>> round(calc_time(2, 7, 34, 2, 6, 33.142), 1)
      203.5
      """
      pass

doctest.testmod()
d1, d2, h, v_sand, n, theta1 = input_data()
t = calc_time(d1, d2, h, v_sand, n, theta1)
print_result(theta1, t)