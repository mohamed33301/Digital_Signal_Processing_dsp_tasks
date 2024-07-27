import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox  # Import messagebox
import numpy as np
import matplotlib.pyplot as plt
import ConvTest 
import DerivativeSignal
import Shift_Fold_Signal



class Signal:
    def __init__(self, samples, boolean_value):
        self.samples = samples
        self.boolean_value = boolean_value
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


class Algorithm:
    pass

class MovingAverage(Algorithm):
    def __init__(self):
        self.input_signal = None
        self.input_window_size = 0
        self.output_average_signal = None

        self.InputSignal1 = None
        self.InputSignal2 = None
        self.OutputConvolvedSignal = None

    def run(self):
        samples = []
        for i in range(len(self.input_signal.samples) - self.input_window_size + 1):
            total_sum = sum(self.input_signal.samples[i:i + self.input_window_size])
            average = total_sum / self.input_window_size
            samples.append(average)

        self.output_average_signal = Signal(samples, False)

class Derivatives(Algorithm):
    def __init__(self):
        self.input_signal = None
        self.first_derivative = None
        self.second_derivative = None

    def run(self):
        output_signal_1 = [self.input_signal.samples[i] - self.input_signal.samples[i - 1] for i in range(1, len(self.input_signal.samples))]

        output_signal_2 = [self.input_signal.samples[j + 1] - (2 * self.input_signal.samples[j]) + self.input_signal.samples[j - 1] if j != len(self.input_signal.samples) - 1 else 0
                           for j in range(1, len(self.input_signal.samples))]

        self.first_derivative = Signal(output_signal_1, False)
        self.second_derivative = Signal(output_signal_2, False)

class MovingAverageGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Moving Average GUI")
        self.result_signals = {}  # Initialize result_signals
        self.shifting_constant = 0  # Initialize shifting_constant

        self.input_signal_label = tk.Label(self.master, text="Choose a file:")
        self.choose_file_button = tk.Button(self.master, text="Browse", command=self.load_signal_from_file)
        self.input_window_size_label = tk.Label(self.master, text="Enter window size:")
        self.input_window_size_entry = tk.Entry(self.master)

        # Add entry widget for input samples
        self.input_signal_entry = tk.Entry(self.master)

        self.run_button = tk.Button(self.master, text="Run Moving Average", command=self.run_moving_average)
        #self.derivative_button = tk.Button(self.master, text="Calculate Derivatives", command=self.calculate_derivatives)
        self.derivative_button = tk.Button(self.master, text="Calculate Derivatives", command=DerivativeSignal.DerivativeSignal)

        # New button for loading and shifting signal
        self.load_and_shift_button = tk.Button(self.master, text="Load and Shift Signal", command=self.load_and_shift_signal)
        self.load_and_shift_button.grid(row=5, column=0, columnspan=2, pady=10)

        # New button for plotting original and shifted signals      
        self.plot_both_button = tk.Button(self.master, text="Plot Original", command=self.plot_original_and_shifted2)
        self.plot_both_button.grid(row=6, column=0, columnspan=2, pady=10)

         # New button for loading and folding signal
        self.load_and_fold_button = tk.Button(self.master, text="Load and Fold Signal", command=self.load_and_fold_signal)
        self.load_and_fold_button.grid(row=10, column=0, columnspan=2, pady=10)

        # New button for plotting original and folded signals    
        self.plot_both_button = tk.Button(self.master, text="Plot Original and Folded", command=self.plot_original_and_folded)
        self.plot_both_button.grid(row=11, column=0, columnspan=2, pady=10)
      
        # New button for loading and folding signal
        self.load_and_fold_button = tk.Button(self.master, text="Load for shift_Fold", command=self.load_and_shift_signal)
        self.load_and_fold_button.grid(row=12, column=0, columnspan=2, pady=10)
        
        # New button for shift fold
        self.plot_both_button = tk.Button(self.master, text="plot Original + shift Fold", command=self.plot_original_and_shifted_fold)
        self.plot_both_button.grid(row=13, column=0, columnspan=2, pady=10)

        # New button for remove dc
        self.load_and_fold_button = tk.Button(self.master, text="Load for remove dc", command=self.choose_file)
        self.load_and_fold_button.grid(row=14, column=0, columnspan=2, pady=10)
        self.load_and_fold_button = tk.Button(self.master, text="Process Signal", command=self.load_and_remove_dc)
        self.load_and_fold_button.grid(row=15, column=0, columnspan=2, pady=10)

        

        # New button for loading s_convolution
        self.load_s_convolution_button = tk.Button(self.master, text="Load 2_s_convolution", command=self.load_s_convolution)
        self.load_s_convolution_button.grid(row=16, column=0, columnspan=2, pady=10)        


        # Grid layout
        self.input_signal_label.grid(row=0, column=0, padx=10, pady=10)
        self.choose_file_button.grid(row=0, column=1, padx=10, pady=10)
        self.input_window_size_label.grid(row=1, column=0, padx=10, pady=10)
        self.input_window_size_entry.grid(row=1, column=1, padx=10, pady=10)
        self.input_signal_entry.grid(row=2, column=1, padx=10, pady=10)  # Adjusted row
        self.run_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.derivative_button.grid(row=4, column=0, columnspan=2, pady=10)

    def load_signal_from_file(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                # Skip the first 3 rows
                for _ in range(3):
                    file.readline()

                signal_data = file.read()
                self.input_signal_label.config(text=f"File loaded: {file_path}")
                self.input_signal_entry.delete(0, tk.END)
                self.input_signal_entry.insert(0, signal_data)

    def run_moving_average(self):
        input_data = self.input_signal_entry.get()

        # Split the input by newline characters
        lines = input_data.split('\n')

        # Extract numerical values from each line
        input_samples = []
        for line in lines:
            try:
                value = float(line.split()[1])  # Assuming the value is at the second position in each line
                input_samples.append(value)
            except (ValueError, IndexError):
                # Ignore lines that don't have a valid numerical value
                pass

        window_size = int(self.input_window_size_entry.get())

        moving_average = MovingAverage()
        moving_average.input_signal = Signal(input_samples, False)
        moving_average.input_window_size = window_size
        moving_average.run()

        # Display the output in a new window
        output_window = tk.Toplevel(self.master)
        output_window.title("Moving Average Output")

        # Table to display output
        output_table = ttk.Treeview(output_window, columns=("Index", "Average"))
        output_table.heading("#0", text="Index")

        output_table.heading("Average", text="Moving Average")

        # Display the averages in the table
        for i, average in enumerate(moving_average.output_average_signal.samples):
            output_table.insert("", i+3, values=(i , round(average, 2)))

        output_table.grid(row=0, column=0, columnspan=2, padx=10, pady=10)



    def load_and_shift_signal(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                for _ in range(3):
                    file.readline()

                signal_data = file.read()
                self.input_signal_label.config(text=f"File loaded: {file_path}")
                self.input_signal_entry.delete(0, tk.END)
                self.input_signal_entry.insert(0, signal_data)

            constant = float(simpledialog.askstring("Input", "Enter the shifting constant value (use + or - for positive or negative values):"))
            # Store constant in the instance variable
            self.shifting_constant = constant
            
            signal = self.extract_signal_from_entry()
            self.perform_shifting(signal, constant)

    def plot_original_and_shifted2(self):
        shifted_signal = self.result_signals.get("Shifting")
        original_signal = self.extract_signal_from_entry()

        if original_signal is not None and shifted_signal is not None:
            # Plot Original Signal
            t_original = np.arange(-500, len(original_signal.samples)/2)  # Adjusted range
            plt.plot(t_original, original_signal.samples)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Original Signal')
            plt.legend()
            plt.show()

            # Plot Shifted Signal
            constant = self.shifting_constant  # Retrieve constant from the instance variable 
            if constant > 0:
                t_shifted = np.arange(-len(original_signal.samples), 0)
            else:
                t_shifted = np.arange(0, len(original_signal.samples))
        
            plt.plot(t_shifted, shifted_signal.samples,label="Shifting signal")
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Shifting Signal')
            plt.legend()
            plt.show()

    def extract_signal_from_entry(self):
        input_data = self.input_signal_entry.get()
        lines = input_data.split('\n')
        input_samples = []

        for line in lines:
            try:
                value = float(line.split()[1])
                input_samples.append(value)
            except (ValueError, IndexError):
                pass

        return Signal(input_samples, False)

    def plot_signal(self, signal, title):
        plt.plot(signal.samples)
        plt.xlabel('Index')
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.show()
    

    def create_plot_button(self, key, constant):
        button = tk.Button(
            self.master,
            text=f"Plot {key}",
            command=lambda: self.plot_signal(self.result_signals[key], f"{key} Signal", constant))
        button.grid(row=7, column=0, columnspan=2, pady=10)

    def perform_shifting(self, signal, constant):
        try:
            val = []
            ind = []

            for i in range(len(signal.samples)):
                ind.append(i - constant)  # Adjust the x-values (index)
                val.append(signal.samples[i])  # Keep the y-values (amplitude)

            result_signal = Signal(val, False)
            self.result_signals["Shifting"] = result_signal

            # Display result in a text file
            self.display_result_in_text_file(result_signal)

            self.display_message("Shifting performed successfully.")
            self.create_plot_button("Shifting")
        except ValueError:
            self.display_message("Invalid constant value.")
            return


    def fold_signal_operation(self, signal):
        try:
            folded_signal = Signal(signal.samples[::-1], False)
            return folded_signal
        except AttributeError:
            self.display_message("Error in folding signal. 'Signal' object should have a 'samples' attribute.")
            return None
            

    def display_result_in_text_file(self, result_signal):
        with open("result.txt", "w") as file:
            #file.write("Index\tValue\n")
            for i, value in enumerate(result_signal.samples):
                file.write(f"{i} {value}\n")

    def display_message(self, message):
        messagebox.showinfo("Info", message)

    def create_plot_button(self, key):
        button = tk.Button(self.master, text=f"Plot {key}", command=lambda: self.plot_original_and_shifted2())
        button.grid(row=8, column=0, columnspan=2, pady=10)

    
        
    def load_and_fold_signal(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                for _ in range(3):
                    file.readline()

                signal_data = file.read()
                self.input_signal_label.config(text=f"File loaded: {file_path}")
                self.input_signal_entry.delete(0, tk.END)
                self.input_signal_entry.insert(0, signal_data)

            folded_signal = self.fold_signal_operation(self.extract_signal_from_entry())
            self.result_signals["Folding"] = folded_signal

            # Display result in a text file
            self.display_result_in_text_file(folded_signal)
            self.display_message("Folding performed successfully.")

    def plot_original_and_folded(self):
        folded_signal = self.result_signals.get("Folding")
        original_signal = self.extract_signal_from_entry()

        if original_signal is not None and folded_signal is not None:
            # Plot Original and Folded Signals
            t_original = np.arange(-500, len(original_signal.samples) / 2)  # Adjusted range
            plt.plot(t_original, original_signal.samples, label="Original Signal")

            # Adjust the x-values (index) for the folded signal
            t_folded = np.arange(-500, len(original_signal.samples) / 2)
            plt.plot(t_folded, folded_signal.samples, label="Folded Signal")

            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Original and Folded Signals')
            plt.legend()
            plt.show()


    def plot_original_and_shifted_fold(self):
        shifted_signal = self.result_signals.get("Shifting")
        original_signal = self.extract_signal_from_entry()

        if original_signal is not None and shifted_signal is not None:
            # Create a figure with two subplots
            fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

            # Plot Original Signal
            t_original = np.arange(-500, len(original_signal.samples) / 2)  # Adjusted range
            axs[0].plot(t_original, original_signal.samples)
            axs[0].set_ylabel('Y')
            axs[0].set_title('Original Signal')

            # Plot Shifted Signal
            constant = self.shifting_constant  # Retrieve constant from the instance variable 
            if constant > 0:
                t_shifted = np.arange(0, len(original_signal.samples))
                print(Shift_Fold_Signal.Shift_Fold_Signal("D:\\Downloads\\dsp_tasks_2023\\Lab 6 (after midterm)-20231122T160337Z-001\\Lab 6 (after midterm)\\TestCases\\Shifting and Folding\\Output_ShifFoldedby500.txt",t_shifted, shifted_signal.samples))
                
            else:
                t_shifted = np.arange(-len(original_signal.samples), 0)
                print(Shift_Fold_Signal.Shift_Fold_Signal("D:\\Downloads\\dsp_tasks_2023\\Lab 6 (after midterm)-20231122T160337Z-001\\Lab 6 (after midterm)\\TestCases\\Shifting and Folding\\Output_ShiftFoldedby-500.txt",t_shifted, shifted_signal.samples))
               

            axs[1].plot(t_shifted, shifted_signal.samples, label="Shifting signal")
            axs[1].set_xlabel('X')
            axs[1].set_ylabel('Y')
            axs[1].set_title('Shifting Signal')

            # Display the plots
            plt.show()
    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    def load_and_remove_dc(self):
       
        if self.file_path:
            with open(self.file_path, "r") as file:
                input_lines = file.read().strip().split('\n')

            num_values = int(input_lines[2])  # Extracting the number of values from the third line

            # Process the remaining lines starting from the fourth line
            self.input_signal = [0.0] * num_values
            for line in input_lines[3:]:
                index, value = map(float, line.split())
                self.input_signal[int(index)] = value
        
            dc_result = self.remove_dc_component_operation(self.input_signal)

            output_window = tk.Toplevel(self.master)
            output_window.title("DC Result")

            table_label = tk.Label(output_window, text="DC Result:")
            table_label.pack()

            # Creating a treeview
            table = ttk.Treeview(output_window, columns=("Index", "Value"))
            table.heading("#0", text="Index")
            table.heading("#1", text="Value")

            for i, value in enumerate(dc_result.values):
                table.insert("", i, values=(i, value))

            table.pack()

    def display_result_in_text_file2(self, result_signal, file_path="result.txt"):
        with open(file_path, "w") as file:
            # file.write("Index\tValue\n")
            for i in range(len(result_signal.indices)):
                index = result_signal.indices[i]
                value = result_signal.values[i]
                file.write(f"{index} {value}\n")
                # file.write(f"{index} {value.real}\n")  


        self.display_message(f"Result saved successfully to {file_path}.")


    def remove_dc_component_operation(self, signal_values):
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

        x = np.array(signal_values, dtype=float)

        # (DFT)
        dft_result = dft(x)

        # Remove (first component)
        dft_result[0] = 0

        # (IDFT)
        modified_signal = idft(dft_result).real

       
        indices = list(range(len(modified_signal)))
        modified_signal_object = Signal6(indices=indices, values=modified_signal)

        return modified_signal_object


    # def s_convolution_operation(self):
    #     self.OutputConvolvedSignal = Signal6(indices=[], values=[])

    #     min_sample_index = self.InputSignal1.indices[0] + self.InputSignal2.indices[0]
        

    #     for n in range(min_sample_index+2,self.InputSignal1.indices[-1] + self.InputSignal2.indices[-1] + 3):
    #         element = 0
    #         for k in range(n + 1):
          
    #             signal_1_k_th_element = self.InputSignal1.values[k] if k < len(self.InputSignal1.values) else 0
    #             signal_2_n_minus_k_th_element = self.InputSignal2.values[n - k] if n - k < len(self.InputSignal2.values) else 0
    #             element += signal_1_k_th_element * signal_2_n_minus_k_th_element

    #         self.OutputConvolvedSignal.indices.append(min_sample_index)
    #         self.OutputConvolvedSignal.values.append(element)
    #         min_sample_index += 1

    #     while self.OutputConvolvedSignal.values[-1] == 0:
    #         self.OutputConvolvedSignal.values.pop()
    #         self.OutputConvolvedSignal.indices.pop()

    #     while self.OutputConvolvedSignal.values[0] == 0:
    #         self.OutputConvolvedSignal.values.pop(0)
    #         self.OutputConvolvedSignal.indices.pop(0)
    #         # test cases
    #     print( ConvTest.ConvTest(self.OutputConvolvedSignal.indices,self.OutputConvolvedSignal.values))

    def s_convolution_operation(self):
        if self.InputSignal1 is None or self.InputSignal2 is None:
            print("Error: Input signals are not loaded.")
            return

        self.OutputConvolvedSignal = Signal6(indices=[], values=[])

        min_sample_index = self.InputSignal1.indices[0] + self.InputSignal2.indices[0]

        for n in range(min_sample_index+2, self.InputSignal1.indices[-1] + self.InputSignal2.indices[-1] + 3):
            element = 0
            for k in range(n + 1):
                signal_1_k_th_element = self.InputSignal1.get_value_at_index(k)
                signal_2_n_minus_k_th_element = self.InputSignal2.get_value_at_index(n - k)
                element += signal_1_k_th_element * signal_2_n_minus_k_th_element

            self.OutputConvolvedSignal.indices.append(min_sample_index)
            self.OutputConvolvedSignal.values.append(element)
            min_sample_index += 1

        while self.OutputConvolvedSignal.values[-1] == 0:
            self.OutputConvolvedSignal.values.pop()
            self.OutputConvolvedSignal.indices.pop()

        while self.OutputConvolvedSignal.values[0] == 0:
            self.OutputConvolvedSignal.values.pop(0)
            self.OutputConvolvedSignal.indices.pop(0)

        # test cases
        print(ConvTest.ConvTest(self.OutputConvolvedSignal.indices, self.OutputConvolvedSignal.values))


    def load_s_convolution(self):
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

        # Perform s_convolution operation
        if self.InputSignal1 and self.InputSignal2:
            self.s_convolution_operation()
            self.result_signals["s_convolution"] = self.OutputConvolvedSignal

            # Ask the user for the file path to save the result
            save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

            if save_file_path:
                # Display result in a text file
                self.display_result_in_text_file2(self.OutputConvolvedSignal, save_file_path)
    


if __name__ == "__main__":
    root = tk.Tk()
    app = MovingAverageGUI(root)
    root.mainloop()
