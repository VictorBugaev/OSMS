import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import sounddevice as sd


audio_path = 'Recording.wav'
y, sr = librosa.load(audio_path)

num_samples = y.size
duration = librosa.get_duration(y=y, sr=sr)
Fs = num_samples / duration
print("Частота дискретизации: {:.2f} Гц".format(Fs))

# Уменьшаем частоту дискретизации
new_sr = 2205
y_downsampled = scipy.signal.resample(y, int(len(y) * new_sr / sr))
sd.play(y_downsampled, new_sr)
sd.wait()


def plot_amplitude_spectrum(y, title):
    dft_result = np.fft.fft(y)
    fft_freqs = np.fft.fftfreq(len(dft_result)) * 10000
    magnitude = np.abs(dft_result)

    plt.figure(figsize=(8, 6))
    plt.plot(abs(fft_freqs), magnitude)
    plt.title(title)
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()


# Визуализация аудиосигнала
plt.figure(figsize=(12, 6))
librosa.display.waveshow(y, sr=sr)
plt.title('Аудиосигнал')
plt.xlabel('Время (секунды)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

# Извлечение спектрограммы
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
plt.figure(figsize=(12, 6))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Спектрограмма')
plt.show()

plot_amplitude_spectrum(y, 'Амплитудный спектр оригинального сигнала')

plot_amplitude_spectrum(y_downsampled, 'Амплитудный спектр прореженного сигнала')
