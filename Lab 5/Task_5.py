import math
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import comparesignal2


class DCTApp:
    def __init__(self, master):
        self.master = master
        master.title("DCT Coefficients Viewer")

        self.file_path = None
        self.m = None  # Variable to store the value of m
        self.input_signal = None  # Instance variable to store input_signal

        self.choose_file_button = ttk.Button(master, text="Choose Input File_DCT", command=self.choose_file)
        self.choose_file_button.pack()

        self.process_button = ttk.Button(master, text="Process Signal", command=self.process_signal_button_click)
        self.process_button.pack()

        self.choose_file_button = ttk.Button(master, text="Choose Input File_DC", command=self.choose_file)
        self.choose_file_button.pack()

        self.process_button = ttk.Button(master, text="Process Signal", command=self.process_signal_button_click_2)
        self.process_button.pack()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    def process_signal_button_click(self):
        if self.file_path:
            with open(self.file_path, "r") as file:
                input_lines = file.read().strip().split('\n')

            num_values = int(input_lines[2])  # Extracting the number of values from the third line

            # Process the remaining lines starting from the fourth line
            self.input_signal = [0.0] * num_values
            for line in input_lines[3:]:
                index, value = map(float, line.split())
                self.input_signal[int(index)] = value

            dct_coefficients = self.compute_dct(self.input_signal)

            output_window = tk.Toplevel(self.master)
            output_window.title("DCT Coefficients Result")

            table_label = tk.Label(output_window, text="DCT Coefficients:")
            table_label.pack()

            # Creating a treeview
            table = ttk.Treeview(output_window, columns=("Index", "Coefficient"))
            table.heading("#0", text="Index")
            table.heading("#1", text="Coefficient")

            for i, coefficient in enumerate(dct_coefficients):
                table.insert("", i, values=(i, coefficient))
            #print(comparesignal2.SignalSamplesAreEqual("D:\\Downloads\\dsp_tasks_2023\\lab 5\\Task files-20231118T091116Z-001\\Task files\\DCT\\DCT_output.txt","D:\\Downloads\\dsp_tasks_2023\\lab 5\\Task files-20231118T091116Z-001\\Task files\DCT\\al.txt"))

            table.pack()

            save_button = ttk.Button(output_window, text="Save Coefficients", command=self.get_m_and_save_coefficients)
            save_button.pack()

    def compute_dct(self, input_signal):
        N = len(input_signal)
        dct_coefficients = []

        for k in range(N):
            ck = 0
            for n in range(N):
                ck += input_signal[n] * math.cos((math.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))
            dct_coefficients.append(np.sqrt(2 / N) * ck)

        return dct_coefficients

    def get_m_and_save_coefficients(self):
        self.m = simpledialog.askinteger("Input", "Enter the number of coefficients to save:", parent=self.master)
        if self.m is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, "w") as file:
                    # Add the specified values to the file
                    file.write("0\n1\n6\n")  # Values 0, 1, 6 in three separate lines

                    dct_coefficients = self.compute_dct(self.input_signal)[:self.m]
                    for i, coefficient in enumerate(dct_coefficients):
                        file.write(f"{i}  {coefficient}\n")

    def process_signal_button_click_2(self):
        if self.file_path:
            with open(self.file_path, "r") as file:
                input_lines = file.read().strip().split('\n')

            num_values = int(input_lines[2])  # Extracting the number of values from the third line

            # Process the remaining lines starting from the fourth line
            self.input_signal = [0.0] * num_values
            for line in input_lines[3:]:
                index, value = map(float, line.split())
                self.input_signal[int(index)] = value
        
            dc_result = self.DC_Component(self.input_signal)

            output_window = tk.Toplevel(self.master)
            output_window.title("DC Result")

            table_label = tk.Label(output_window, text="DC Result:")
            table_label.pack()

            # Creating a treeview
            table = ttk.Treeview(output_window, columns=("Index", "Value"))
            table.heading("#0", text="Index")
            table.heading("#1", text="Value")

            for i, value in enumerate(dc_result):
                table.insert("", i, values=(i, value))

            table.pack()


    def DC_Component(self, input_signal):
        output_signal = []
        signal_sum = sum(input_signal)
        mean = signal_sum / len(input_signal)

        for sample in input_signal:
            output_signal.append(sample - mean)

        return output_signal


if __name__ == "__main__":
    root = tk.Tk()
    app = DCTApp(root)
    root.mainloop()



