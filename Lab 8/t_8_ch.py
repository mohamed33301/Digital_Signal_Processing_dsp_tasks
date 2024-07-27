import numpy as np
#from scipy.signal import convolve
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import filedialog
from tkinter import ttk, filedialog, messagebox
import math
import task_6

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

class Signal:
    def __init__(self, samples, samples_indices, is_discrete):
        self.Samples = samples
        self.SamplesIndices = samples_indices
        self.IsDiscrete = is_discrete

class FILTER_TYPES:
    LOW = "LOW"
    HIGH = "HIGH"
    BAND_PASS = "BAND_PASS"
    BAND_STOP = "BAND_STOP"

class FIR:
    def __init__(self):
       
        self.InputTimeDomainSignal = None
        self.InputFilterType = None
        self.InputFS = None
        self.InputCutOffFrequency = None
        self.InputF1 = None
        self.InputF2 = None
        self.InputStopBandAttenuation = None
        self.InputTransitionBand = None
        # self.OutputHn = None
        # self.OutputYn = None
        self.OutputHn = Signal([], [], False)
        self.OutputYn = Signal([], [], False)

    def run(self):
        
        self.OutputHn = Signal([], [], False)
        self.OutputYn = Signal([], [], False)

        
        try:
            numberOfCoefficients = 0
            equation = ""

            if self.InputStopBandAttenuation <= 21:
                equation = "1000"
                numberOfCoefficients = 0.9 / (self.InputTransitionBand / self.InputFS)
                numberOfCoefficients = self.num_of_coefficients(numberOfCoefficients)
            elif self.InputStopBandAttenuation <= 44:
                equation = "0100"
                numberOfCoefficients = 3.1 / (self.InputTransitionBand / self.InputFS)
                numberOfCoefficients = self.num_of_coefficients(numberOfCoefficients)
            elif self.InputStopBandAttenuation <= 53:
                equation = "0010"
                numberOfCoefficients = 3.3 / (self.InputTransitionBand / self.InputFS)
                numberOfCoefficients = self.num_of_coefficients(numberOfCoefficients)
            elif self.InputStopBandAttenuation <= 74:
                equation = "0001"
                numberOfCoefficients = 5.5 / (self.InputTransitionBand / self.InputFS)
                numberOfCoefficients = self.num_of_coefficients(numberOfCoefficients)

            lower_boundary = int(-math.floor(numberOfCoefficients / 2))
            upper_boundary = int(math.floor(numberOfCoefficients / 2))
            finalCutOffFrequency, finalCutOffFrequency2 = 0, 0
            coefficients = []

            if self.InputFilterType == FILTER_TYPES.LOW:
                finalCutOffFrequency = (self.InputCutOffFrequency + (self.InputTransitionBand / 2)) / self.InputFS
                if equation == "0001":
                    coefficients =self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.blackman, self.lowpass)
                elif equation == "0010":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.hamming, self.lowpass)
                elif equation == "0100":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.hanning, self.lowpass)
                elif equation == "1000":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.rectangular, self.lowpass)
            elif self.InputFilterType == FILTER_TYPES.HIGH:
                finalCutOffFrequency = (self.InputCutOffFrequency + (self.InputTransitionBand / 2)) / self.InputFS
                if equation == "0001":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.blackman, self.highpass)
                elif equation == "0010":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.hamming, self.highpass)
                elif equation == "0100":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.hanning, self.highpass)
                elif equation == "1000":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, 0, self.rectangular, self.highpass)
            elif self.InputFilterType == FILTER_TYPES.BAND_PASS:
                finalCutOffFrequency = (self.InputF1 - (self.InputTransitionBand / 2)) / self.InputFS
                finalCutOffFrequency2 = (self.InputF2 + (self.InputTransitionBand / 2)) / self.InputFS
                if equation == "0001":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.blackman, self.bandpass)
                elif equation == "0010":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.hamming, self.bandpass)
                elif equation == "0100":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.hanning, self.bandpass)
                elif equation == "1000":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.rectangular, self.bandpass)
            elif self.InputFilterType == FILTER_TYPES.BAND_STOP:
                finalCutOffFrequency = (self.InputF1 - (self.InputTransitionBand / 2)) / self.InputFS
                finalCutOffFrequency2 = (self.InputF2 + (self.InputTransitionBand / 2)) / self.InputFS
                if equation == "0001":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.blackman, self.bandreject)
                elif equation == "0010":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.hamming, self.bandreject)
                elif equation == "0100":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.hanning, self.bandreject)
                elif equation == "1000":
                    self.calculate_coefficients(lower_boundary, upper_boundary, int(numberOfCoefficients), finalCutOffFrequency, finalCutOffFrequency2, self.rectangular, self.bandreject)

            # Assuming DirectConvolution, blackman, lowpass, etc. functions are defined elsewhere
            dc = DirectConvolution()
            dc.InputSignal1 = self.InputTimeDomainSignal
            dc.InputSignal2 = self.OutputHn
            dc.run()
            self.OutputYn = dc.OutputConvolvedSignal
            print(self.OutputYn)

            # # Display the results in a formatted way
            # result_text = ""
            # if self.OutputYn is not None and self.OutputYn.SamplesIndices:
            #     for index, value in zip(self.OutputYn.SamplesIndices, self.OutputYn.Samples):
            #         result_text += f"{index} {value}\n"
            # else:
            #     result_text = "No results to display."
            # return result_text
                    
            # # After the coefficients are computed
            # coefficients_window = tk.Toplevel()
            # coefficients_window.title("Computed Coefficients")

            # coefficients_text = tk.Text(coefficients_window, height=10, width=50)
            # coefficients_text.pack()

            # # Insert the computed coefficients into the text widget
            # for coef in coefficients:
            #     coefficients_text.insert(tk.END, f"{coef}\n")

                

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def rectangular(self, n, N):
        return 1.0

    def hanning(self, n, N):
        result = 0.5 + 0.5 * math.cos(2 * math.pi * n / N)
        return result

    def hamming(self,n, N):
        result = 0.54 + 0.46 * math.cos(2 * math.pi * n / N)
        return result


    def blackman(self, n, N):
        result = 0.42 + 0.5 * math.cos(2 * math.pi * n / (N - 1)) + 0.08 * math.cos(4 * math.pi * n / (N - 1))
        return result

    def lowpass(self, n, cutoff_frequency, zero):
        if n != 0:
            return 2 * cutoff_frequency * ((math.sin(n * 2 * math.pi * cutoff_frequency)) / (n * 2 * math.pi * cutoff_frequency))
        else:
            return 2 * cutoff_frequency

    def highpass(self, n, cutoff_frequency, zero):
        if n != 0:
            return -1 * 2 * cutoff_frequency * ((math.sin(n * 2 * math.pi * cutoff_frequency)) / (n * 2 * math.pi * cutoff_frequency))
        else:
            return 1 - (2 * cutoff_frequency)

    def bandpass(self, n, cutoff_frequency1, cutoff_frequency2):
        if n != 0:
            res1 = 2 * cutoff_frequency1 * ((math.sin(n * 2 * math.pi * cutoff_frequency1)) / (n * 2 * math.pi * cutoff_frequency1))
            res2 = 2 * cutoff_frequency2 * ((math.sin(n * 2 * math.pi * cutoff_frequency2)) / (n * 2 * math.pi * cutoff_frequency2))
            return res2 - res1
        else:
            return 2 * (cutoff_frequency2 - cutoff_frequency1)

    def bandreject(self, n, cutoff_frequency1, cutoff_frequency2):
        if n != 0:
            res1 = 2 * cutoff_frequency1 * ((math.sin(n * 2 * math.pi * cutoff_frequency1)) / (n * 2 * math.pi * cutoff_frequency1))
            res2 = 2 * cutoff_frequency2 * ((math.sin(n * 2 * math.pi * cutoff_frequency2)) / (n * 2 * math.pi * cutoff_frequency2))
            return res1 - res2
        else:
            return 1 - (2 * (cutoff_frequency2 - cutoff_frequency1))

    def num_of_coefficients(self, N):
        final_num = int(math.ceil(N))
        if final_num % 2 == 0:
            final_num += 1
        return final_num

        try:
            # Additional inputs for FIR filter
            normalized_cutoff_frequency = self.InputCutOffFrequency / self.InputFS
            normalized_transition_band = self.InputTransitionBand / self.InputFS
            half_transition_band = normalized_transition_band / 2

            # Adjust frequencies using half transition band
            if self.InputFilterType in [FILTER_TYPES.LOW, FILTER_TYPES.HIGH]:
                finalCutOffFrequency = (normalized_cutoff_frequency + half_transition_band)

            elif self.InputFilterType in [FILTER_TYPES.BAND_PASS, FILTER_TYPES.BAND_STOP]:
                finalCutOffFrequency = (self.InputF1 - half_transition_band)
                finalCutOffFrequency2 = (self.InputF2 + half_transition_band)
            # Compute coefficients
            coefficients = self.calculate_coefficients(finalCutOffFrequency, finalCutOffFrequency2)
            # Convolve the input signal with the computed coefficients
            convolved_signal = np.convolve(self.InputTimeDomainSignal.values, coefficients, mode='same')
            # Draw the resulted signal (assuming a plotting function exists)


            #plot_signal(self.InputTimeDomainSignal.indices, convolved_signal)
            # Save the coefficients to a text file
            self.save_coefficients_to_file(coefficients)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # def calculate_coefficients(self, small_index, large_index, coefficients, FC1, FC2, window, filter):
    #     # Modify the following part to return the computed coefficients
    #     coefficients = []
    #     for i in range(small_index, large_index + 1):
    #         self.OutputHn.SamplesIndices.append(i)
    #         w = window(i, N)
    #         h = filter(i, FC1, FC2)
    #         coef = h * w
    #         self.OutputHn.Samples.append(coef)

    def calculate_coefficients(self, small_index, large_index, coefficients, FC1, FC2, window, filter):
        computed_coefficients = []
        for i in range(small_index, large_index + 1):
            self.OutputHn.SamplesIndices.append(i)
            w = window(i, coefficients)
            h = filter(i, FC1, FC2)
            coef = h * w
            self.OutputHn.Samples.append(coef)
            computed_coefficients.append(coef)
        return computed_coefficients
    
    def save_coefficients_to_file(self, coefficients):
            with open("coefficients.txt", "w") as file:
                for coef in coefficients:
                    file.write(f"{coef}\n")

# Assuming DirectConvolution is defined elsewhere
class DirectConvolution:
    def __init__(self):
        self.InputSignal1 = None
        self.InputSignal2 = None
        self.OutputConvolvedSignal = None

    def run(self):
        task_6.MovingAverageGUI.s_convolution_operation(self)

class FIRGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("FIR Filter GUI")
        self.fir_filter = FIR()
        # GUI Components  fir_filter
        self.signal_frame_1 = self.create_signal_frame("Signal 1")

        self.filter_label = tk.Label(self, text="Select Filter Type:")
        self.filter_label.pack()

        self.filter_var = tk.StringVar()
        self.filter_var.set("LOW")
        self.filter_menu = tk.OptionMenu(self, self.filter_var, "LOW", "HIGH", "BAND_PASS", "BAND_STOP")
        self.filter_menu.pack()

        self.fs_label = tk.Label(self, text="Enter Sampling Frequency:")
        self.fs_label.pack()

        self.fs_entry = tk.Entry(self)
        self.fs_entry.pack()

        self.stop_band_attenuation_label = tk.Label(self, text="Enter Stop Band Attenuation:")
        self.stop_band_attenuation_label.pack()

        self.stop_band_attenuation_entry = tk.Entry(self)
        self.stop_band_attenuation_entry.pack()

        self.cutoff_label = tk.Label(self, text="Enter Cutoff Frequency:")
        self.cutoff_label.pack()

        self.cutoff_entry = tk.Entry(self)
        self.cutoff_entry.pack()

        self.transition_label = tk.Label(self, text="Enter Transition Band:")
        self.transition_label.pack()

        self.transition_entry = tk.Entry(self)
        self.transition_entry.pack()

        self.run_button = tk.Button(self, text="Run Filter", command=self.run_filter)
        self.run_button.pack()

        

            # task sampling 

        self.results_label = tk.Label(self, text="Results:")
        self.results_label.pack()

        self.results_text = tk.Text(self, height=10, width=50)
        self.results_text.pack()                                                                  

    def browse_file(self, signal_label):
        file_path = filedialog.askopenfilename(title=f"Select {signal_label} File", filetypes=[("Text Files", "*.txt")])
        self.load_file(signal_label, file_path)

    def load_file(self, signal_label, file_path):
        if file_path:
            with open(file_path, 'r') as file:
                for _ in range(3):
                    next(file)

                signal_samples = []
                indices = []  # Add this line to define indices
                for line in file:
                    values = line.strip().split()
                    indices.append(int(values[0]))  # Assuming the first value in each line is the index
                    signal_samples.append(float(values[1]))  # Assuming the second value in each line is the sample

            if signal_label == "Signal 1":
                self.signal_frame_1['samples'] = signal_samples
                self.signal_frame_1['indices'] = indices
    def create_signal_frame(self, signal_label):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10, side=tk.LEFT)

        label = tk.Label(frame, text=signal_label)
        label.grid(row=0, column=0, columnspan=2, pady=5)

        browse_button = tk.Button(frame, text="Browse", command=lambda: self.browse_file(signal_label))
        browse_button.grid(row=1, column=0, pady=5)

        return {'frame': frame, 'samples': []}
    # def run_filter(self):
    #     try:
    #         # Get inputs from the GUI
    #         filter_type = self.filter_var.get()
    #         cutoff_frequency = float(self.cutoff_entry.get())
    #         fs = float(self.fs_entry.get())
    #         transition_band = float(self.transition_entry.get())
    #         stop_band_attenuation = float(self.stop_band_attenuation_entry.get())

    #         # Set a default value for InputStopBandAttenuation
    #         if stop_band_attenuation is None:
    #             stop_band_attenuation = 0  # Set your default value here

    #         # Additional inputs for BAND_PASS and BAND_STOP
    #         f1, f2 = 0, 0
    #         if filter_type in [FILTER_TYPES.BAND_PASS, FILTER_TYPES.BAND_STOP]:
    #             f1 = askfloat("Input", "Enter F1 for Band Pass/Stop Filter:")
    #             f2 = askfloat("Input", "Enter F2 for Band Pass/Stop Filter:")
    #         # Set inputs for FIR filter
    #         self.fir_filter.InputFilterType = filter_type
    #         self.fir_filter.InputFS = fs
    #         self.fir_filter.InputCutOffFrequency = cutoff_frequency
    #         self.fir_filter.InputF1 = f1
    #         self.fir_filter.InputF2 = f2
    #         self.fir_filter.InputTransitionBand = transition_band
    #         self.fir_filter.InputStopBandAttenuation = stop_band_attenuation  # Set the stop band attenuation

    #         # Run the FIR filter
    #         result_text = self.fir_filter.run()

    #         # Display results in a new window
    #         result_window = tk.Toplevel(self)
    #         result_window.title("Filtered Signal")

    #         results_text = tk.Text(result_window, height=10, width=50)
    #         results_text.pack()

    #         results_text.insert(tk.END, result_text)  # Insert the formatted result text

    #     except ValueError:
    #         messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")


    def run_filter(self):
        try:
            # Get inputs from the GUI
            filter_type = self.filter_var.get()
            cutoff_frequency = float(self.cutoff_entry.get())
            fs = float(self.fs_entry.get())
            transition_band = float(self.transition_entry.get())
            stop_band_attenuation = float(self.stop_band_attenuation_entry.get())

            # Set a default value for InputStopBandAttenuation
            if stop_band_attenuation is None:
                stop_band_attenuation = 0  # Set your default value here

            # Additional inputs for BAND_PASS and BAND_STOP
            f1, f2 = 0, 0
            if filter_type in [FILTER_TYPES.BAND_PASS, FILTER_TYPES.BAND_STOP]:
                f1 = askfloat("Input", "Enter F1 for Band Pass/Stop Filter:")
                f2 = askfloat("Input", "Enter F2 for Band Pass/Stop Filter:")

            # Set inputs for FIR filter
            self.fir_filter.InputFilterType = filter_type
            self.fir_filter.InputFS = fs
            self.fir_filter.InputCutOffFrequency = cutoff_frequency
            self.fir_filter.InputF1 = f1
            self.fir_filter.InputF2 = f2
            self.fir_filter.InputTransitionBand = transition_band
            self.fir_filter.InputStopBandAttenuation = stop_band_attenuation  # Set the stop band attenuation

            # Run the FIR filter
            self.fir_filter.run()

            # Display results in a new window
            result_window = tk.Toplevel(self)
            result_window.title("Filtered Signal")

            results_text = tk.Text(result_window, height=10, width=50)
            results_text.pack()

            results = "Filtered Signal:\n"
            for index, value in zip(self.fir_filter.OutputYn.SamplesIndices, self.fir_filter.OutputYn.Samples):
                results += f"{index} {value}\n"

            results_text.insert(tk.END, results)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")


if __name__ == "__main__":
    app = FIRGUI()
    app.mainloop()
