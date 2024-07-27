import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import simpledialog, messagebox
from tkinter import Text
from tkinter import Toplevel , font
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import signalcompare


def dft(x):
    N = len(x)
    X = np.zeros(N, dtype=complex)
    
    for k in range(N):
        for n in range(N):
            angle = 2 * np.pi * k * n / N
            X[k] += x[n] * np.exp(-1j * angle)
    
    return X
def idft(X):
    N = len(X)
    x = np.zeros(N, dtype=complex)
    
    for n in range(N):
        for k in range(N):
            angle = 2 * np.pi * k * n / N
            x[n] += X[k] * np.exp(1j * angle)
    
    return x / N
 # Define global variables
x, t, f, amp, phase = None, None, None, None, None
def apply_fourier_transform():
    global x, t, f, amp, phase , frequency_table 
    contents = open_file()
    if not contents:
        return
    for i in range(0, len(contents)):
        contents[i] = contents[i].strip()

    signal_type = int(contents[1])
    is_periodic = int(contents[0])
    n1 = int(contents[2])
    t = []
    data = []
    im = 1j
    phase_shift = []
    phase2=[]
    A = []
    img = []
    Amp=[]
    if signal_type == 0:
        for i in range(3, len(contents)):
            line = contents[i].split()
            t.append(float(line[1]))
        # Calculate the DFT of the signal
        freq_domain = dft(t)
        print("freq_domain : ",freq_domain)
        # Convert to polar form
        A = np.abs(freq_domain)
        phase_shift = np.angle(freq_domain)

        # Update the table with the new frequency components fft
        freq_table_frame = ttk.Frame(apply_dft_tab)
        freq_table_frame.grid(row=1, column=1, padx=2, pady=2, sticky='news')
        freq_canvas = tk.Canvas(freq_table_frame)
        freq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(freq_table_frame, orient="vertical", command=freq_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frequency_table = []
        for i in range(len(freq_domain)):
            frequency_table.append([
                tk.Entry(freq_canvas, width=10, textvariable=tk.StringVar(value=f'{A[i]:.4f}')),
                tk.Entry(freq_canvas, width=10, textvariable=tk.StringVar(value=f'{phase_shift[i]:.4f}')),
            ])
            for j in range(len(frequency_table[-1])):
                frequency_table[-1][j].grid(row=i, column=j)
        print(" time_domain : ",t)
        amp = A
        phase = phase_shift
        

        

        # # Plot the Time Domain signal
        x = np.arange(len(t))
    
        f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / 2 / len(t)
    
    elif signal_type == 1:  # Freq Domain
        
        
        for i in range(3, len(contents)):
            line = contents[i].split(',')
            line[0] = line[0].strip('f')
            line[1] = line[1].strip('f')
            Amp = float(line[0])
            phase2 = float(line[1])

            img.append((round(Amp * math.cos(phase2), 12) + round((Amp * math.sin(phase2)), 12) * im))
            
        time_domain = idft(img)
        

        real_time = np.zeros(n1, dtype=float)
        for i in range(0, len(time_domain)):
            time_domain[i] = round(time_domain[i], 12)
            real_time[i] = np.sqrt(time_domain[i].real ** 2 + time_domain[i].imag ** 2)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        f = np.linspace(0, sample_frequency_var.get() / 2, len(t))
        ax1.bar(f, np.abs(img), width=0.1, align='center', color='C0')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)
        # Plot the Signal in Time Domain
        time = np.arange(n1)
        ax2.plot(time, real_time, 'k')
        ax2.set_xlabel('Index')
        ax2.set.ylabel('Samples')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
        
        
    print("\nSignalComapreAmplitude  =  ",signalcompare.SignalComapreAmplitude(SignalInput=Amp, SignalOutput=A))
    print("\nSignalComaprePhaseShift  =  ",signalcompare.SignalComaprePhaseShift(SignalInput=phase2, SignalOutput=phase_shift))
    print("\n\n\n\n")
    
def open_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, 'r') as file:
            return file.readlines()
    return []

def read_and_reconstruct_signal():
    contents = open_file()
    if not contents:
        return

    for i in range(0, len(contents)):
        contents[i] = contents[i].strip()

    signal_type = int(contents[1])
    is_periodic = int(contents[0])
    n1 = int(contents[2])
    n = []
    im = 1j

    if signal_type == 0:  # Time Domain logic
        for i in range(3, len(contents)):
            line = contents[i].split()
            n.append(float(line[0]))
        x = np.array(n)

        t = []
        for i in range(3, len(contents)):
            line = contents[i].split()
            t.append(float(line[1]))

        # Calculate the correct phase shift for the frequency signal
        freq_signal = dft(t)
        f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / 2 / len(t)
        amp = np.abs(freq_signal)
        phase = np.angle(freq_signal)

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))
        ax1.plot(x[3:], t[3:], 'k')
        ax1.set_xlabel('Index')
        ax1.set_ylabel('Samples')
        ax1.grid(True)

        freq_signal = dft(t)
        f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / 2 / len(t)
        amp = np.abs(freq_signal)
        phase = np.angle(freq_signal)

        ax2.bar(f, amp, width=0.1, align='center', color='C0')
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True)

        A = []
        phase_shift = []
        for i in range(len(freq_signal)):
            A.append(math.sqrt(freq_signal[i].real ** 2 + freq_signal[i].imag ** 2))
            phase_shift.append(math.atan2(freq_signal[i].imag, freq_signal[i].real))

        freq_components = np.column_stack((A, phase_shift))

        global frequency_table
        freq_table_frame = ttk.Frame(read_file_tab)
        freq_table_frame.pack(side=tk.LEFT)
        freq_canvas = tk.Canvas(freq_table_frame)
        freq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(freq_table_frame, orient="vertical", command=freq_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frequency_table = []
        for i in range(len(freq_components)):
            frequency_table.append([tk.Entry(freq_canvas, width=10, textvariable=tk.StringVar(value=f'{A[i]:.4f}')),
                                    tk.Entry(freq_canvas, width=10, textvariable=tk.StringVar(value=f'{phase_shift[i] * (180 / math.pi):.4f}'))])
            for j in range(len(frequency_table[-1])):
                frequency_table[-1][j].grid(row=i, column=j)

        update_button = tk.Button(read_file_tab, text='Update', command=update_amplitude_phase)
        update_button.pack(pady=10)

        result_var.set("The file was read successfully")

        # Plot the Frequency vs. Amplitude subplot
        ax3.bar(f, phase_shift, width=0.1, align='center', color='C0')
        ax3.set_xlabel('Frequency')
        ax3.set_ylabel('Phase Shift')
        ax3.grid(True)

        plt.tight_layout()
        plt.show()

    elif signal_type == 1:  # Freq Domain
        img = []
        for i in range(3, len(contents)):
            line = contents[i].split(',')
            line[0] = line[0].strip('f')
            line[1] = line[1].strip('f')
            Amp = float(line[0])
            phase = float(line[1])

            img.append((round(Amp * math.cos(phase), 12) + round((Amp * math.sin(phase)), 12) * im))

        time_domain = idft(img)

        real_time = np.zeros(n1, dtype=float)
        for i in range(0, len(time_domain)):
            time_domain[i] = round(time_domain[i], 12)
            real_time[i] = np.sqrt(time_domain[i].real ** 2 + time_domain[i].imag ** 2)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        sample_frequency = float(sample_frequency_var.get())
        n1 = len(contents) - 3  # Assuming that the length of the data is determined by the contents

        f = np.arange(0, n1) * sample_frequency / 2 / n1

        ax1.bar(f*12.5, np.abs(img), width=0.1, align='center', color='C0')
        #ax1.stem(f, np.abs(img), linefmt='C0-', markerfmt='C0o', basefmt='C0-')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('input signal')
        ax1.grid(True)

        # Plot the Signal in Time Domain
        time = np.arange(n1)
        ax2.plot(time, real_time, 'k')
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Samples')
        ax2.set_title('Orignal signal')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

def update_amplitude_phase():
    for i in range(len(frequency_table)):
        freq_components[i, 0] = float(frequency_table[i][0].get())
        freq_components[i, 1] = float(frequency_table[i][1].get())
    update_plots()


def update_plots():
    amp = []
    phase = []
    for i in range(len(frequency_table)):
        amp.append(float(frequency_table[i][0].get()))
        phase.append(float(frequency_table[i][1].get()))

        # indent lines
    f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / 2 / len(t)

    # Plot the Frequency vs. Amplitude subplot
    ax2.clear()
    ax2.bar(f, amp, width=0.1, align='center', color='C0')
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True)

    # Plot the Frequency vs. Phase shift subplot
    ax3.clear()
    ax3.bar(f, phase, width=0.1, align='center', color='C0')
    ax3.set_xlabel('Frequency')
    ax3.set_ylabel('Phase Shift')
    ax3.grid(True)

    plt.tight_layout()
    plt.show()

# Function to create a new window and plot the subplots
def plot_subplots():
    global ax1, ax2, ax3, frequency_table
    
    amp = []
    phase_shift = []
    for i in range(len(frequency_table)):
        amp.append(float(frequency_table[i][0].get()))
        phase_shift.append(float(frequency_table[i][1].get()))

    f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / 2 / len(t)

    # Plot the Frequency vs. Amplitude subplot
    new_fig, (ax1, ax2,ax3) = plt.subplots(3, 1, figsize=(9, 7))

    # Plot the original signal after skipping the first 3 rows (index, samples)
    xm = np.arange(0,8,1)
    ax1.plot(xm, t[0:])
    # new_ax[0].plot(x[3:], t[3:],'k')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Samples')
    ax1.grid(True)

    #ax2.stem(f, amp, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
    ax2.bar(f*12.5, amp, width=0.1, align='center', color='C0')
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True)

    # Plot the Frequency vs. Phase shift subplot
    #ax3.stem(f, phase_shift, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
    ax3.bar(f*12.5, phase_shift, width=0.1, align='center', color='C0')
    ax3.set_xlabel('Frequency')
    ax3.set_ylabel('Phase Shift')
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
def save_file(data):
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[('Text File', '*.txt')])
    if not filename:
        return
    else:
        with open(filename, 'w') as f:
            f.write("0\n")  # Is periodic
            f.write("1\n")  # Signal type
            f.write(f"{len(data)}\n")  # Length of data
            for i in range(len(data)):
                f.write(f"{data[i][0].get()}f,{data[i][1].get()}f\n")
        result_var.set("\n\n\nData saved successfully")

root = tk.Tk()
root.title("Frequency Domain Menu")

main_frame = ttk.Frame(root)
main_frame.grid(column=0, row=0, padx=10, pady=10)

tabs = ttk.Notebook(main_frame)
tabs.pack(fill='both', expand=True)

apply_dft_tab = ttk.Frame(tabs)
read_file_tab = ttk.Frame(tabs)
#task 5
DCT_DC_tab = ttk.Frame(tabs)

tabs.add(apply_dft_tab, text="DFT")
tabs.add(read_file_tab, text="Read File_IDFT")
#task 5
tabs.add(DCT_DC_tab, text="DCT+DC")


sample_frequency_var = tk.StringVar()
sample_frequency_var.set('1.0')

input_label = ttk.Label(apply_dft_tab, text="Sample Frequency:")
input_label.grid(column=0, row=0, padx=5, pady=5)

input_entry = ttk.Entry(apply_dft_tab, textvariable=sample_frequency_var)
input_entry.grid(column=1, row=0, padx=5, pady=5)

apply_button = ttk.Button(apply_dft_tab, text="Load DFT Signal", command=apply_fourier_transform)
apply_button.grid(column=0, row=1, padx=5, pady=5)

result_var = tk.StringVar()
result_label = ttk.Label(apply_dft_tab, textvariable=result_var)
result_label.grid(column=0, row=2, padx=5, pady=5)

frequency_table = []
freq_table_frame = ttk.Frame(apply_dft_tab)
freq_table_frame.grid(row=1, column=1, padx=2, pady=2, sticky='news')

# Create the table headers
header_amp_label = ttk.Label(freq_table_frame, text="Amplitude")
header_amp_label.grid(row=0, column=0, padx=2, pady=2)
header_phase_label = ttk.Label(freq_table_frame, text="Phase Shift")
header_phase_label.grid(row=0, column=1, padx=2, pady=2)



# Add the initial data to the table
freq_components = np.zeros((1, 2))
amp_entry = tk.Entry(freq_table_frame, width=10, textvariable=tk.StringVar(value=f'0.0'))
amp_entry.grid(row=1, column=0, padx=2, pady=2)
phase_entry = tk.Entry(freq_table_frame, width=10, textvariable=tk.StringVar(value=f'0.0'))
phase_entry.grid(row=1, column=1, padx=2, pady=2)

frequency_table.append([amp_entry, phase_entry])

update_button = ttk.Button(apply_dft_tab, text='Update', command=update_amplitude_phase)
update_button.grid(row=2, column=0, pady=10)
save_button = ttk.Button(apply_dft_tab, text='Write file', command=lambda: save_file(frequency_table))
save_button.grid(row=3, column=0, pady=10)

plot_button = ttk.Button(apply_dft_tab, text="Plot Subplots", command=plot_subplots)
plot_button.grid(row=4, column=0, pady=10)

# Create the file dialog and read file button
read_file_button = ttk.Button(read_file_tab, text="Read File", command=read_and_reconstruct_signal)
read_file_button.grid(column=0, row=0, padx=5, pady=5)

file_selected_label = ttk.Label(read_file_tab, text="No file selected")
file_selected_label.grid(column=1, row=0, padx=5, pady=5)

fig = plt.Figure(figsize=(8, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=read_file_tab)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, padx=5, pady=5)

ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
root.mainloop()

