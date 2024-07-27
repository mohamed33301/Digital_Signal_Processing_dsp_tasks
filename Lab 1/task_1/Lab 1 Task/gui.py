from tkinter.simpledialog import askinteger
import dsp
import comparesignals
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import *


def _run():
    a = int(amplitudeValue.get())
    phase_shift = float(phaseShiftValue.get())
    analog_frequency = int(analogFrequencyValue.get())
    sampling_frequency = int(samplingFrequencyValue.get())
    while sampling_frequency < 2 * analog_frequency:
        messagebox.showinfo("Response", f"The sampling frequency must be greater than {2 * analog_frequency}.")
        sampling_frequency = askinteger("Input", "Enter a new value for sampling frequency:")
        if sampling_frequency is not None:
            samplingFrequencyValue.delete(0, tk.END)
            samplingFrequencyValue.insert(0, str(sampling_frequency))
        else:
            break

    if Cosine.get() == 1:
        x = dsp.cos_signal(a, phase_shift, analog_frequency, sampling_frequency)
    else:
        x = dsp.sin_signal(a, phase_shift, analog_frequency, sampling_frequency)
    dsp.display_continuous(x)

def open_new_page():
    new_page = tk.Toplevel(top)
    new_page.title("Signals")

    FilePath = Label(new_page, text="Enter  Signal File path :")
    FilePath.place(x=350, y=150)
    FilePath.pack()

    filePathValue = Entry(new_page, width=30)
    filePathValue.place(x=350, y=170)
    filePathValue.pack()


    def display_signals():
        s1 = filePathValue.get()
        ss1 = dsp.read_signal(s1)
        dis_c = tk.Button(new_page, text="Display_continuous", command=lambda: dsp.display_continuous(ss1))
        dis_c.pack()
        dis_d = tk.Button(new_page, text="Display_discrete", command=lambda: dsp.display_disc(ss1))
        dis_d.pack()

    display_button = Button(new_page, text="Display Signals", command=display_signals)
    display_button.pack()

    new_page_button = tk.Button(new_page, text="Close", command=new_page.destroy)
    new_page_button.pack()





top = tk.Tk()
top.title("Lab1 Task DSP")


input_frame = tk.Frame(top)
input_frame.pack(pady=10)


Amplitude = tk.Label(input_frame, text="Amplitude:")
Amplitude.grid(row=0, column=0)
amplitudeValue = tk.Entry(input_frame, width=30)
amplitudeValue.grid(row=0, column=1)


PhaseShift = tk.Label(input_frame, text="Phase shift:")
PhaseShift.grid(row=1, column=0)
phaseShiftValue = tk.Entry(input_frame, width=30)
phaseShiftValue.grid(row=1, column=1)


AnalogFrequency = tk.Label(input_frame, text="Analog frequency:")
AnalogFrequency.grid(row=2, column=0)
analogFrequencyValue = tk.Entry(input_frame, width=30)
analogFrequencyValue.grid(row=2, column=1)


SamplingFrequency = tk.Label(input_frame, text="Sampling frequency:")
SamplingFrequency.grid(row=3, column=0)
samplingFrequencyValue = tk.Entry(input_frame, width=30)
samplingFrequencyValue.grid(row=3, column=1)


Cosine = tk.BooleanVar()
Sine = tk.BooleanVar()
sin_cos_frame = tk.Frame(top)
sin_cos_frame.pack()
sin_cos_label = tk.Label(sin_cos_frame, text="Select a waveform:")
sin_cos_label.pack()
selected_waveform = tk.StringVar()
cosine_radio = tk.Radiobutton(sin_cos_frame, text="Cosine", variable=selected_waveform, value="cosine")
sine_radio = tk.Radiobutton(sin_cos_frame, text="Sine", variable=selected_waveform, value="sine")
selected_waveform.set("cosine")
cosine_radio.pack()
sine_radio.pack()



run_button = tk.Button(top, text="Run", command=_run)
run_button.pack()


open_new_page_button = tk.Button(top, text="Read and display another two signals", command=open_new_page)
open_new_page_button.pack()


exit_button = tk.Button(top, text="Exit", command=top.destroy)
exit_button.pack()

top.mainloop()
