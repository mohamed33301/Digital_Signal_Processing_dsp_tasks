import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import simpledialog, messagebox
from tkinter import Text
from tkinter import Toplevel , font
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.fft import fft, ifft
import QuanTest1
import QuanTest2
class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.amplitude = None
        self.root.title("Signal Processing Framework")

        # Create menu
        menubar = tk.Menu(root)
        signal_menu = tk.Menu(menubar, tearoff=0)
        signal_menu.add_command(label="Sine Wave", command=self.generate_sine_wave)
        signal_menu.add_command(label="Cosine Wave", command=self.generate_cosine_wave)
        menubar.add_cascade(label="Signal Generation", menu=signal_menu)

        # task 2
        # Create menu
        arithmetic_menu = tk.Menu(menubar, tearoff=0)
        arithmetic_menu.add_command(label="Addition", command=lambda: self.perform_arithmetic_operation("Addition"))
        arithmetic_menu.add_command(label="Subtraction", command=lambda: self.perform_arithmetic_operation("Subtraction"))
        arithmetic_menu.add_command(label="Multiplication", command=self.load_signal_for_multiplication)
        #arithmetic_menu.add_command(label="Squaring", command=lambda: self.perform_arithmetic_operation("Squaring"))
        arithmetic_menu.add_command(label="Squaring", command=self.load_signal_for_Squaring)
        arithmetic_menu.add_command(label="Shifting", command=self.load_signal_for_shifting)
        arithmetic_menu.add_command(label="Normalization", command=lambda: self.perform_arithmetic_operation("Normalization"))
        arithmetic_menu.add_command(label="Accumulation", command=lambda: self.perform_arithmetic_operation("Accumulation"))
        # task 3
        arithmetic_menu.add_command(label="quantization", command=self.load_signal_for_quantization)
        menubar.add_cascade(label="Arithmetic Operations", menu=arithmetic_menu)

        # task 4
        # Create menu
        menu_task4 = tk.Menu(menubar, tearoff=0)
        menu_task4.add_command(label="DFT/IDFT", command=self.open_frequency_domain_menu)
        menubar.add_cascade(label="Frequency Domain", menu=menu_task4)
       

        root.config(menu=menubar)

        # Create canvas for plotting
        self.fig, self.ax = plt.subplots(nrows=2, ncols=1, figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create buttons
        self.load_button = tk.Button(root, text="Load Signal", command=self.load_signal)
        self.load_button.pack(side=tk.LEFT)

        self.plot_buttons = []
        self.signals = []
        self.result_signals = {}

    def load_signal(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                signal = np.loadtxt(file, skiprows=3, usecols=[1])
                self.signals.append(signal)

    def load_signal_for_multiplication(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                signal = np.loadtxt(file, skiprows=3, usecols=[1])
                self.perform_multiplication(signal)


    def load_signal_for_shifting(self):
     file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
     if file_path:
         with open(file_path, "r") as file:
             signal = np.loadtxt(file, skiprows=3)
             x_values = signal[:, 0]  # Extract x-axis values from the signal
             constant = float(self.get_user_input("Enter the shifting constant value (use + or - for positive or negative values):"))
             self.perform_shifting(signal, constant)
    def load_signal_for_Squaring(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                signal = np.loadtxt(file, skiprows=3, usecols=[1])
                self.perform_Squaring(signal)

    def load_signal_for_quantization(self):
        # Create a new window for displaying the output
        output_window = Toplevel(self.root)
        output_window.title("Quantization Output")
        text_font = font.nametofont("TkDefaultFont")  # Get the default font
        text_font.configure(size=18)  # Set the font size to 12 (change 12 to your desired font size)
        output_text = Text(output_window, wrap=tk.WORD, height=20, width=60, font=text_font)
        output_text.pack()

        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                signal = np.loadtxt(file, skiprows=3)
                signal_list = signal.tolist()
                x_values = []
                y_values = []
                
                for item in signal_list:               
                    x_v, y_v = item
                    x_values.append((float(x_v)))
                    y_values.append((float(y_v)))
                choice = self.get_user_input("Enter 1 for specifying the number of bits, 2 for specifying the number of levels:")


            if choice == "1":
                # Test Case 1: Take number of bits from the user
                    num_bits = int(self.get_user_input("Enter the number of bits:"))               
                    encoded_signal_bits,formatted_quantized_signal=self.quantize_signal_bits(x_values,y_values,num_bits)
                    output_text.insert(tk.END, "   Encoded : quantized\n\n")
                    for item, item2 in zip(encoded_signal_bits, formatted_quantized_signal):
                        output_text.insert(tk.END, f"{' ' * 3} {item:8s} {' ' * 2} {item2:6.2f}\n")
                    #print("\nQuanTest1 = ",QuanTest1.QuantizationTest1(file_path,encoded_signal_bits,formatted_quantized_signal))
            elif choice == "2":
                    # Test Case 2: Take number of levels from the user
                    num_levels = int(self.get_user_input("Enter the number of levels:"))
                    Interval, encoded_signal_levels, quantized_signal_levels, quantization_error = self.quantize_signal_levels(x_values,y_values, num_levels)
                    output_text.insert(tk.END, "   Interval : Encoded : quantized : error\n\n")
                    for item, item2, item3, item4 in zip(Interval, encoded_signal_levels, quantized_signal_levels, quantization_error):
                        output_text.insert(tk.END, f"{' ' * 3} {item:1d} {' ' * 9} {item2:0s} {' ' * 8} {item3:7.3f} {' ' * 6} {item4:7.3f}\n")

                    #print("\nQuanTest = ",QuanTest2.QuantizationTest2)
    def generate_sine_wave(self):
        # Create a new window for user input
        sine_window = tk.Toplevel(self.root)
        sine_window.title("Sine Wave Parameters")

        # Create input fields
        amplitude_label = tk.Label(sine_window, text="Amplitude:")
        amplitude_label.pack()
        amplitude_entry = tk.Entry(sine_window)
        amplitude_entry.pack()

        phase_shift_label = tk.Label(sine_window, text="Phase Shift (radians):")
        phase_shift_label.pack()
        phase_shift_entry = tk.Entry(sine_window)
        phase_shift_entry.pack()

        analog_frequency_label = tk.Label(sine_window, text="Analog Frequency (Hz):")
        analog_frequency_label.pack()
        analog_frequency_entry = tk.Entry(sine_window)
        analog_frequency_entry.pack()

        sampling_frequency_label = tk.Label(sine_window, text="Sampling Frequency (Hz):")
        sampling_frequency_label.pack()
        sampling_frequency_entry = tk.Entry(sine_window)
        sampling_frequency_entry.pack()

        # Create a button to generate the sine wave
        generate_button = tk.Button(sine_window, text="Generate", command=lambda: self.generate_sine_wave_signal(amplitude_entry.get(),
                                                                                                            phase_shift_entry.get(),
                                                                                                            analog_frequency_entry.get(),
                                                                                                            sampling_frequency_entry.get(),
                                                                                                            sine_window))
        generate_button.pack()

    def generate_sine_wave_signal(self, amplitude, phase_shift, analog_frequency, sampling_frequency, window):
        self.amplitude = int(amplitude)
        phase_shift = float(phase_shift)
        analog_frequency = float(analog_frequency)
        sampling_frequency = float(sampling_frequency)

        t = np.arange(0, 1, 0.0001)
        signal = self.amplitude * np.sin(2 * np.pi * analog_frequency * t + phase_shift)
        self.signals.append(signal)

        if sampling_frequency < (2 * analog_frequency):
            print("Sampling frequency must be at least twice the analog frequency.")
            return

        window.destroy()

    def generate_cosine_wave(self):
        # Create a new window for user input
        cosine_window = tk.Toplevel(self.root)
        cosine_window.title("Cosine Wave Parameters")

        # Create input fields
        amplitude_label = tk.Label(cosine_window, text="Amplitude:")
        amplitude_label.pack()
        amplitude_entry = tk.Entry(cosine_window)
        amplitude_entry.pack()

        phase_shift_label = tk.Label(cosine_window, text="Phase Shift (radians):")
        phase_shift_label.pack()
        phase_shift_entry = tk.Entry(cosine_window)
        phase_shift_entry.pack()

        analog_frequency_label = tk.Label(cosine_window, text="Amplitude (Hz):")
        analog_frequency_label.pack()
        analog_frequency_entry = tk.Entry(cosine_window)
        analog_frequency_entry.pack()

        sampling_frequency_label = tk.Label(cosine_window, text="Sampling Frequency (Hz):")
        sampling_frequency_label.pack()
        sampling_frequency_entry = tk.Entry(cosine_window)
        sampling_frequency_entry.pack()

        # Create a button to generate the cosine wave
        generate_button = tk.Button(cosine_window, text="Generate", command=lambda: self.generate_cosine_wave_signal(amplitude_entry.get(),
                                                                                                                phase_shift_entry.get(),
                                                                                                                analog_frequency_entry.get(),
                                                                                                                sampling_frequency_entry.get(),
                                                                                                                cosine_window))
        generate_button.pack()

    def generate_cosine_wave_signal(self, amplitude, phase_shift, analog_frequency, sampling_frequency, window):
        self.amplitude = int(amplitude)
        phase_shift = float(phase_shift)
        analog_frequency = float(analog_frequency)
        sampling_frequency = float(sampling_frequency)

        t = np.arange(0, 1, 0.0001)
        signal = self.amplitude * np.cos(2 * np.pi * analog_frequency * t + phase_shift)
        self.signals.append(signal)

        if sampling_frequency < (2 * analog_frequency):
            print("Sampling frequency must be at least twice the analog frequency.")
            return

        window.destroy()

    def create_plot_button(self, operation_name):
        button = tk.Button(self.root, text=f"Plot {operation_name}", command=lambda: self.plot_operation(operation_name))
        self.plot_buttons.append(button)
        button.pack(side=tk.LEFT)

    def plot_operation(self, operation_name):
        result_signal = self.result_signals.get(operation_name, None)
        
        if result_signal is not None:
            fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6, 8))  # Updated to 3 subplots

            if operation_name in ["Addition", "Subtraction"]:
                # Plot the loaded signals and the result in separate subplots
                t = np.arange(0, len(self.signals[0]))
                axs[0].plot(t, self.signals[0])
                axs[0].set_xlabel('X')
                axs[0].set_ylabel('Y')
                axs[0].set_title('Loaded Signal 1')
                axs[0].legend()

                t = np.arange(0, len(self.signals[1]))
                axs[1].plot(t, self.signals[1])
                axs[1].set_xlabel('X')
                axs[1].set_ylabel('Y')
                axs[1].set_title('Loaded Signal 2')
                axs[1].legend()

                t = np.arange(0, len(result_signal))
                axs[2].plot(t, result_signal)
                axs[2].set_xlabel('X')
                axs[2].set_ylabel('Y')
                axs[2].set_title(f' {operation_name} Result')
                axs[2].legend()

            elif operation_name == "Multiplication":
                # Plot the loaded signal
                if len(self.signals) > 0:
                    t = np.arange(0, len(self.signals[0]))
                    axs[0].plot(t, self.signals[0])
                axs[0].set_xlabel('X')
                axs[0].set_ylabel('Y')
                axs[0].set_title(f'Original Signal')
                axs[0].legend()

                # Plot the result of multiplication
                t = np.arange(0, len(result_signal))
                axs[1].plot(t, result_signal)
                axs[1].set_xlabel('X\n')
                axs[1].set_ylabel('Y')
                axs[1].set_title(f'{operation_name} Result')
                axs[1].legend()

            elif operation_name == "Squaring":
                # Plot the loaded signal
                if len(self.signals) > 0:
                    t = np.arange(0, len(self.signals[0]))
                    axs[0].plot(t, self.signals[0])
                    axs[0].set_xlabel('X')
                    axs[0].set_ylabel('Y')
                    axs[0].set_title(f'Original Signal')
                    axs[0].legend()

                # Plot the result of multiplication
                t = np.arange(0, len(result_signal))
                axs[1].plot(t, result_signal)
                axs[1].set_xlabel('X')
                axs[1].set_ylabel('Y^2')
                axs[1].set_title(f'{operation_name} Result')
                axs[1].legend()

            elif operation_name == "Accumulation":
                # Plot the loaded signal
                if len(self.signals) > 0:
                    t = np.arange(0, len(self.signals[0]))
                    axs[0].plot(t, self.signals[0])
                    axs[0].set_xlabel('X')
                    axs[0].set_ylabel('Y')
                    axs[0].set_title(f'Original Signal')
                    axs[0].legend()

                # Plot the result of multiplication
                t = np.arange(0, len(result_signal))
                axs[1].plot(t, result_signal)
                axs[1].set_xlabel('X')
                axs[1].set_ylabel('Y')
                axs[1].set_title(f'{operation_name} Result')
                axs[1].legend()


            elif operation_name == "Shifting":
                # Plot the loaded signal
                if len(self.signals) > 0:
                    #len(self.signals[0])
                    t = np.arange(-500, len(self.signals[0])/2)
                    axs[0].plot(t, self.signals[0])
                    axs[0].set_xlabel('X')
                    axs[0].set_ylabel('Y')
                    axs[0].set_title(f'Original Signal')
                    axs[0].legend()

                if np.all(result_signal <= 0):
                    t = np.arange(-1000, len(result_signal))
                 
                    axs[1].plot( result_signal[:, 0],result_signal[:, 1])
                    axs[1].set_xlabel('X')
                    axs[1].set_ylabel('Y')
                    axs[1].set_title(f'{operation_name} Result')
                    axs[1].legend()

                else:
                    t = np.arange(0, len(result_signal))
                    axs[1].plot( result_signal[:, 0],result_signal[:, 1])
                    axs[1].set_xlabel('X')
                    axs[1].set_ylabel('Y')
                    axs[1].set_title(f'{operation_name} Result')
                    axs[1].legend()
     

            elif operation_name == "Normalization":
                # Plot the loaded signal
                if len(self.signals) > 0:
                    t = np.arange(0, len(self.signals[0]))
                    axs[0].plot(t, self.signals[0])
                axs[0].set_xlabel('X')
                axs[0].set_ylabel('Y')
                axs[0].set_title(f'Original Signal')
                axs[0].legend()

                # Plot the result 
                t = np.arange(0, len(result_signal))
                axs[1].plot(t, result_signal)
                axs[1].set_xlabel('X')
                axs[1].set_ylabel('Y')
                axs[1].set_title(f'\n{operation_name} Result')
                axs[1].legend()

            self.canvas.get_tk_widget().destroy()  # Remove the old canvas
            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def perform_arithmetic_operation(self, operation_name):
        if len(self.signals) < 2:
            self.display_message(f"At least 2 signals are required for {operation_name}.")
            return

        if operation_name == "Addition":
            result_signal = np.add(self.signals[0], self.signals[1])
        elif operation_name == "Subtraction":
            result_signal = np.subtract(self.signals[0], self.signals[1])


        elif operation_name == "Normalization":
            choice = self.get_user_input("Enter 1 for normalization from -1 to 1, 2 for normalization from 0 to 1:")
            if choice not in ["1", "2"]:
                self.display_message("Invalid choice.")
                return
            result_signal = self.normalize_signal(self.signals[0], choice)
        elif operation_name == "Accumulation":
            result_signal = np.cumsum(self.signals[0])

     
        else:
            result_signal = None

        if result_signal is not None:
            self.result_signals[operation_name] = result_signal
            self.display_message(f"{operation_name} performed successfully.")
            self.create_plot_button(operation_name)

    def normalize_signal(self, signal, choice):
        if choice == "1":
            min_value = np.min(signal)
            max_value = np.max(signal)
            normalized_signal = -1 + 2 * (signal - min_value) / (max_value - min_value)
        elif choice == "2":
            min_value = np.min(signal)
            max_value = np.max(signal)
            normalized_signal = (signal - min_value) / (max_value - min_value)
        else:
            normalized_signal = signal
        return normalized_signal

    def perform_multiplication(self, signal):
        constant = self.get_user_input("Enter the constant value for multiplication:")
        try:
            constant = float(constant)
        except ValueError:
            self.display_message("Invalid constant value.")
            return

        result_signal = signal * constant
        self.result_signals["Multiplication"] = result_signal
        self.display_message("Multiplication performed successfully.")
        self.create_plot_button("Multiplication")

    def perform_shifting(self, signal, constant):
     try:
        val = []  # List for y-values
        ind = []  # List for x-values

        for i in range(len(signal)):
                ind.append(signal[i][0] - constant)  # Adjust the x-values (time)
                val.append(signal[i][1])  # Keep the y-values (amplitude)
        result_signal = np.column_stack((ind, val))  # Create a new signal


        self.result_signals["Shifting"] = result_signal
        self.display_message("Shifting performed successfully.")
        self.create_plot_button("Shifting")
     except ValueError:
        self.display_message("Invalid constant value.")
        return

    def perform_Squaring(self, signal):
        
        result_signal = np.square(signal)
        self.result_signals["Squaring"] = result_signal
        self.display_message("Squaring performed successfully.")
        self.create_plot_button("Squaring")

# Function to quantize the signal based on the number of bits
    @staticmethod
    
    def quantize_signal_bits(x_values,y_values, num_bits):
        if num_bits <= 0:
            raise ValueError("Number of bits must be greater than 0")
        levels=pow(2,num_bits)
        Min=np.min(y_values)
        Max=np.max(y_values)
        delta=(Max- Min) / levels
        q=[]
        ra =[]
        tem = Min
        mmm=[]
        nnn=[]
        b=int(num_bits)
        n=int(levels)
        for i in range(len(y_values)):
            temp=round(float(tem+delta),4)
            mid=round((temp+tem)/2,4)
            q.append(mid)
            nnn.append(tem)
            tem=temp
            mmm.append(temp)
        for i in range(len(y_values)):
            for x in range(n):
                if y_values[i]<=mmm[x] and y_values[i]>=nnn[x]:
                    ra.append(x)
                    break
        result=[]
        for i in range(len(ra)):
            result.append(q[ra[i]])
        encod=[]
        bin3 = lambda x: ''.join(reversed([str((x >> i) & 1) for i in range(b)]))
        for i in range(len(ra)):
            encod.append(bin3(ra[i]))
        return encod,result
        
     # Function to quantize the signal based on the number of levels
    @staticmethod
    def quantize_signal_levels(x_values,y_values, num_levels):
        if num_levels <= 0:
            raise ValueError("Number of levels must be greater than 0")

        numb=math.log(num_levels,2)
        Min=np.min(y_values)
        Max=np.max(y_values)
        delta=(Max- Min) / num_levels
        delta=round(delta,3)
        q=[]
        ra =[]
        tem = Min
        mmm=[]
        nnn=[]
        n=int(numb)
        for i in range(len(y_values)):
            temp=round(float(tem+delta),3)
            mid=round((temp+tem)/2,3)
            q.append(mid)
            nnn.append(tem)
            tem=temp
            mmm.append(temp)

        for i in range(len(y_values)):
            for x in range(len(y_values)):
                if y_values[i]<=mmm[x] and y_values[i]>=nnn[x]:
                    ra.append(x)
                    break
        result=[]
        for i in range(len(ra)):
            result.append(q[ra[i]])
        encod=[]
        bin3 = lambda x: ''.join(reversed([str((x >> i) & 1) for i in range(n)]))
        for i in range(len(ra)):
            encod.append(bin3(ra[i]))
        er=[]
        for i in range(len(ra)):
            a=float(result[i]-y_values[i])
            a=round(a,3)
            er.append(a)
        for i in range(len(ra)):
            ra[i]=ra[i]+1
        return ra,encod,result,er
  
    def display_interval_indices(self, interval_indices):
        self.display_message("Interval Indices: " + ', '.join(map(str, interval_indices)))


    def get_user_input(self, prompt):
        return simpledialog.askstring("User Input", prompt)


    def display_message(self, message):
        messagebox.showinfo("Information", message)




    # task 4 
    
    def open_frequency_domain_menu(self):
        
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
            
            if signal_type == 0:
                for i in range(3, len(contents)):
                    line = contents[i].split()
                    t.append(float(line[1]))

                # Calculate the DFT of the signal
                freq_domain = np.fft.fft(t)
                A = []
                phase_shift = []
                # Convert to polar form
                A = np.abs(freq_domain)
                phase_shift = np.angle(freq_domain)

                # Update the table with the new frequency components
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

                amp = A
                phase = phase_shift

                # # Plot the Time Domain signal
                x = np.arange(len(t))
            
                f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / len(t)

            elif signal_type == 1:  # Freq Domain
                img = []
                for i in range(3, len(contents)):
                    line = contents[i].split(',')
                    line[0] = line[0].strip('f')
                    line[1] = line[1].strip('f')
                    Amp = float(line[0])
                    phase = float(line[1])

                    img.append((round(Amp * math.cos(phase), 12) + round((Amp * math.sin(phase)), 12) * im))

                time_domain = ifft(img)

                real_time = np.zeros(n1, dtype=float)
                for i in range(0, len(time_domain)):
                    time_domain[i] = round(time_domain[i], 12)
                    real_time[i] = np.sqrt(time_domain[i].real ** 2 + time_domain[i].imag ** 2)

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
                
                # Plot the Signal in Frequency Domain
                f = np.arange(n1)*(1/n1)*float(sample_frequency_var.get())
                ax1.stem(f, np.abs(img), linefmt='C0-', markerfmt='C0o', basefmt='C0-')
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
                freq_signal = np.fft.fft(t)
                f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / len(t)
                amp = np.abs(freq_signal)
                phase = np.angle(freq_signal)

                fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))
                ax1.plot(x[3:], t[3:], 'k')
                ax1.set_xlabel('Index')
                ax1.set_ylabel('Samples')
                ax1.grid(True)

                freq_signal = np.fft.fft(t)
                f = np.arange(0, len(t)) * float(sample_frequency_var.get()) / len(t)
                amp = np.abs(freq_signal)
                phase = np.angle(freq_signal)

                ax2.stem(f, amp, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
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
                ax3.stem(f, phase_shift, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
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

                time_domain = np.fft.ifft(img)

                real_time = np.zeros(n1, dtype=float)
                for i in range(0, len(time_domain)):
                    time_domain[i] = round(time_domain[i], 12)
                    real_time[i] = np.sqrt(time_domain[i].real ** 2 + time_domain[i].imag ** 2)

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
                # Plot the Signal in Frequency Domain
                f = np.arange(n1)*(1/n1)*float(sample_frequency_var.get())
                ax1.stem(f, np.abs(img), linefmt='C0-', markerfmt='C0o', basefmt='C0-')
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
            f = np.arange(len(amp)) * float(sample_frequency_var.get()) / len(amp)

            # Plot the Frequency vs. Amplitude subplot
            ax2.clear()
            ax2.stem(f, amp, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
            ax2.set_xlabel('Frequency')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True)

            # Plot the Frequency vs. Phase shift subplot
            ax3.clear()
            ax3.stem(f, phase, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
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

            f = np.arange(len(amp)) * float(sample_frequency_var.get()) / len(amp)

            # Plot the Frequency vs. Amplitude subplot
            new_fig, (ax1, ax2,ax3) = plt.subplots(3, 1, figsize=(9, 7))

            # Plot the original signal after skipping the first 3 rows (index, samples)
            xm = np.arange(0,8,1)
            ax1.plot(xm, t[0:])
            # new_ax[0].plot(x[3:], t[3:],'k')
            ax1.set_xlabel('Index')
            ax1.set_ylabel('Samples')
            ax1.grid(True)

            ax2.stem(f, amp, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
            ax2.set_xlabel('Frequency')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True)

            # Plot the Frequency vs. Phase shift subplot
            ax3.stem(f, phase_shift, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
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

        tabs.add(apply_dft_tab, text="DFT")
        tabs.add(read_file_tab, text="Read File_IDFT")

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
        
         

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()

# root = tk.Tk()
# app = SignalProcessingApp(root)
# root.mainloop()

