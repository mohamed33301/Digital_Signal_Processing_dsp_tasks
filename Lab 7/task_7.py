

import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import CompareSignal
import os  # Import os module

class Signal:
    def __init__(self, samples, periodic):
        self.samples = samples
        self.periodic = periodic

class DirectCorrelation:
    def __init__(self):
        self.input_signal_1 = None
        self.input_signal_2 = None
        self.output_non_normalized_correlation = []
        self.output_normalized_correlation = []

    def run(self):
        if (
            self.input_signal_1 is not None
            and self.input_signal_2 is not None
            and len(self.input_signal_1.samples) == len(self.input_signal_2.samples)
        ):
            size = len(self.input_signal_1.samples)

            for i in range(size):
                temp = 0
                for j in range(size):
                    if self.input_signal_2.periodic:
                        temp += np.sum(np.multiply(self.input_signal_1.samples[j], self.input_signal_2.samples[(i + j) % size]))
                    else:
                        temp += np.sum(np.multiply(self.input_signal_1.samples[j], self.input_signal_2.samples[i + j]))

                self.output_non_normalized_correlation.append(temp / size)
                self.output_normalized_correlation.append((temp / size) / (np.sqrt(np.sum(np.square(self.input_signal_1.samples)) * np.sum(np.square(self.input_signal_2.samples))) / size))

        else:
            print("Error: Both signals must be loaded and have the same length")


class TimeDelay:
    def __init__(self):
        self.input_signal_1 = None
        self.input_signal_2 = None
        self.input_sampling_period = None
        self.output_time_delay = None

    def run(self):
        dc = DirectCorrelation()

        dc.input_signal_1 = self.input_signal_1
        dc.input_signal_2 = self.input_signal_2

        dc.run()
        maxi = 0
        conu = 0

        for i in range(len(dc.output_non_normalized_correlation)):
            if dc.output_non_normalized_correlation[i] > maxi:
                maxi = dc.output_non_normalized_correlation[i]
                conu = i

        self.output_time_delay = conu * self.input_sampling_period


class CorrelationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Correlation App")

        self.signal_frame_1 = self.create_signal_frame("Signal 1")
        self.signal_frame_2 = self.create_signal_frame("Signal 2")

        self.run_button = tk.Button(self.master, text="Run Normalized Correlation", command=self.run_correlation)
        self.run_button.pack(pady=10)

        self.run_button = tk.Button(self.master, text="Run Non Normalized Correlation", command=self.run_correlation_time)
        self.run_button.pack(pady=10)

        self.sampling_period_entry = ttk.Entry(self.master)
        self.sampling_period_entry.insert(0, "")
        self.sampling_period_entry.pack(pady=10)

        self.calculate_time_delay_button = tk.Button(self.master, text="Calculate Time Delay", command=self.calculate_time_delay)
        self.calculate_time_delay_button.pack(pady=10)

        self.expected_output_label = tk.Label(self.master, text="")
        self.expected_output_label.pack(pady=10)

        self.correlation = None
        self.correlation_result = None
        self.time_delay_analysis = TimeDelay()

        self.class1_folder = tk.StringVar()
        self.class2_folder = tk.StringVar()
        self.test_file = tk.StringVar()

        self.create_folder_entry("Class 1 Folder", self.class1_folder)
        self.create_folder_entry("Class 2 Folder", self.class2_folder)
        self.create_file_entry("Test File", self.test_file)

        self.run_button = tk.Button(self.master, text="Run Template Matching", command=self.run_template_matching)
        self.run_button.pack(pady=10)

    def create_folder_entry(self, label_text, variable):
        label = tk.Label(self.master, text=label_text)
        label.pack(pady=5)

        entry_frame = tk.Frame(self.master)
        entry_frame.pack(pady=5)

        entry = tk.Entry(entry_frame, textvariable=variable, width=40)
        entry.grid(row=0, column=0)

        browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_folder(variable))
        browse_button.grid(row=0, column=1)

    def create_file_entry(self, label_text, variable):
        label = tk.Label(self.master, text=label_text)
        label.pack(pady=5)

        entry_frame = tk.Frame(self.master)
        entry_frame.pack(pady=5)

        entry = tk.Entry(entry_frame, textvariable=variable, width=40)
        entry.grid(row=0, column=0)

        browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_file_t(variable))
        browse_button.grid(row=0, column=1)

    def browse_folder(self, variable):
        folder_path = filedialog.askdirectory(title="Select Folder")
        variable.set(folder_path)

    def browse_file_t(self, variable):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])
        variable.set(file_path)

    def load_templates(self, folder_path):
        templates = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    template_samples = [float(line.strip()) for line in file]
                    templates.append(template_samples)
        return templates

    def load_signals(self, file_path):
        signals = []
        with open(file_path, 'r') as file:
            for line in file:
                signal_samples = [float(value) for value in line.strip().split()]
                signals.append(signal_samples)
        return signals

    def calculate_correlation(self, signal, template):
        signal_samples = np.array(signal.samples) if isinstance(signal, Signal) else np.array(signal)
        template_samples = np.array(template.samples) if isinstance(template, Signal) else np.array(template)

        size = len(signal_samples)
        raw_result = self.correlate(signal_samples, template_samples)

        return [val / size for val in raw_result] if len(raw_result) > 0 else [0.0]


    def run_template_matching(self):
        class1_folder = self.class1_folder.get()
        class2_folder = self.class2_folder.get()
        test_file = self.test_file.get()

        class1_templates = self.load_templates(class1_folder)
        class2_templates = self.load_templates(class2_folder)
        test_signals = self.load_signals(test_file)

        class1_average = Signal(np.mean(class1_templates, axis=0), periodic=False)
        class2_average = Signal(np.mean(class2_templates, axis=0), periodic=False)

        corr_class1 = self.calculate_correlation(test_signals[0], class1_average)  
        corr_class2 = self.calculate_correlation(test_signals[0], class2_average)  

        bigger_corr = max(corr_class1, corr_class2)

        if bigger_corr == corr_class1:
            movement = "Class 1: Down Movement"
        else:
            movement = "Class 2: Up Movement"

        print(f"Test signal 1: {movement} (Correlation: {bigger_corr})")

    def correlate(self, signal, template):
        size = len(signal)
        result = []

        for i in range(size):
            temp = 0
            for j in range(len(template)):
                if i + j < size:
                    temp += signal[i + j] * template[j]

            result.append(temp)

        return result

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

    def run_correlation(self):
        correlation = DirectCorrelation()
        correlation.input_signal_1 = Signal(self.signal_frame_1['samples'], True)
        correlation.input_signal_2 = Signal(self.signal_frame_2['samples'], True)
        correlation.run()
        self.correlation = correlation

        self.display_results(correlation.output_normalized_correlation, "Normalized Correlation")

    def display_results(self, results, title):
        result_window = tk.Toplevel(self.master)
        result_window.title(title)

        text = tk.Text(result_window, height=20, width=50)
        text.pack()

        size = len(results)
        index = []
        val = []

        for i, result in enumerate(results):
            if i == 0:
                text.insert(tk.END, "0\n")
                text.insert(tk.END, "1\n")
                text.insert(tk.END, "5\n")
            text.insert(tk.END, f"{i} {result:.8f}\n")
            index.append(i)
            val.append(result)

        print(len(index))
        print(len(val))
        print(CompareSignal.Compare_Signals("D:\\Downloads\\dsp_tasks_2023\\lab 7\\SC and Csys\\Task Files\\Point1 Correlation\\CorrOutput.txt", index, val))

    def run_correlation_time(self):
        correlation = DirectCorrelation()
        correlation.input_signal_1 = Signal(self.signal_frame_1['samples'], True)
        correlation.input_signal_2 = Signal(self.signal_frame_2['samples'], True)
        correlation.run()
        self.correlation = correlation

        self.display_results_time(correlation.output_non_normalized_correlation, "Non Normalized Correlation")

    def display_results_time(self, results, title):
        result_window = tk.Toplevel(self.master)
        result_window.title(title)

        text = tk.Text(result_window, height=20, width=50)
        text.pack()
        size = len(results)
        for i, result in enumerate(results):
            if i == 0:
                text.insert(tk.END, "0\n")
                text.insert(tk.END, "1\n")
                text.insert(tk.END, "5\n")
            text.insert(tk.END, f"{i} {result:.8f}\n")

    def calculate_time_delay(self):
        self.correlation.run()  # correlation

        max_corr = max(abs(result) for result in self.correlation.output_non_normalized_correlation)  # max absolute value
        j = self.correlation.output_non_normalized_correlation.index(max_corr)  # save its lag (j)

        time_delay = j * float(self.sampling_period_entry.get())  # Time delay= j * Ts

        self.expected_output_label.config(text=f"Expected Output = {time_delay}")
        print("expected output = ", time_delay)

if __name__ == "__main__":
    root = tk.Tk()
    app = CorrelationApp(root)
    root.mainloop()

