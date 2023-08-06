import pandas as pd
import os


def genSettingsTemplate(self) -> None:

    if os.path.exists(os.path.join(self.path,self.folders['INFORMATION'],self.INFO['settings filename'])):
        name = self.INFO['settings filename'].replace('.xlsx','_template.xlsx')

    else:
        name = self.INFO['settings filename']

    print('Creating a conditions file template in:')
    print('', os.path.join(self.path,self.folders['INFORMATION'],name))

    # create a new Excel file
    writer = pd.ExcelWriter( os.path.join(self.path,self.folders['INFORMATION'],name), engine='xlsxwriter')

    # create the "Calibration" sheet
    calibration_data = CalibrationTemplate()
    calibration_data.to_excel(writer, sheet_name='Calibration', index=False)

    # create the "Test" sheet
    new_values = self._getNewValuesFromOBRbook() 
    test_data = TestTemplate(new_values)
    test_data.to_excel(writer, sheet_name='Test')

    # save the Excel file
    writer.save()


    print('','please open and edit it')

def CalibrationTemplate() -> pd.DataFrame:
    """ 
        Generates a tempate datafreme used to generate the seetings for the calibration situation.
        In the calibration situation the microstrain (Delta eps) and temperature (Delta T) 
        are asumed to vary in a linerar way, and only one segment (from z_ini->x=0 to z_fin)
        of the fiber is subjected to these variations.

    """

    data = [
        ['Delta T = ','','+ ','','x [m]'],
        ['Delta eps = ','','+ ','','x [m]'],
        ['z_ini [m] =',''],
        ['z_fin [m] =','']
    ]
    df = pd.DataFrame(data)
    return df

def _getNewValuesFromOBRbook(self) -> list:
    
    """ 
        Get the new values written in the OBRbook by the user.

    """

    # Read the CSV file
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['OBR book filename'])
    df = pd.read_csv(book_path)

    # Get the column names
    column_names = df.columns.tolist()

    # Remove the old ones
    column_names.remove('ID')
    column_names.remove('filename')
    column_names.remove('date')

    return column_names


def TestTemplate(new_values) -> pd.DataFrame:
    """ 
        Generates a template dataframe used to generate the seetings for a situation where 
        several measurements are performed during a process where some magnitudes vary e.g. 
        load, temperature, time, ...

        *param: new_values(list) 
    """
    
    columns = ['Units','xlabel','ylabel']
    df = pd.DataFrame(columns=columns, index=new_values)

    return df


def genSettings(self,situation:str) -> None:
    """ 
        Generate settings object out of the setting .xlxs template created before

        * param: situation: identifies the use given to the FOS 
                            "Calibration" stands for calibration of the own sensor (see CalibrationTemplate() for more info)
                            "Test" stands for general user of FOS sensor (see TestTemplate() for further information)
    
    """

    # Generate an object of class settings

    self.settings = self.Settings(situation)

    # read the Excel file
    with pd.ExcelFile(os.path.join(self.path,self.folders['INFORMATION'],self.INFO['settings filename'])) as reader:
        
        # read the Calibration sheet into a dataframe
        calibration_df = pd.read_excel(reader, sheet_name='Calibration')

        # read the Test sheet into a dataframe
        test_df = pd.read_excel(reader, sheet_name='Test')

    # create a dictionary with the dataframes
    self.settings.info = {
        'Calibration': calibration_df,
        'Test': test_df
}