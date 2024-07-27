import numpy as np
import tkinter as tk
from CompareSignal import Compare_Signals
from OldFunctions import conv



def ReadingFile(file_path):
    file = open(file_path, "r")
    signal_data = file.readlines()
    ignored_lines = signal_data[3:]
    x0, y0 = [], []
    for l in ignored_lines:
        row = l.split()
        x0.append(float(row[0]))
        y0.append(float(row[1]))
    return x0,y0

def SetSpecificationsFilters(FileName):
    global FilterType, FS, StopBandAttenuation, FC, F1, F2, TransitionBand
    FilterType = 0
    FS = 0
    StopBandAttenuation = 0
    FC = 0
    F1 = 0
    F2 = 0
    TransitionBand = 0
    
    file = open(FileName, "r", encoding='utf-8')
    lines1 = file.readlines()
    file.close()

    x = []
    y = 0

    ignored_lines = lines1[1:]
    for l in ignored_lines:
        row = l.split()
        x.append(float(row[2]))  # Convert to float

    for l in lines1:
        row = l.split()
        y = (row[2] + row[3])
        break

    if y == "Lowpass":
        FilterType = 1
    elif y == "Highpass":
        FilterType = 2
    elif y == "Bandpass":
        FilterType = 3
    elif y == "Bandstop":
        FilterType = 4

    if len(x) == 4:
        FS, StopBandAttenuation, FC, TransitionBand = x
    elif len(x) == 5:
        FS, StopBandAttenuation, F1, F2, TransitionBand = x
    return FilterType, FS, StopBandAttenuation, FC, F1, F2, TransitionBand


def CheckNOddOrEven(N):
    if(np.fmod(N,2) == 1 ):
        return int(N)
    elif(np.fmod(N,2)  == 0 or (np.fmod(N,2) ) < 1) :
        return int(N)+1
    elif((np.fmod(N,2) ) > 1 ):
        return int(N)+2
def CalculateFC_new(Type ,TransitionBand,FS,Fc= None,FC1 = None , FC2 = None ):
    if(Type == 1):
    # type = 1 (Low Pass Filter) 
        FC_Low_New =( Fc + (TransitionBand/2))/FS
        return FC_Low_New
    elif(Type == 2):
    # type = 2 (High Pass Filter) 
        FC_High_New =( Fc - (TransitionBand/2))/FS
        return FC_High_New
    elif(Type == 3):
    # type = 3 (Band Pass Pass Filter) 
        FC1_New =( FC1 - (TransitionBand/2))/FS
        FC2_New =( FC2 + (TransitionBand/2))/FS
        return FC1_New,FC2_New
    elif(Type == 4):
    # type = 4 (Band Stop Pass Filter) 
        FC1_New = (FC1 + (TransitionBand/2))/FS
        FC2_New = (FC2 - (TransitionBand/2))/FS
        return FC1_New,FC2_New
def No (StopBandAttenuation,TransitionBand,FS):
    if(StopBandAttenuation <= 21):
        N = 0.9 *FS / TransitionBand
    elif(StopBandAttenuation > 21 and StopBandAttenuation <= 44):
        N = 3.1 *FS / TransitionBand
    elif(StopBandAttenuation > 44 and StopBandAttenuation <= 53):
        N = 3.3 *FS / TransitionBand
    elif(StopBandAttenuation > 53 and StopBandAttenuation <= 74):
        N = 5.5 *FS / TransitionBand
    N_new =CheckNOddOrEven(N)
    return N_new
def Wn (StopBandAttenuation,N,n):
    
    if(StopBandAttenuation <= 21):
        return 1
    elif(StopBandAttenuation > 21 and StopBandAttenuation <= 44):
        eq = 0.5 + 0.5 * np.cos((2*np.pi*n)/N)
        return eq
    elif(StopBandAttenuation > 44 and StopBandAttenuation <= 53):
        eq = 0.54 + 0.46 * np.cos((2*np.pi*n)/N)
        return eq
    elif(StopBandAttenuation > 53 and StopBandAttenuation <= 74):
        eq = 0.42 + 0.5 * np.cos((2*np.pi*n)/(N-1))+ 0.08 * np.cos((4*np.pi*n)/(N-1))
        return eq
    
def CalculateWindowFunction(StopBandAttenuation,TransitionBand,FS,Index):
    N = No(StopBandAttenuation,TransitionBand,FS)
    n = - int(N/2)
    wn = []
    for i in range(N):
        wn.append(Wn(StopBandAttenuation,N,n))
        Index.append(n)
        n = n + 1
    return wn
def Hn (FilterType,n,TransitionBand,FS,FC,F1,F2):
    
    if(FilterType == 1):
        if(n == 0):
            eq = 2 * CalculateFC_new(FilterType ,TransitionBand,FS,Fc= FC)
            return eq
        else :
            f = CalculateFC_new(FilterType ,TransitionBand,FS,Fc= FC)
            eq = 2 *f *np.sin(n*2*np.pi*f)/(n * 2*np.pi *f)
            return eq

    elif(FilterType == 2):
        if(n == 0):
            eq =1- 2 * CalculateFC_new(FilterType ,TransitionBand,FS,Fc= FC)
            return eq
        else :
            f = CalculateFC_new(FilterType ,TransitionBand,FS,Fc= FC)
            eq =- 2 *f *np.sin(n*2*np.pi*f)/(n * 2*np.pi *f)
            return eq
    elif(FilterType == 3):
        if(n == 0):
            f1,f2 = CalculateFC_new(FilterType ,TransitionBand,FS,FC1=F1,FC2=F2)
            eq = 2 * (f2-f1)
            return eq
        else :
            f1,f2 = CalculateFC_new(FilterType ,TransitionBand,FS,FC1=F1,FC2=F2)
            eq = (2 *f2 *np.sin(n*2*np.pi*f2)/(n * 2*np.pi *f2))-(2 *f1 *np.sin(n*2*np.pi*f1)/(n * 2*np.pi *f1))
            return eq
    elif(FilterType == 4):
        if(n == 0):
            f1,f2 = CalculateFC_new(FilterType ,TransitionBand,FS,FC1=F1,FC2=F2)
            eq = 1 - 2 * (f2-f1)
            return eq
        else :
            f1,f2 = CalculateFC_new(FilterType ,TransitionBand,FS,FC1=F1,FC2=F2)
            eq = (2 *f1 *np.sin(n*2*np.pi*f1)/(n * 2*np.pi *f1))-(2 *f2 *np.sin(n*2*np.pi*f2)/(n * 2*np.pi *f2))
            return eq
    
def CalculateFilter(FilterType,StopBandAttenuation,TransitionBand,FS,FC,F1,F2):
    N = No(StopBandAttenuation,TransitionBand,FS)
    n = -int(N/2)
    hn = []
    for i in range(N):
        hn.append(Hn(FilterType,n,TransitionBand,FS,FC,F1,F2))
        n = n + 1
    return hn

def FIR(FilterType,StopBandAttenuation,TransitionBand,FS,FC,F1,F2):
    Index = []
    wn = CalculateWindowFunction(StopBandAttenuation,TransitionBand,FS,Index)
    hn = CalculateFilter(FilterType,StopBandAttenuation,TransitionBand,FS,FC,F1,F2)
    h = []
    N = No(StopBandAttenuation,TransitionBand,FS)
    for i in range(N):
        h.append(wn[i]*hn[i])
    return h , Index

def Testcases():
 TestCase_no = int(input("Please enter a number of TestCase_number from 1 to 8: "))

 if TestCase_no==1 :
    # TestCase1
    SetSpecificationsFilters("FIR test cases\Testcase 1\Filter Specifications.txt")
    LowPass , Index = FIR(FilterType, StopBandAttenuation,TransitionBand,FS,FC,F1,F2)
    Compare_Signals("FIR test cases\Testcase 1\LPFCoefficients.txt",Index,LowPass)
 elif TestCase_no==2:

    # TestCase2
    SetSpecificationsFilters("FIR test cases\Testcase 2\Filter Specifications.txt")
    LowPass0, Index0 = FIR(FilterType, StopBandAttenuation, TransitionBand, FS, FC, F1, F2)
    x0 , y0 = ReadingFile("FIR test cases\Testcase 2\ecg400.txt")
    output = conv(x0, y0, Index0, LowPass0)
    outputx, outputy = output
    Compare_Signals("FIR test cases\Testcase 2\ecg_low_pass_filtered.txt",outputx,outputy)
 elif TestCase_no==3:
    # TestCase3 
    SetSpecificationsFilters("FIR test cases\Testcase 3\Filter Specifications.txt")
    HighPass , Index= FIR(FilterType, StopBandAttenuation,TransitionBand,FS,FC,F1,F2)
    Compare_Signals("FIR test cases\Testcase 3\HPFCoefficients.txt",Index,HighPass)
 elif TestCase_no==4:
    # TestCase4
    SetSpecificationsFilters("FIR test cases\Testcase 4\Filter Specifications.txt")
    HighPass, Index0 = FIR(FilterType, StopBandAttenuation, TransitionBand, FS, FC, F1, F2)
    x0 , y0 = ReadingFile("FIR test cases\Testcase 4\ecg400.txt")
    output = conv(x0, y0, Index0, HighPass)
    outputx, outputy = output
    Compare_Signals("FIR test cases\Testcase 4\ecg_high_pass_filtered.txt",outputx,outputy)
 elif TestCase_no==5:
    # TestCase5
    SetSpecificationsFilters("FIR test cases\Testcase 5\Filter Specifications.txt")
    BandPass , Index= FIR(FilterType, StopBandAttenuation,TransitionBand,FS,FC,F1,F2)
    Compare_Signals("FIR test cases\Testcase 5\BPFCoefficients.txt",Index,BandPass)
 elif TestCase_no==6:
    # TestCase6
    SetSpecificationsFilters("FIR test cases\Testcase 6\Filter Specifications.txt")
    BandPass, Index0 = FIR(FilterType, StopBandAttenuation, TransitionBand, FS, FC, F1, F2)
    x0 , y0 = ReadingFile("FIR test cases\Testcase 6\ecg400.txt")
    output = conv(x0, y0, Index0, BandPass)
    outputx, outputy = output
    Compare_Signals("FIR test cases\Testcase 6\ecg_band_pass_filtered.txt",outputx,outputy)
 elif TestCase_no==7:
    # TestCase7
    SetSpecificationsFilters("FIR test cases\Testcase 7\Filter Specifications.txt")
    BandStop , Index= FIR(FilterType, StopBandAttenuation,TransitionBand,FS,FC,F1,F2)
    Compare_Signals("FIR test cases\Testcase 7\BSFCoefficients.txt",Index,BandStop)
 elif TestCase_no==8:
    # TestCase8
    SetSpecificationsFilters("FIR test cases\Testcase 8\Filter Specifications.txt")
    BandStop, Index0 = FIR(FilterType, StopBandAttenuation, TransitionBand, FS, FC, F1, F2)
    x0 , y0 = ReadingFile("FIR test cases\Testcase 8\ecg400.txt")
    output = conv(x0, y0, Index0, BandStop)
    outputx, outputy = output
    Compare_Signals("FIR test cases\Testcase 8\ecg_band_stop_filtered.txt",outputx,outputy)

Testcases()
 