

# import tkinter as tk
# from tkinter import ttk, filedialog
# import math
# import numpy as np
# import CompareSignal

# class Signal:
#     def __init__(self, samples, periodic):
#         self.samples = samples
#         self.periodic = periodic

# class DirectCorrelation:
#     def __init__(self):
#         self.input_signal_1 = None
#         self.input_signal_2 = None
#         #self.output_non_normalized_correlation = []
#         self.output_normalized_correlation = []

#     def run(self):
#         if (
#             self.input_signal_1 is not None
#             and self.input_signal_2 is not None
#             and len(self.input_signal_1.samples) == len(self.input_signal_2.samples)
#         ):
#             size = len(self.input_signal_1.samples)

#             for i in range(size):
#                 temp = 0
#                 for j in range(size):
#                     if self.input_signal_2.periodic:
                        
#                         temp += np.sum(np.multiply(self.input_signal_1.samples[j], self.input_signal_2.samples[(i + j) % size]))
#                     else:
#                         temp += np.sum(np.multiply(self.input_signal_1.samples[j], self.input_signal_2.samples[i + j]))

#                 self.output_normalized_correlation.append((temp / size) / (np.sqrt(np.sum(np.square(self.input_signal_1.samples)) * np.sum(np.square(self.input_signal_2.samples))) / size))

        
#         else:
#             print("Error: Both signals must be loaded and have the same length")

# class CorrelationApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Correlation App")

#         self.signal_frame_1 = self.create_signal_frame("Signal 1")
#         self.signal_frame_2 = self.create_signal_frame("Signal 2")

#         self.run_button = tk.Button(self.master, text="Run Correlation", command=self.run_correlation)
#         self.run_button.pack(pady=10)

#     def browse_file(self, signal_label):
#         file_path = filedialog.askopenfilename(title=f"Select {signal_label} File", filetypes=[("Text Files", "*.txt")])
#         self.load_signal(signal_label, file_path)

#     def load_signal(self, signal_label, file_path):
#         if file_path:
#             with open(file_path, 'r') as file:
#                 for _ in range(3):
#                     next(file)

#                 signal_samples = []
#                 for line in file:
#                     values = line.strip().split()
#                     signal_samples.append(float(values[1]))  # Assuming the second value in each line is the sample

#             if signal_label == "Signal 1":
#                 self.signal_frame_1['samples'] = signal_samples
#             elif signal_label == "Signal 2":
#                 self.signal_frame_2['samples'] = signal_samples

#     def create_signal_frame(self, signal_label):
#         frame = ttk.Frame(self.master)
#         frame.pack(padx=10, pady=10, side=tk.LEFT)

#         label = tk.Label(frame, text=signal_label)
#         label.grid(row=0, column=0, columnspan=2, pady=5)

#         browse_button = tk.Button(frame, text="Browse", command=lambda: self.browse_file(signal_label))
#         browse_button.grid(row=1, column=0, pady=5)

#         return {'frame': frame, 'samples': []}

#     def run_correlation(self):
#         correlation = DirectCorrelation()
#         correlation.input_signal_1 = Signal(self.signal_frame_1['samples'], True)  
#         correlation.input_signal_2 = Signal(self.signal_frame_2['samples'], True)  
#         correlation.run()

#         self.display_results(correlation.output_normalized_correlation, "Normalized Correlation")

#     def display_results(self, results, title):
#         result_window = tk.Toplevel(self.master)
#         result_window.title(title)

#         text = tk.Text(result_window, height=20, width=50)
#         text.pack()

#         size = len(results)
#         index = []
#         val=[]

#         for i, result in enumerate(results):
#             if i==0:
#                 text.insert(tk.END, "0\n")
#                 text.insert(tk.END, "1\n")
#                 text.insert(tk.END, "5\n")
#             text.insert(tk.END, f"{i} {result:.8f}\n")
#             index.append(i)
#             val.append(result) 
        
#         print(len(index))
#         print(len(val))
#         print(CompareSignal.Compare_Signals("D:\\Downloads\\dsp_tasks_2023\\lab 7\\SC and Csys\\Task Files\\Point1 Correlation\\CorrOutput.txt", index , val))
        



# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CorrelationApp(root)
#     root.mainloop()




# import tkinter as tk
# from tkinter import ttk, filedialog
# import math
# import numpy as np
# import CompareSignal

# class Signal:
#     def __init__(self, samples, periodic):
#         self.samples = samples
#         self.periodic = periodic

# class DirectCorrelation:
#     def __init__(self):
#         self.input_signal_1 = None
#         self.input_signal_2 = None
#         #self.output_non_normalized_correlation = []
#         self.output_normalized_correlation = []

#     def run(self):
#         if (
#             self.input_signal_1 is not None
#             and self.input_signal_2 is not None
#             and len(self.input_signal_1.samples) == len(self.input_signal_2.samples)
#         ):
#             size = len(self.input_signal_1.samples)

#             for i in range(size):
#                 temp = 0
#                 for j in range(size):
#                     if self.input_signal_2.periodic:
                        
#                         temp += np.sum(np.multiply(self.input_signal_1.samples[j], self.input_signal_2.samples[(i + j) % size]))
#                     else:
#                         temp += np.sum(np.multiply(self.input_signal_1.samples[j], self.input_signal_2.samples[i + j]))

#                 self.output_normalized_correlation.append((temp / size) / (np.sqrt(np.sum(np.square(self.input_signal_1.samples)) * np.sum(np.square(self.input_signal_2.samples))) / size))

        
#         else:
#             print("Error: Both signals must be loaded and have the same length")

# class CorrelationApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Correlation App")

#         self.signal_frame_1 = self.create_signal_frame("Signal 1")
#         self.signal_frame_2 = self.create_signal_frame("Signal 2")

#         self.run_button = tk.Button(self.master, text="Run Correlation", command=self.run_correlation)
#         self.run_button.pack(pady=10)

#     def browse_file(self, signal_label):
#         file_path = filedialog.askopenfilename(title=f"Select {signal_label} File", filetypes=[("Text Files", "*.txt")])
#         self.load_signal(signal_label, file_path)

#     def load_signal(self, signal_label, file_path):
#         if file_path:
#             with open(file_path, 'r') as file:
#                 for _ in range(3):
#                     next(file)

#                 signal_samples = []
#                 for line in file:
#                     values = line.strip().split()
#                     signal_samples.append(float(values[1]))  # Assuming the second value in each line is the sample

#             if signal_label == "Signal 1":
#                 self.signal_frame_1['samples'] = signal_samples
#             elif signal_label == "Signal 2":
#                 self.signal_frame_2['samples'] = signal_samples

#     def create_signal_frame(self, signal_label):
#         frame = ttk.Frame(self.master)
#         frame.pack(padx=10, pady=10, side=tk.LEFT)

#         label = tk.Label(frame, text=signal_label)
#         label.grid(row=0, column=0, columnspan=2, pady=5)

#         browse_button = tk.Button(frame, text="Browse", command=lambda: self.browse_file(signal_label))
#         browse_button.grid(row=1, column=0, pady=5)

#         return {'frame': frame, 'samples': []}

#     def run_correlation(self):
#         correlation = DirectCorrelation()
#         correlation.input_signal_1 = Signal(self.signal_frame_1['samples'], True)  
#         correlation.input_signal_2 = Signal(self.signal_frame_2['samples'], True)  
#         correlation.run()

#         self.display_results(correlation.output_normalized_correlation, "Normalized Correlation")

#     def display_results(self, results, title):
#         result_window = tk.Toplevel(self.master)
#         result_window.title(title)

#         text = tk.Text(result_window, height=20, width=50)
#         text.pack()

#         size = len(results)
#         index = []
#         val=[]

#         for i, result in enumerate(results):
#             if i==0:
#                 text.insert(tk.END, "0\n")
#                 text.insert(tk.END, "1\n")
#                 text.insert(tk.END, "5\n")
#             text.insert(tk.END, f"{i} {result:.8f}\n")
#             index.append(i)
#             val.append(result) 
        
#         print(len(index))
#         print(len(val))
#         print(CompareSignal.Compare_Signals("D:\\Downloads\\dsp_tasks_2023\\lab 7\\SC and Csys\\Task Files\\Point1 Correlation\\CorrOutput.txt", index , val))
        



# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CorrelationApp(root)
#     root.mainloop()










