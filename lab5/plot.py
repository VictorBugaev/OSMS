import matplotlib.pyplot as plt

values = [1, 1, 0.6 ,0.3, 0.15, 0.1]

polynomial_lengths = list(range(2, 8))

plt.plot(polynomial_lengths, values, marker='o', linestyle='-')
plt.title('График зависимости от длины полинома')
plt.xlabel('Длина полинома')
plt.ylabel('Среднее значение суммы ошибок(за 10 раз)')
plt.grid(True)
plt.show()
