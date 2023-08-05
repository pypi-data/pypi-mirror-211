import os
import pandas as pd
import numpy as np
import glob
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .UTILS.read_OBR import multi_read_OBR

def mainOBR(self,limit1=None,limit2=None) -> None:
    """ Computes the following sequence:
            
        * First generates OBR book from OBR filenames and the date recorded in each .obr
                
            self.genOBRbook()

        * Then open each one and reads relevant information in the specified segment
                
            self.computeOBR(limit1,limit2)

        * Finally OBR information is saved
                
            self.save_OBRfiles() 
        
        :optional limit1 (float/bool)=None: Initial point of the region of interest 
        :optional limit2 (float/bool)=None: Final   point of the region of interest 
    
    """

    self.genOBRbook()
    self.computeOBR(limit1,limit2)
    self.save_OBRfiles()

def genOBRbook(self,auto_overwrite=False) -> pd.DataFrame:
    """
    Function to generate OBR book from OBR filenames and the date recorded in each .obr

        :optional: auto_overwrite (bool) = False: if True the OBRbook will be auto-overwritten
        :returns: df (pd.Dataframe): dataframe from OBR book file

    """

    # Check current information

    if self.OBRbook == None:
        print('OBR book not found')
        print(' Creating a new one ...')
        save_df  = True
        save_obj = True
    elif self.OBRbook != None and len(self.OBRfiles) == 0:
        print('OBR book found but not registered')
        print(' Registering ...')
        save_df  = False
        save_obj = True
    else:
        print('OBR book found and registered')
        if auto_overwrite==True:
            print(' Auto-overwrite enabled, OBRbook will be overwitten')
            save_df  = True
            save_obj = True
        else:
            if 'n' in input(' Do you want to overwrite?(yes/no)'):
                return self.OBRbook
            else:
                save_df  = True
                save_obj = True

    # Get all OBR files
    OBR_files = find_OBR(os.path.join(self.path,self.folders['OBR']))
    # Initialize dataframe
    df = pd.DataFrame()

    # Loop through OBR files
    for filename in OBR_files:
        # Get date
        date = get_date(os.path.join(self.path,self.folders['OBR'],filename))
        # Get ID from date
        ID = ID_generator(date)
        # Append to object OBRfile
        if save_obj:
            self.OBRfiles[filename.replace('.obr','')] = self.OBRfile(ID,filename,date)
        # Append to dataframe
        df = df.append({
            'ID':           ID,
            'filename':     filename,
            'date':         date},
             ignore_index=True)
        
        
    # Sort dataframe by ID
    df.sort_values('ID')

    # Save dataframe to csv
    if save_df:
        self.OBRbook = df
        self.save_OBRbook()
        # Return dataframe
        return df
    else:
        print('Done!')
        return df

def computeOBR(self,limit1=None,limit2=None) -> None:
    """
    Reads all .obr files and registers information: f,z and Data = [Pc,Sc,Hc]
    among currently existing (filename, name, flecha, temperature and date)

    * If RAM is not able to allocate enough memory the object will be saved and
    by running this function a couple of times all the information will be
    sotoraged correctly

    :optional: limit1 (bool) = None
    :optional: limit2 (bool) = None

        * If both limits (limit1 and limit2) are None, a prompt will be displayed asking for them
        * If some limit  (limit1 or  limit2) is False, no prompt will be displayed asking for them and will be assumed that the users wants to keep the whole OBR readouts 

    """

    # Check if information files exists
    if not isinstance(self.OBRbook,pd.DataFrame) and len(self.OBRfiles) == 0:
        print('\n','OBR book not found or not registered')
        print('Please, create/register a new one calling')
        print('DATASET.genOBRbook()')
        return
    else:
        pass

    # Check for region of interest
    if limit1==None and limit2==None:

        if self.settings.info['Calibration'] is None and self.settings.info['Test'] is None:
            # If there is not settings file, display warning
            print('WARNING: No settings found')
            print('Please if you want to configure the DOFS settings run:')
            print('     your_obrpy_object.genSettingsTemplate()')
            print('and edit it')
            print('WARNING: No limits were specified')
            print(' if you want to compute the full lenght of sensors leave empty the next prompts')

            limit1 = input(' Region of interest start point [m]: ')
            limit2 = input(' Region of interest end point [m]: ')

            limit1 = False if limit1 == "" else float(limit1)
            limit2 = False if limit2 == "" else float(limit2)


        else:
            # Gets limits from settings
            
            limit1 = self.settings.z_ini
            limit2 = self.settings.z_fin

    # Generate datasets from selected data
    for key, OBRfile in self.OBRfiles.items():

        import psutil
        if psutil.virtual_memory()[2] < 90:

            if not hasattr(OBRfile, 'Data') or OBRfile.Data is None:
                # Read .obr file
                f,z,Data = multi_read_OBR([OBRfile.name],os.path.join(self.path,self.folders['OBR']),limit1=limit1,limit2=limit2)
                # Update OBR file register
                OBRfile.f           = f
                OBRfile.z           = z
                OBRfile.Data        = Data[OBRfile.name]
            else:
                pass

        else:
            # Esta parte hay que mejorarla para la 2.0
            print('\nUnable to allocate more information')
            print("DON'T PANIC the information will be saved")
            print('just run again DATASETS.computeOBR() until no more .obr files are read')
            self.save()
            return False
            exit()

    return True

def find_OBR(path:str, verbose=False) -> list:
    """ Function to find all .obr files from a folder

        param:  path      (str)          : path to folder
        return: OBR_files (list of str)  : list of OBR filenames

    """
    # Find all .obr files
    OBR_files = glob.glob(os.path.join(path,'*.obr'))
    print(OBR_files) if verbose else None
    # Keep just filename and extension (basename)
    OBR_files = [os.path.basename(f) for f in OBR_files]
    print(OBR_files) if verbose else None
    return OBR_files

def get_date(file:str) -> str:
    """
    Open an .obr file to get date of the measure

        param: file (str): file to be read
        return: DateTime (str): date formated as %Y,%M,%D,%h:%m:%s

    """

    # Data lecture (all this offsets are heritage from read_OBR())
    offset = np.dtype('<f').itemsize
    offset += np.dtype('|U8').itemsize
    offset = 12 # Ni idea de por qué este offset pero funciona
    offset += np.dtype('<d').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('uint16').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('int32').itemsize
    offset += np.dtype('int32').itemsize
    offset += np.dtype('uint32').itemsize
    offset += np.dtype('uint32').itemsize

    DateTime=np.fromfile(file, count=8,dtype= 'uint16',offset = offset)                              # Measurement date

    DateTime=f'{DateTime[0]},{DateTime[1]},{DateTime[3]},{DateTime[4]}:{DateTime[5]}:{DateTime[6]}'  # "2022,03,03,13:41:27"

    return DateTime

def ID_generator(date:str) -> str:
    """ Function to create OBRfile ID. As is written now, it just takes the date and converts it into a plain integer 
    
            :param: date (str): date where the measure was taken, it is formatted as %Y,%M,%D,%h:%m:%s
            :returns: date formatted as: %Y%M%D%h%m%s (str)
    
    """
    
    return date.replace(',','').replace(':','')

