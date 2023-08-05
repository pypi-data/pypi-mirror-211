import os
import pickle
import shutil

def load(self) -> None:
    """ Load the object existing in the root of the folder """

    path_to_dataset = os.path.join(self.path,self.name)

    new_path = self.path
    new_name = self.name

    with open(path_to_dataset, 'rb') as inp:
        self.__dict__ = pickle.load(inp)

    self.path = new_path
    self.name = new_name

    print(f'---> {self.name} loaded!')

    return self

def new(self) -> None:

    """ Creates a new obrpy folder structure and initializes atributes and objects """

    # Folder structure
    self.folders = {
    'OBR'              : './0_OBR',
    'PROCESSED_DATA'   : './1_PROCESSED_DATA',
    'INFORMATION'      : './2_INFORMATION'}

    # Creates folder structure if not exists
    for key,val in self.folders.items():
        if not os.path.exists(os.path.join(self.path,val)):
            os.makedirs(os.path.join(self.path,val))

    # Move all .obr files to its folder, if they exists
    for file in os.listdir(self.path):
        if file.endswith('.obr'):
            print('Moving',file,'to',self.folders['OBR'])
            shutil.move(os.path.join(self.path,file), os.path.join(self.path,self.folders['OBR'],file))

    # Information filenames
    self.INFO = {
    'OBR book filename'             :   'OBR_book.csv',
    'OBRfiles filename'             :   'OBRfiles.pkl',
    'settings filename'             :   'settings.xlsx',
    'slices book filename'          :   'slices_book.csv',
    'slices filename'               :   'slices.pkl',
    '':'',
    'measures filename'             :   'measures.pkl',
    'dataset book filename'         :   'dataset_book.csv',
    'dataset filename'              :   'dataset.pkl',
    'fiber distribution filename'   :   'fiber_distribution.txt'}

    ######### Other atributes inicialization  #########

    # All OBR files as a dictionary
    self.OBRfiles = dict()

    # OBR book as a pandas df 
    self.OBRbook = None

    # Settings
    self.settings = self.Settings(None)

    # Slices
    self.slices = self.Slices()

    # Slices book as pandas df
    self.slicesbook = None