% Определение длины последовательности
LENGTH = 5;
cons = 2^LENGTH - 1;

% Инициализация регистров Голда
register_state_x = [0, 0, 0, 1, 1];
register_state_y = [0, 1, 0, 1, 0];
register_state_x1 = [0, 0, 1, 0, 0];
register_state_y1 = [0, 0, 1, 0, 1];

% Генерация последовательности Голда и измененной последовательности
pseudo_random_sequence = generate_pseudo_random_sequence(register_state_x, register_state_y, cons);
modified_sequence = generate_pseudo_random_sequence(register_state_x1, register_state_y1, cons);

% Генерация сдвинутых последовательностей для вычисления автокорреляции
shifted_sequences = zeros(cons, cons);
for shift = 1:cons
    shifted_sequences(shift, :) = circshift(pseudo_random_sequence, [0, shift-1]);
end

% Вычисление автокорреляции и взаимной корреляции
autocorrelation_values = autocorr(pseudo_random_sequence, cons-1);
crosscorrelation = xcorr(pseudo_random_sequence, modified_sequence);

% Вывод результатов
fprintf('Автокорреляция:\n');
disp(autocorrelation_values');

fprintf('Взаимная корреляция двух последовательностей голда:\n');
disp(crosscorrelation);

% Построение графика автокорреляции
lag = 0:cons-1;
figure;
stem(lag, autocorrelation_values);
title('Autocorrelation vs Delay');
xlabel('Delay');
ylabel('Autocorrelation');
grid on;

