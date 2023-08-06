import subprocess
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'obrsdk'))

def OBRSDKcalibration(self, verbose=True) -> None:
    """ Performs Luna's OBR-4600 calibration
     
        Only works in a Windows environment :( 
    
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')

    output = subprocess.check_output(f"{exe_path} -c")

    if verbose:
        for line in output.splitlines():
            print(line)


def OBRSDKalignment(self,verbose=True) -> None:
    """ Performs Luna's OBR-4600 optical alignment         
    
        Only works in a Windows environment :( 
    
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')
    
    output = subprocess.check_output(f"{exe_path} -a")

    if verbose:
        for line in output.splitlines():
            print(line)

def OBRSDKscan(self,filepath:str,verbose=True):
    """ Acquires measurement

        * param: filepath: path to save the .obr file

        Only works in a Windows environment :( 

    """
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')

    output = subprocess.check_output(f"{exe_path} -s {filepath}")

    if verbose:
        for line in output.splitlines():
            print(line)

    return

def OBRSDKextendedScan(self,filepath:str,verbose=True):
    """ Acquires measurement in extended scan format (less precission)

        * param: filepath: path to save the .obr file

        Only works in a Windows environment :( 
    
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(current_directory, 'obrsdk', 'obr.exe')

    output = subprocess.check_output(f"{exe_path} -e {filepath}")

    if verbose:
        for line in output.splitlines():
            print(line)

    return

    return
