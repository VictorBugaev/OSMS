# coding: utf8
import numpy as np
import matplotlib.pyplot as plt

# Функция для квантования значений сигнала до заданного числа битов
def quantize_signal(signal, num_bits):
    max_value = 2**(num_bits-1) - 1
    return np.round(np.clip(signal, 0, max_value))


fs = 6
t = np.linspace(0, 1, 1000) 
original_signal =6 * np.sin(2 * np.pi * fs * t + np.pi/5)

# Разрядности АЦП для оценки
bit_depths = [3, 4, 5, 6]

# Словарь для хранения средних ошибок квантования
quantization_errors = {}


for num_bits in bit_depths:
    quantized_signal = quantize_signal(original_signal, num_bits)
    dft_result = np.fft.fft(quantized_signal)
    magnitude = np.abs(dft_result)
    
    
    quantization_error = np.mean(np.abs(original_signal - quantized_signal))
    quantization_errors[num_bits] = quantization_error
    
    plt.figure(figsize=(8, 6))
    plt.plot(magnitude)
    plt.title('Амплитудный спектр ({}-битное АЦП)'.format(num_bits))
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.grid(True)

# Вывод средних ошибок квантования для разных разрядностей АЦП
for num_bits, error in quantization_errors.items():
    print("Средняя ошибка квантования ({}-битное АЦП): {:.4f}".format(num_bits, error))

plt.show()