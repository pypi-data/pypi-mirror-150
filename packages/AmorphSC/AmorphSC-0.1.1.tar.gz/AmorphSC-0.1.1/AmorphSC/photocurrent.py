import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def calculate_PC(data, gain, change_positions):
    """
    Function that given input data returns the photocurrent spectra calculated
    with each 

    Parameters
    ----------
    data : 
        input data of photocurrent
    gain : float
        vector with gains used
    change_positions : float
        vector with positions at which the gain has been changed

    Returns
    -------
    Amp: float
        calculated amplitude photocurrent

    """
    
    Amp = []#vector of amplitudes
    sens = data.s[0] #sensitivity 
    p = 0 # counter for initial position
    for i, j in enumerate(change_positions):
        amp = data.Amp[p:j+1] #take that part of spectrum
        amp = amp*sens*1e-4 /gain[i] #adjust with gain and sens
        p = j+1
        Amp = np.concatenate((Amp, amp))
    return Amp

def lamp_spec(data, gain, change, diode_area):
    """
    Function that takes into account a set of lamp data and returns the adjustment
    of the set with the sensitivity of photodiode

    Parameters
    ----------
    data : fdataframe
        dataframe recorded by the instrument

    Returns
    -------
    floar
        vector with data adjusted with sensitivity

    """
    A = diode_area
    L1=[]
    
    #import photodiode sensitivities
    pdc = pd.read_csv("SensitivityPhotodiode.dat", sep="\t", names=["WL", "S"])
    #perform and interpolation to smooth conversion
    pdc_int = interp1d(pdc.WL, pdc.S)
    sens_new_WL = np.linspace(200,1000, 1000 )
    sens_new = pdc_int(sens_new_WL)
    #calculate spectrum of lamp
    PC = calculate_PC(data, gain, change)
    #now multiply sensitivity
    for i in range(len(data.WL)):
        for j in range(len(sens_new_WL)):
            if (data.WL[i] >= sens_new_WL[j] and data.WL[i] < sens_new_WL[j+1]):
                L1.append(PC[i] /( 1e-3 * sens_new[j]))
                break
            else: continue
    L1 = np.asarray(L1)
    #return adjusted values in W/cm^2
    return L1/A