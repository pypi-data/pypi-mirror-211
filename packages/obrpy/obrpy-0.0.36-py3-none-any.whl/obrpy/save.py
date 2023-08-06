import os
import pickle as pickle
import pandas as pd

def save(self) -> None:
    """ Save the object in the root of folder """

    # Change self and its objects to global

    if 'self' in globals():
        pass
    else:
        globals()['self'] = self

    for key in self.__dict__.keys():
        if isinstance(self.__dict__[key], object):
            globals()[key] = self.__dict__[key]

    # Define path

    path_to_dataset = os.path.join(self.path,self.name)

    # Save with pickle

    with open(path_to_dataset, 'wb') as outp:
        pickle.dump(self.__dict__, outp, pickle.HIGHEST_PROTOCOL)
    print(f'---> {self.name} saved!')

    # Return self and its objects to local

    if 'self' in globals():
        del globals()['self']
    else:
        pass

    for key in self.__dict__.keys():
        if isinstance(self.__dict__[key], object):
            del globals()[key]
        else:
            pass

def save_something(self,object_to_save: object,path_to:str) -> None:
    
    """ Function to save something
        :param: object_to_save (obj): object to be saved
        :param: path_to (str): path to the directory where the object will be saved"""


    # Save with pickle
    with open(path_to, 'wb') as outp:
        pickle.dump(object_to_save, outp, pickle.HIGHEST_PROTOCOL)
    print('--> object saved in',path_to)

def save_OBRfiles(self) -> None:

    """ Save OBRfiles once computed """

    path_to = os.path.join(self.path,self.folders['PROCESSED_DATA'],self.INFO['OBRfiles filename'])
    object_to_save = self.OBRfiles
    self.save_something(object_to_save,path_to)
    print('--> OBRfiles saved in',path_to)

def save_OBRbook(self) -> None:

    """ Save OBRbook as .csv"""
    
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['OBR book filename'])
    self.OBRbook.to_csv(book_path, index=False)
    print('--> OBRbook saved in', book_path)


def save_settings(self) -> None:

    """ Save settings to .xlsx """

    # overwrite settings
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['settings filename'])
    writer = pd.ExcelWriter( book_path, engine='xlsxwriter')

    # create the "Calibration" sheet
    calibration_data = self.settings.info['Calibration']
    calibration_data.to_excel(writer, sheet_name='Calibration', index=False)

    # create the "Test" sheet
    test_data =self.settings.info['Test']
    test_data.to_excel(writer, sheet_name='Test', index=False)

    # save the Excel file
    writer.save()
    print('--> settings file saved in', book_path)

def save_slicesbook(self) -> None:

    """ Save slices book as .csv"""
    
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['slices book filename'])
    self.slicesbook.to_csv(book_path, index=False)
    print('--> slices book saved in', book_path)


def save_slices(self) -> None:

    """ Save slices once computed """

    path_to = os.path.join(self.path,self.folders['PROCESSED_DATA'],self.INFO['slices filename'])
    object_to_save = self.slices
    self.save_something(object_to_save,path_to)