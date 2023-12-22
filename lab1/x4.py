import numpy as np
import matplotlib.pyplot as plt

f = 6
t = np.linspace(0, 1, 1000)
y = 6 * np.sin(2 * np.pi * f * t + np.pi/5)

Fs = 4 * 2 * f
duration = 1
num_samples = int(Fs * duration)
t2 = np.linspace(0, duration, num_samples)
y2 = 6 * np.sin(2 * np.pi * f * t + np.pi/5)


fft_result = np.fft.fft(y)
fft_freqs = np.fft.fftfreq(len(fft_result))
magnitude = np.abs(fft_result)


max_frequency_index = np.argmax(magnitude)
max_frequency = fft_freqs[max_frequency_index]


plt.figure(figsize=(8, 6))
plt.plot(t, y)
plt.title('График сигнала y(t) = 6*sin(2*pi*9*t + pi/5)')
plt.xlabel('Время (секунды)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()


plt.figure(figsize=(8, 6))
plt.plot(fft_freqs, magnitude)
plt.title('Амплитудный спектр')
plt.xlabel('Частота (Гц)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

print("Максимальная частота в спектре: {:.2f} Гц".format(np.abs(max_frequency)))


Fmax = np.abs(max_frequency)

Fs_min = 2 * Fmax

print("Минимальная необходимая частота дискретизации: {:.2f} Гц".format(Fs_min))

plt.plot(t2, y2)
plt.title('Оцифрованный сигнал')
plt.xlabel('Время (секунды)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

digital_signal = y

dft_result = np.fft.fft(digital_signal)


Fs_min = 2 * np.abs(np.max(np.fft.fftfreq(len(dft_result))))
spectral_width = Fs_min

 
memory_size_bytes = dft_result.nbytes

print("Ширина спектра: {:.2f} Гц".format(spectral_width))
print("Объем памяти для хранения массива DFT: {} байт".format(memory_size_bytes))

t_interpolated = np.linspace(0, duration, 4 * num_samples)
y_interpolated = np.interp(t_interpolated, t2, y2)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, y)
plt.title('Оригинальный сигнал')
plt.xlabel('Время (секунды)')
plt.ylabel('Амплитуда')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t_interpolated, y_interpolated)
plt.title('Восстановленный сигнал после оцифровки')
plt.xlabel('Время (секунды)')
plt.ylabel('Амплитуда')
plt.grid(True)

plt.tight_layout()
plt.show()