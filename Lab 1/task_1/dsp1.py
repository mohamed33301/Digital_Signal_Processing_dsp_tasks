import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        root.config(menu=menubar)
        
        # Create canvas for plotting
        self.fig, self.ax = plt.subplots(nrows=2, ncols=1, figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.load_button = tk.Button(root, text="Load Signal", command=self.load_signal)
        self.load_button.pack(side=tk.LEFT)
        self.plot_button = tk.Button(root, text="Plot", command=self.plot_signals)
        self.plot_button.pack(side=tk.LEFT)
        
        self.signals = []
  
    def load_signal(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                signal = np.loadtxt(file,skiprows=3,  usecols=[1])
            #skiprows=3,
                self.signals.append(signal)
    
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
        #amplitude= float(amplitude)
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
        
        analog_frequency_label = tk.Label(cosine_window, text="Analog Frequency (Hz):")
        analog_frequency_label.pack()
        analog_frequency_entry = tk.Entry(cosine_window)
        analog_frequency_entry.pack()
        
        sampling_frequency_label = tk.Label(cosine_window, text="Sampling Frequency (Hz):")
        sampling_frequency_label.pack()
        sampling_frequency_entry = tk.Entry(cosine_window)
        sampling_frequency_entry.pack()
        
        # Create a button to generate the cosine wave
        generate_button = tk.Button(cosine_window, text="Generate", command=lambda: self.generate_cosine_wave_signal(amplitude_entry.get(),phase_shift_entry.get(),
                                                                                                                analog_frequency_entry.get(),
                                                                                                                sampling_frequency_entry.get(),
                                                                                                                cosine_window))
    

        generate_button.pack()
       
    
    def generate_cosine_wave_signal(self, amplitude, phase_shift, analog_frequency, sampling_frequency, window):
        
        self.amplitude = int(amplitude)
        #amplitude = float(amplitude)
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




    def plot_signals(self):
       self.ax[0].clear()
       self.ax[1].clear()
    
       for i, signal in enumerate(self.signals):
          
          t = np.arange(0, len(signal))
          self.ax[0].plot(t, signal)
          
          #self.ax[1].stem(t, signal)  # Use stem plot for discrete signal    , use_line_collection=True
          #self.ax[1].scatter(t,signal )
          sampling_indices = np.arange(0, len(signal), int(len(signal)/10))  # Sample every 10th index
          self.ax[1].stem(sampling_indices, signal[sampling_indices],linefmt='C{}-'.format(i), markerfmt='C{}o'.format(i), basefmt='C{}-'.format(i))
                             
       self.ax[0].set_xlabel('Time')
       self.ax[0].set_ylabel('Amplitude')
       self.ax[0].set_title('Continuous Signal')
    
       self.ax[1].set_xlabel('Time')
       self.ax[1].set_ylabel('Amplitude')
       self.ax[1].set_title('Discrete Signal')

    #    if self.amplitude is not None:
    #     self.ax[1].set_xlim(-1 * self.amplitude, len(self.signals[0]))
    #    else:
    #     # Set a default x-axis limit if self.amplitude is None
    #     self.ax[1].set_xlim(0, len(self.signals[0]))
       #self.ax[1].set_xlim(-1*0.5, len(self.signals[0]) - 0.5)
    
       self.fig.tight_layout()
       self.canvas.draw()
       plt.show()
    


    
    
     

# Create the main window
root = tk.Tk()
app = SignalProcessingApp(root)
root.mainloop()






