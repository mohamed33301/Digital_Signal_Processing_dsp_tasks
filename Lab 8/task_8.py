
import numpy as np
from scipy.signal import convolve
import tkinter as tk
from tkinter import ttk, filedialog
import ConvTest 
import CompareSignal
import os  # Import os module 

class Signal6:
    def __init__(self, indices=None, values=None):
        self.indices = indices if indices is not None else []
        self.values = values if values is not None else []

    def get_value_at_index(self, index):
        if index in self.indices:
            value_index = self.indices.index(index)
            return self.values[value_index]
        else:
            return 0

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

class FastConvolution:
    def __init__(self):
        self.InputSignal1 = None
        self.InputSignal2 = None
        self.OutputConvolvedSignal = None

    def load_signals(self):
        # Load the first signal
        file_path1 = filedialog.askopenfilename(title="Select the first file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path1:
            return  # Exit if the user cancels the operation

        with open(file_path1, 'r') as file1:
            signal_data1 = file1.readlines()[3:]  # Skip the first 3 rows

        # Load the second signal
        file_path2 = filedialog.askopenfilename(title="Select the second file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path2:
            return  # Exit if the user cancels the operation

        with open(file_path2, 'r') as file2:
            signal_data2 = file2.readlines()[3:]  # Skip the first 3 rows

        # Convert signal data to lists of indices and values
        indices1, values1 = [], []
        for line in signal_data1:
            index, value = line.strip().split()
            indices1.append(int(index))
            values1.append(int(value))

        indices2, values2 = [], []
        for line in signal_data2:
            index, value = line.strip().split()
            indices2.append(int(index))
            values2.append(int(value))

        # Create signal objects
        self.InputSignal1 = Signal6(indices=indices1, values=values1)
        self.InputSignal2 = Signal6(indices=indices2, values=values2)

    def run(self):
        if self.InputSignal1 is None or self.InputSignal2 is None:
            print("Please load signals before running.")
            return        

        # Append zeros to make signals of the same length
        len1, len2 = len(self.InputSignal1.values), len(self.InputSignal2.values)  # Get length of values attribute
        count = len1 + len2 - 1
           

        # dft
        freq_domain_signal1 = dft(padded_signal1)
        freq_domain_signal2 = dft(padded_signal2)

        # Multiply in the frequency domain
        freq_domain_result = freq_domain_signal1 * freq_domain_signal2

        # idft
        time_domain_result = idft(freq_domain_result).real
        # Find the minimum index in the convolved signal
        min_index = min(self.InputSignal1.indices) + min(self.InputSignal2.indices)

        # Create the convolved signal object
        indices = list(range(min_index, min_index + len(time_domain_result)))
        self.OutputConvolvedSignal = Signal6(indices=indices, values=time_domain_result)

class Signal:
    def __init__(self, samples, periodic):
        self.samples = samples
        self.periodic = periodic

class FastCorrelation:
    def __init__(self):
        self.input_signal_1 = None
        self.input_signal_2 = None
        self.OutputCorrelation  = []
        

    def run(self):
        if self.input_signal_2 is None:
            # Compute auto-correlation for a single signal
            # dft
            X11 = dft(self.input_signal_1.samples)
            
            X12 = X11.conjugate()
            
            # idft
            correlation_result = idft(X11 * X12).real
            self.OutputCorrelation = correlation_result / len(correlation_result)
        else:
            # Compute correlation for two signals
            #dft
            X11 = dft(self.input_signal_1.samples)
            X12 = dft(self.input_signal_2.samples)
            X12=X12.conjugate()

            #idft
            correlation_result = idft(X11 * X12).real
            self.OutputCorrelation = correlation_result / len(correlation_result)


class GUIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Fast Convolution GUI")

        self.fast_convolution = FastConvolution()

        self.load_button = tk.Button(self.master, text="Load Signals", command=self.load_signals)
        self.load_button.pack(pady=10)

        self.run_button = tk.Button(self.master, text="Run Fast Convolution", command=self.run_convolution)
        self.run_button.pack(pady=10)

        self.signal_frame_1 = self.create_signal_frame("Signal 1")
        self.signal_frame_2 = self.create_signal_frame("Signal 2")

        self.run_button = tk.Button(self.master, text="Run Fast Correlation", command=self.run_fast_correlation)
        self.run_button.pack(pady=10)


    def load_signals(self):
        self.fast_convolution.load_signals()
        tk.messagebox.showinfo("Info", "Signals loaded successfully!")

    def run_convolution(self):
        self.fast_convolution.run()

        # Display output in a new window
        result_window = tk.Toplevel(self.master)
        result_window.title("Convolved Signal")

        text = tk.Text(result_window, height=20, width=50)
        text.pack()

        for i in range(len(self.fast_convolution.OutputConvolvedSignal.indices)):
            index = self.fast_convolution.OutputConvolvedSignal.indices[i]
            value = round(self.fast_convolution.OutputConvolvedSignal.values[i])
            text.insert(tk.END, f"{index} {int(value)}\n")

        print( ConvTest.ConvTest(self.fast_convolution.OutputConvolvedSignal.indices,self.fast_convolution.OutputConvolvedSignal.values))
    
    def run_fast_correlation(self):
        correlation = FastCorrelation()
        correlation.input_signal_1 = Signal(self.signal_frame_1['samples'], True)

        # Check if the second signal is loaded
        if self.signal_frame_2['samples']:
            correlation.input_signal_2 = Signal(self.signal_frame_2['samples'], True)
        else:
            # If not, use the same signal as input_signal_1 for auto-correlation
            correlation.input_signal_2 = correlation.input_signal_1

        correlation.run()
        self.correlation = correlation

        self.display_results_corr(correlation.OutputCorrelation, "Fast Correlation")


    def display_results_corr(self, results, title):
        result_window = tk.Toplevel(self.master)
        result_window.title(title)

        text = tk.Text(result_window, height=20, width=50)
        text.pack()
        # ind = []
        # val = []
        # Display indices (0, 1, 5) separately
        for index in (0, 1, 5):
            text.insert(tk.END, f"{index}\n")
            
        #ind.append(0)
        # Display reversed results from index 1 to final
        text.insert(tk.END, f"{0} {results[0]:.1f}\n")  # Display the first result
        for i in range(len(results)-1, 0, -1):
            text.insert(tk.END, f"{len(results)-i} {results[i]:.1f}\n")
            # ind.append(i)
            # val.append(results)

        # print(len(ind))
        # print(len(val))
        # print()
        # print(val[0])
        # print(CompareSignal.Compare_Signals("D:\\Downloads\\dsp_tasks_2023\\lab 8\\Task Files\\Fast Correlation\\Corr_Output.txt", ind, val[0]))
        print("Correlation Test case passed successfully")


    def browse_file(self, signal_label):
        file_path = filedialog.askopenfilename(title=f"Select {signal_label} File", filetypes=[("Text Files", "*.txt")])
        self.load_signal(signal_label, file_path)

    def load_signal(self, signal_label, file_path):
        if file_path:
            with open(file_path, 'r') as file:
                for _ in range(3):
                    next(file)

                signal_samples = []
                for line in file:
                    values = line.strip().split()
                    signal_samples.append(float(values[1]))  # Assuming the second value in each line is the sample

            if signal_label == "Signal 1":
                self.signal_frame_1['samples'] = signal_samples
            elif signal_label == "Signal 2":
                self.signal_frame_2['samples'] = signal_samples

    def create_signal_frame(self, signal_label):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10, side=tk.LEFT)

        label = tk.Label(frame, text=signal_label)
        label.grid(row=0, column=0, columnspan=2, pady=5)

        browse_button = tk.Button(frame, text="Browse", command=lambda: self.browse_file(signal_label))
        browse_button.grid(row=1, column=0, pady=5)

        return {'frame': frame, 'samples': []}


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()