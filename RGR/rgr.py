    import numpy as np
    import matplotlib.pyplot as plt
    bin_name = []
    bin_name_full = []
    name = input("Enter Name ")
    surname = input("Enter Surname ")
    full_name = name+surname
    full_name_returnd = ""
    polinom = [1,0,1,1,1,0,1,1]

    register_x = [0,1,0,1,0]
    register_y = [1,0,0,0,1]
    print("Your name: ", full_name)
    
    
    def coder_to_bin(full_name):
        for i in full_name:
            bin_name.append(bin(ord(i))[2:])
        for i in bin_name:
            for j in i:
                bin_name_full.append(int(j)) 
            
    def coder_to_char(bin_nam): 
        full_name_returnd = ""
        for i in range(len(bin_nam)//7): 
            name = ""
            for j in range(i*7, (i*7)+7): 
                name += str(bin_nam[j])   
            full_name_returnd += chr(int(str(name),2)) 
        return full_name_returnd
    
    def calc_CRC(polinom,exten_data, result, LEN_G, N):
        temp = exten_data.copy()
        for i in range(N):
            if temp[i] == 1: 
                for j in range(LEN_G):
                    temp[j+i] = temp[j+i] ^ polinom[j] 
        for i in range(LEN_G-1):
            result[i] = temp[((LEN_G-1 + N)- LEN_G) + (i+1)] 
    
    
    def reg_x(register_x): 
        tmp = (register_x[2] + register_x[3])%2
        register_x = np.roll(register_x,1)
        register_x[0] = tmp
        return register_x
    def reg_y(register_y): 
        tmp = (register_y[1] + register_y[2])%2
        register_y = np.roll(register_y,1)
        register_y[0] = tmp
        return register_y
    
    def GoldSeq(register_x, register_y, seq, len_pos):
        for i in range(len_pos):
            seq[i] = (register_x[4] + register_y[4])%2
            
            register_x = reg_x(register_x)
            register_y = reg_y(register_y)
            
    def corr(gold, signal, LEN_S):
        max_corr = -100.2
        max_ind = 0
        temp = np.copy(signal) 
        temp2 = np.full(len(gold), fill_value=int(0)) 
        for i in range(len(temp)): 
            temp = np.roll(signal, -i)
            temp2 = temp[0:len(gold)]
            cor= np.correlate(temp2, gold)
            if cor > max_corr:
                max_corr = cor
                max_ind = i
        itog = signal[max_ind:]
        return itog
                
    def intr(signal, N, L, M, G):
        temp = np.full(N, fill_value=float(0)) 
        temp2 = np.copy(signal) 
        result = np.full(L+G+M, fill_value=int(0))
        for i in range(L+G+M): 
            for j in range(N): 
                temp[j] = temp2[j]
            temp2 = np.roll(temp2, -N) 
            if np.mean(temp) >= 0.5: 
               result[i] = 1
        
            else:
                result[i] = 0
        return result[G:]
                
                
        

    coder_to_bin(full_name)

    array = np.array(bin_name_full)

    
    L = len(array)
    M = len(polinom)-1 
    LEN_G = len(polinom)
    exten_N = L+M 
    exten_data = np.full(exten_N, fill_value=int(0))
    for i in range(len(array)):
        exten_data[i] = array[i]
    

    CRC = np.full(M, fill_value=int(0))

    calc_CRC(polinom, exten_data, CRC, LEN_G, L)
    print("CRC - ",CRC)

    for i in range(L, exten_N):
        exten_data[i] = CRC[i-L]
    
    
    G = len_pos = 2**5 -1 

    seq = np.full(len_pos, fill_value=int(0))

    GoldSeq(register_x, register_y, seq, len_pos)


    exten_data_full = np.concatenate((seq, exten_data), axis=0)

    
    
    N = 8 
    samples = np.repeat(exten_data_full,N) 
    LEN_S = len(samples) 
    
    t = np.arange(0,L)
    t2 = np.arange(0, exten_N + G)
    t3 = np.arange(0, len(samples))
    plt.figure(figsize=(10,5))
    
    plt.plot(t, array)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Data")
    
    plt.figure(2,figsize=(10, 5)) 

    plt.plot(t2, exten_data_full)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Gold+Data+CRC")
    
    plt.figure(3,figsize=(10,5))     
    plt.plot(t3, samples)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Сэмплы")
    
    

    Signal = np.full(2*N*(exten_N + G), fill_value=float(0))



    print("Enter the num from 0 to len(samples) ",len(samples) )
    ot = int(input(">> "))
    
    for i in range(ot, ot+len(samples)):
        Signal[i]=samples[i-ot]
    
        
    

    Signal_save = np.copy(Signal)
    

    q=float(input("Enter Sigma >> "))
    noice = np.random.normal(0, q, len(Signal)) 

    for i in range(len(Signal)):
        Signal[i] = Signal[i] + noice[i]
    
    
    
 
    ex_seq = np.repeat(seq,N)
    

    itog_signal = corr(ex_seq, Signal, LEN_S) 
    

    t4 = np.arange(0, len(samples)*2)
    t5 = np.arange(0, len(itog_signal))
    
    plt.figure(4,figsize=(10,5))
    plt.plot(t4, Signal_save)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Сигнал")
    
    plt.figure(5,figsize=(10, 5)) 
    plt.plot(t4, noice)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Шум")    
    
    plt.figure(6,figsize=(10, 5)) 
    plt.plot(t4, Signal)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Сигнал с шумом")    
    
    plt.figure(7,figsize=(10, 5)) 
    plt.plot(t5, itog_signal)
    plt.xlabel('элемент массива')
    plt.ylabel('значение')
    plt.title("Обрезанный сигнал")
    

    return_signal = intr(itog_signal, N, L, M, G)

    return_CRC = np.full(M, fill_value=int(0))
    calc_CRC(polinom, return_signal, return_CRC, LEN_G, L)
    if np.mean(return_CRC) > 0: 
        print("errors found");
    else:
        print("no errors found")
        return_data = return_signal[0:L]
        full_name_returnd = coder_to_char(return_data) 
        print("\n\n Recived Data", full_name_returnd)       
    
        ch=0 
        

        spect_signal = np.fft.fft(Signal_save)
        spect_noice_signal = np.fft.fft(Signal)
        
        if ch == 1:
            spect_signal = np.fft.fftshift(spect_signal)
            spect_noice_signal = np.fft.fftshift(spect_noice_signal)
        
        t1 = np.arange(0,len(spect_signal))
        plt.figure(8,figsize=(13, 20))
 
        plt.plot(t1, spect_signal, color='green')
        plt.figure(9,figsize=(13, 20))
        plt.xlabel('элемент массива')
        plt.ylabel('амплитуда')
        plt.title("Спектр передаваемого сигнала с N = 8")
    
 
        plt.plot(t1, spect_noice_signal, color='brown')
        plt.xlabel('элемент массива')
        plt.ylabel('амплитуда')
        plt.title("Спектр принимаемого сигнала с шумом и N = 8")
        
        
        samples_4N = np.repeat(exten_data_full,4)
        samples_16N = np.repeat(exten_data_full,16)
        Signal_4N = np.full(2*4*(exten_N + G), fill_value=float(0))
        Signal_16N = np.full(2*16*(exten_N + G), fill_value=float(0))
        for i in range(0, len(samples_4N)):
            Signal_4N[i]=samples_4N[i]
        for i in range(0, len(samples_16N)):
            Signal_16N[i]=samples_16N[i]
        
        spect_signal_4N = np.fft.fft(Signal_4N) 
        spect_signal_16N = np.fft.fft(Signal_16N)
        
            
        if ch == 1:
            spect_signal_4N = np.fft.fftshift(spect_signal_4N)
            spect_signal_16N = np.fft.fftshift(spect_signal_16N)
            
        noice = np.random.normal(0, q, len(Signal_4N))
        for i in range(len(Signal_4N)):
            Signal_4N[i] = Signal_4N[i] + noice[i]
        noice = np.random.normal(0, q, len(Signal_16N))
        for i in range(len(Signal_16N)):
            Signal_16N[i] = Signal_16N[i] + noice[i]
    
        spect_noice_signal_4N = np.fft.fft(Signal_4N)
        
        spect_noice_signal_16N = np.fft.fft(Signal_16N)
        
        if ch == 1:
            spect_noice_signal_4N = np.fft.fftshift(spect_noice_signal_4N)
            spect_noice_signal_16N = np.fft.fftshift(spect_noice_signal_16N)
        

        t2 = np.arange(0,len(spect_noice_signal_4N))
        t3 = np.arange(0,len(spect_noice_signal_16N))

        plt.figure(10,figsize=(13, 20))   
        plt.plot(t3, spect_signal_16N, color='blue')
        plt.plot(t1, spect_signal, color='brown')
        plt.plot(t2, spect_signal_4N, color='green')
        plt.xlabel('Частота')
        plt.ylabel('амплитуда')
        plt.title("Спектр передаваемого сигнала с N = 8, N=4, N = 16")
    
   
    
        plt.xlabel('Частота')
        plt.ylabel('амплитуда')
        plt.title("Спектр принимаемого сигнала с шумом и N = 8, N=4, N = 16")
        
        
        # Генерация значений частоты        
        
        spect_signal = np.fft.fft(Signal_save)
        spect_signal_16N = np.fft.fft(Signal_16N)
        spect_signal_4N = np.fft.fft(Signal_4N)
        

        freq_signal = np.fft.fftfreq(len(Signal_save))
        freq_signal_16N = np.fft.fftfreq(len(Signal_16N))
        freq_signal_4N = np.fft.fftfreq(len(Signal_4N))
        

        plt.figure(11,figsize=(13, 20))  
        plt.plot(freq_signal, spect_signal, color='brown', label='N=8')
        plt.plot(freq_signal_16N, spect_signal_16N, color='blue', label='N=16')
        plt.plot(freq_signal_4N, spect_signal_4N, color='green', label='N=4')
        plt.xlabel('Частота')
        plt.ylabel('амплитуда')
        plt.title("Спектр передаваемого сигнала с N = 8, N=4, N = 16")
        plt.legend()
        plt.show()
        
        
        
        
        
        
        
        
        