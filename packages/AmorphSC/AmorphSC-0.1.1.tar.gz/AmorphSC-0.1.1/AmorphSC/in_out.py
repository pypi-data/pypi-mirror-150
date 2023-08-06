import glob
import pandas as pd

def import_char(prefix_file):
    """
    Function that imports all file in a folder with a specific prefix, recorded
    by Keysight SMU. It also print on console the order of imported files.

    Parameters
    ----------
    prefix_file : string
        Prefix of files that have to be imported

    Returns
    -------
    char : float
        Array of imported files

    """
    
    files_char = glob.glob(prefix_file)
    char = []
    for j in files_char:
        csv = pd.read_csv(j, sep="\t", header=1, names=["VG", "IG", "tG", "VD", "ID", "tD"])
        char.append(csv)
        print(j)
    return char

def import_cv(prefix_file):
        """
        Function that imports all file in a folder with a specific prefix, recorded
        by Zurich lockin. It also print on console the order of imported files.

        Parameters
        ----------
        prefix_file : string
            Prefix of files that have to be imported

        Returns
        -------
        char : float
            Array of imported files

        """
        
        files_cv = glob.glob(prefix_file)
        cv = []
        for j in files_cv:
            csv = pd.read_csv(j, sep=";", header=4, names=["Voff", "Amp"])
            cv.append(csv)
            print(j)
        return cv

def s4(a):
    return '{:.4e}'.format(a)

def s0(a):
    return '{:.0e}'.format(a)

def s1(a):
    return '{:.1e}'.format(a)

def import_PC(path):
    """
    Function that imports values of photocurrent from Elvis Card from UniBO

    Parameters
    ----------
    path : string
       Oath of file to be imported

    Returns
    -------
    tft : dataframe
        Dataframe with imported data

    """
    tft = pd.read_csv(path, header=13, 
                        names=["WL", "Amp", "Ph", "f", "s", "RMS", "IPCE"], sep="\t")
    return tft