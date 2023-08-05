import os
from . import submodule

class obrpy(object):
    """
        Main class for correct management of .obr files

            Initialization:
            
                An object of class obrpy can be initialized either by specifying the path or leaving it unspecified, 
                in this case, a wizard will be displayed to select the folder where the .obr and other files will 
                be saved.

            Atributes:

                path (str)                       : absolute path to the root folder
                name (str)                       : name of the root folder (used as the name of the object) 
                folders (dict)                   : dictionary with the name of the folders where different files are storaged
                INFO (dict)                      : dictionary which contains the name of each external file created by this clase
                OBRfiles (dict)                  : dictionary which contains all OBRfile objects labeled with its filename
                settings (obj of class Settings) : object which contains all settings information

            Methods:

                - obr -
                mainOBR()               
                genOBRbook()        
                computeOBR()        
                update_OBRfiles()  

                - obrsdk -
                OBRSDKcalibration() 
                OBRSDKalignment()
                OBRSDKscan()
                OBRSDKextendedScan()

                - settings -
                genSettingsTemplate()
                genSettings()

                - load -
                load()              
                
                - save -
                save()              
                save_OBRfiles()     
                save_something()
                save_settings()   

                - update -
                update_OBRfiles() 
                update_OBRbook()
                update_settings()

            Classes:

                OBRfile()
                Settings()
    """

    def __init__(self,path=None,showpath=False) -> None:


        ######### Folder definition #########

        # Launch GUI if no path is provided
        if not path:
            from .PathSelector import PathSelector
            import tkinter as tk
            # Initialize gui
            root = tk.Tk()
            root.geometry("400x100")
            root.title("Path Selector")

            # Create gui
            app = PathSelector(master=root)
            app.pack_propagate(0)
            app.mainloop()

            # Get path
            path = app.path

        # In construction generates absolute path and name based on the folder name
        self.path = os.path.abspath(path)
        self.name = f'{os.path.basename(os.path.normpath(path))}.pkl'

        # Just to check it
        if showpath:
             print(os.listdir(self.path))

        ######### Load or creation #########

        # Tries to load dataset object, else, if not found, creates one
        try:      
            self.load()

        except Exception as e:
            if 'No such file or directory' in str(e):
                print('No obrpy object found in path')
                print('Creating new one \n')
                self.new()
            else:
                print(e)
                exit()

            

    ######### Classes definitions #########

    class OBRfile(object):
        """ Container class for '.obr' file information """

        def __init__(self,ID,filename,date):

            self.ID             = ID             # see ID_generator() for information
            self.filename       = filename
            self.name           = filename.replace('.obr','')
            self.date           = date           # %Y,%M,%D,%h:%m:%s
            self.f              = None           # [GHz]
            self.z              = None           # [m]
            self.Data           = None           # P, S
    
    class Settings(object):
        """ Class to manage settings information """

        def __init__(self,situation):

            self.situation = situation         
            self.info = {'Calibration':None,'Test':None}
            
            self.T0 = ''    # [ºC]
            self.T1 = ''    # [ºC/m]      T(x) = T0 + T1 * x  -> Name of temperature coeficients in OBRbook 
            self.E0 = ''    # []          E(x) = E0 + E1 * x  -> Name of strain coeficients in OBRbook
            self.E1 = ''    # [1/m]
            self.z_ini = 0  # Initial point of the segment of interest x=0
            self.z_fin = 0  # Final point of the segment of interest x=0
        
        def update(self):

            self.T0     = str(self.info['Calibration'].loc[0, 1])
            self.T1     = str(self.info['Calibration'].loc[0, 3])
            self.E0     = str(self.info['Calibration'].loc[1, 1])
            self.E1     = str(self.info['Calibration'].loc[1, 3])
            self.z_ini  = float(self.info['Calibration'].loc[2, 1])
            self.z_fin  = float(self.info['Calibration'].loc[3, 1])


    class Slice(object):
        """
        Container class for one slice
        """

        def __init__(self):
            self.ID           = 0       # ID of the slice, within the slices objet
            self.T            = 0       # Temperature of the slice
            self.E            = 0       # Strain of the slice
            self.z            = 0       # [m]   spatial axis
            self.x            = 0       # [mm]  Relative position of this slide into the segment of interest (to compute T and E as uniform variables)
            self.f_0          = 0       # [GHz] Initial scan frequency
            self.f_end        = 0       # [GHz] Final scan frequency
            self.delta        = 0       # [Number of points] Sensor spacing 
            self.window       = 0       # [Number of points] Sensor length
            self.date         = ''      # Date of the measurement formatted as %Y,%M,%D,%h:%m:%s
            self.parent_file  = ''      # File where the data has been extracted
            self.P            = list()  # p-polarization signal, later it will be a complex numpy array
            self.S            = list()  # s-polarization signal, later it will be a complex numpy array

    class Slices(object):

        """
        Class to contain a dataset of slices
        """

        def __init__(self):

                self.last_ID = -1
                self.slices  = dict()

        def update_from_file(self,path):

            self.path   = path
            self.name   = '' # TO BE DONE (just taking from path, you know ...)

            try:
                self.load()
                print('\nSLICES found!')

            except Exception as e:

                if 'No such file or directory' in str(e):
                    print('\nNO SLICES FOUND IN PATH')
                else:
                    print(e)
                    exit()

        from .load import load


    ######### Methods definitions #########

    # from .take_a_look import take_a_look # TO BE DONE

    from .load import load, new

    from .save import save, save_something , save_OBRbook, save_OBRfiles, save_settings, save_slicesbook, save_slices

    from .update import update_OBRbook, update_OBRfiles, update_settings, update_slicesbook, update_slicesbook_from_slices, update_slices, update_slices_from_slicesbook

    from .clear import clear_slices, clear_dataset

    from .checkouts import OBR_checkout, settings_file_checkout, slices_checkout
    
    from .obr import mainOBR, genOBRbook, computeOBR

    from .obrsdk import OBRSDKcalibration, OBRSDKalignment, OBRSDKscan, OBRSDKextendedScan

    from .settings import genSettingsTemplate, genSettings, _getNewValuesFromOBRbook

    from .ANALYSIS.global_analysis import global_analysis, global_analysis_GPU

    from .ANALYSIS.local_analysis import genSlices, _obr2slices