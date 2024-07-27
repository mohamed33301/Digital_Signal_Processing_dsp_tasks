# import cv2
# import numpy as np
# import os
# import tkinter as tk
# from tkinter import filedialog

# class TemplateMatchingApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Template Matching App")

#         self.class1_folder = tk.StringVar()
#         self.class2_folder = tk.StringVar()
#         self.test_file = tk.StringVar()

#         self.create_folder_entry("Class 1 Folder", self.class1_folder)
#         self.create_folder_entry("Class 2 Folder", self.class2_folder)
#         self.create_file_entry("Test File", self.test_file)

#         self.run_button = tk.Button(self.master, text="Run Template Matching", command=self.run_template_matching)
#         self.run_button.pack(pady=10)

#     def create_folder_entry(self, label_text, variable):
#         label = tk.Label(self.master, text=label_text)
#         label.pack(pady=5)

#         entry_frame = tk.Frame(self.master)
#         entry_frame.pack(pady=5)

#         entry = tk.Entry(entry_frame, textvariable=variable, width=40)
#         entry.grid(row=0, column=0)

#         browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_folder(variable))
#         browse_button.grid(row=0, column=1)

#     def create_file_entry(self, label_text, variable):
#         label = tk.Label(self.master, text=label_text)
#         label.pack(pady=5)

#         entry_frame = tk.Frame(self.master)
#         entry_frame.pack(pady=5)

#         entry = tk.Entry(entry_frame, textvariable=variable, width=40)
#         entry.grid(row=0, column=0)

#         browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_file(variable))
#         browse_button.grid(row=0, column=1)

#     def browse_folder(self, variable):
#         folder_path = filedialog.askdirectory(title="Select Folder")
#         variable.set(folder_path)

#     def browse_file(self, variable):
#         file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])
#         variable.set(file_path)

#     def run_template_matching(self):
#         class1_folder = self.class1_folder.get()
#         class2_folder = self.class2_folder.get()
#         test_file = self.test_file.get()

#         class1_templates = load_templates(class1_folder)
#         class2_templates = load_templates(class2_folder)
#         test_signals = load_signals(test_file)

#         class1_average = np.mean(class1_templates, axis=0)
#         class2_average = np.mean(class2_templates, axis=0)

#         direct_correlation = DirectCorrelation()

#         for i, test_signal in enumerate(test_signals):
#             direct_correlation.input_signal_1 = Signal(class1_average, periodic=False)
#             direct_correlation.input_signal_2 = Signal(test_signal, periodic=False)
#             direct_correlation.run()

#             bigger_corr = max(direct_correlation.output_normalized_correlation)

#             if bigger_corr == direct_correlation.output_normalized_correlation[0]:
#                 movement = "Class 1: Down Movement"
#             else:
#                 movement = "Class 2: Up Movement"

#             print(f"Test signal {i + 1}: {movement} (Correlation: {bigger_corr})")


# def load_signals(file_path):
#     signals = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             signal_samples = [float(value) for value in line.strip().split()]
#             signals.append(signal_samples)
#     return signals

# def template_matching(template, signal):
#     signal_array = np.array(signal, dtype=np.float32).reshape(1, -1)
#     template_array = np.array(template, dtype=np.float32).reshape(1, -1)

#     result = cv2.matchTemplate(signal_array, template_array, cv2.TM_CCOEFF_NORMED)
#     return result[0][0]

# def classify_movement(test_signal, up_template, down_template):
#     up_score = template_matching(up_template, test_signal)
#     down_score = template_matching(down_template, test_signal)

#     if up_score > down_score:
#         return "Class 2: Up Movement"
#     else:
#         return "Class 1: Down Movement"

# def load_templates(folder_path):
#     templates = []
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith(".txt"):
#             file_path = os.path.join(folder_path, file_name)
#             with open(file_path, 'r') as file:
#                 template_samples = [float(line.strip()) for line in file]
#                 templates.append(template_samples)
#     return templates

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TemplateMatchingApp(root)
#     root.mainloop()

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

class Signal:
    def __init__(self, samples, periodic):
        self.samples = samples
        self.periodic = periodic

class TemplateMatchingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Template Matching App")

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

        browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_file(variable))
        browse_button.grid(row=0, column=1)

    def browse_folder(self, variable):
        folder_path = filedialog.askdirectory(title="Select Folder")
        variable.set(folder_path)

    def browse_file(self, variable):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])
        variable.set(file_path)

    def run_template_matching(self):
        class1_folder = self.class1_folder.get()
        class2_folder = self.class2_folder.get()
        test_file = self.test_file.get()

        class1_templates = load_templates(class1_folder)
        class2_templates = load_templates(class2_folder)
        test_signals = load_signals(test_file)

        class1_average = Signal(np.mean(class1_templates, axis=0), periodic=False)
        class2_average = Signal(np.mean(class2_templates, axis=0), periodic=False)

        corr_class1 = correlation(test_signals[0], class1_average)
        corr_class2 = correlation(test_signals[0], class2_average)

        bigger_corr = max(corr_class1, corr_class2)

        if bigger_corr == corr_class1:
            movement = "Class 1: Down Movement"
        else:
            movement = "Class 2: Up Movement"

        print(f"Test signal 1: {movement} (Correlation: {bigger_corr})")


def load_signals(file_path):
    signals = []
    with open(file_path, 'r') as file:
        for line in file:
            signal_samples = [float(value) for value in line.strip().split()]
            signals.append(signal_samples)
    return signals

# def template_matching(template, signal):
#     signal_array = np.array(signal, dtype=np.float32).reshape(1, -1)
#     template_array = np.array(template, dtype=np.float32).reshape(1, -1)

#     result = cv2.matchTemplate(signal_array, template_array, cv2.TM_CCOEFF_NORMED)
#     return result[0][0]

# def correlation(signal, template):
#     signal = np.array(signal.samples) if isinstance(signal, Signal) else np.array(signal)
#     template = np.array(template.samples) if isinstance(template, Signal) else np.array(template)

#     size = len(signal)
#     result = correlate(signal, template) / size

#     return result[0] if len(result) > 0 else 0.0

def correlation(signal, template):
    signal = np.array(signal.samples) if isinstance(signal, Signal) else np.array(signal)
    template = np.array(template.samples) if isinstance(template, Signal) else np.array(template)

    size = len(signal)
    raw_result = correlate(signal, template)

    return [val / size for val in raw_result] if len(raw_result) > 0 else [0.0]


def correlate(signal, template):
    signal = np.array(signal.samples) if isinstance(signal, Signal) else np.array(signal)
    template = np.array(template.samples) if isinstance(template, Signal) else np.array(template)

    size = len(signal)
    result = []

    for i in range(size):
        temp = 0
        for j in range(len(template)):
            if i + j < size:
                temp += signal[i + j] * template[j]

        result.append(temp)

    return result


def load_templates(folder_path):
    templates = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                template_samples = [float(line.strip()) for line in file]
                templates.append(template_samples)
    return templates




if __name__ == "__main__":
    root = tk.Tk()
    app = TemplateMatchingApp(root)
    root.mainloop()



# class TemplateMatchingApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Template Matching App")

#         self.class1_folder = tk.StringVar()
#         self.class2_folder = tk.StringVar()
#         self.test_file = tk.StringVar()

#         self.create_folder_entry("Class 1 Folder", self.class1_folder)
#         self.create_folder_entry("Class 2 Folder", self.class2_folder)
#         self.create_file_entry("Test File", self.test_file)

#         self.run_button = tk.Button(self.master, text="Run Template Matching", command=self.run_template_matching)
#         self.run_button.pack(pady=10)

#     def create_folder_entry(self, label_text, variable):
#         label = tk.Label(self.master, text=label_text)
#         label.pack(pady=5)

#         entry_frame = tk.Frame(self.master)
#         entry_frame.pack(pady=5)

#         entry = tk.Entry(entry_frame, textvariable=variable, width=40)
#         entry.grid(row=0, column=0)

#         browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_folder(variable))
#         browse_button.grid(row=0, column=1)

#     def create_file_entry(self, label_text, variable):
#         label = tk.Label(self.master, text=label_text)
#         label.pack(pady=5)

#         entry_frame = tk.Frame(self.master)
#         entry_frame.pack(pady=5)

#         entry = tk.Entry(entry_frame, textvariable=variable, width=40)
#         entry.grid(row=0, column=0)

#         browse_button = tk.Button(entry_frame, text="Browse", command=lambda: self.browse_file(variable))
#         browse_button.grid(row=0, column=1)

#     def browse_folder(self, variable):
#         folder_path = filedialog.askdirectory(title="Select Folder")
#         variable.set(folder_path)

#     def browse_file(self, variable):
#         file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])
#         variable.set(file_path)

#     def run_template_matching(self):
#         class1_folder = self.class1_folder.get()
#         class2_folder = self.class2_folder.get()
#         test_file = self.test_file.get()

#         class1_templates = load_templates(class1_folder)
#         class2_templates = load_templates(class2_folder)
#         test_signals = load_signals(test_file)

#         class1_average = np.mean(class1_templates, axis=0)
#         class2_average = np.mean(class2_templates, axis=0)

#         for i, test_signal in enumerate(test_signals):
#             class1_corr = template_matching(class1_average, test_signal)
#             class2_corr = template_matching(class2_average, test_signal)

#             up_score = template_matching(class2_templates[0], test_signal)
#             down_score = template_matching(class1_templates[0], test_signal)

#             if up_score > down_score:
#                 bigger_corr = class2_corr
#                 movement = "Class 2: Up Movement"
#             else:
#                 bigger_corr = class1_corr
#                 movement = "Class 1: Down Movement"

#             if class1_corr > bigger_corr:
#                 bigger_corr = class1_corr
#                 movement = "Class 1: Down Movement"

#             if class2_corr > bigger_corr:
#                 bigger_corr = class2_corr
#                 movement = "Class 2: Up Movement"

#             print(f"Test signal {i + 1}: {movement} (Correlation: {bigger_corr})")


# def load_signals(file_path):
#     signals = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             signal_samples = [float(value) for value in line.strip().split()]
#             signals.append(signal_samples)
#     return signals

# def template_matching(template, signal):
#     signal_array = np.array(signal, dtype=np.float32).reshape(1, -1)
#     template_array = np.array(template, dtype=np.float32).reshape(1, -1)

#     result = cv2.matchTemplate(signal_array, template_array, cv2.TM_CCOEFF_NORMED)
#     return result[0][0]

# def classify_movement(test_signal, up_template, down_template):
#     up_score = template_matching(up_template, test_signal)
#     down_score = template_matching(down_template, test_signal)

#     if up_score > down_score:
#         return "Class 2: Up Movement"
#     else:
#         return "Class 1: Down Movement"
    
# def load_templates(folder_path):
#     templates = []
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith(".txt"):
#             file_path = os.path.join(folder_path, file_name)
#             with open(file_path, 'r') as file:
#                 template_samples = [float(line.strip()) for line in file]
#                 templates.append(template_samples)
#     return templates

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TemplateMatchingApp(root)
#     root.mainloop()
