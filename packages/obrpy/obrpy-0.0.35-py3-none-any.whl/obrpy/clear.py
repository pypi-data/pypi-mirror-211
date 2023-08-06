import os

def clear_slices(self,auto=True):
    """ Function to clear slices and its book """

    if auto == True or 'n' not in input('Are you sure? (yes/no) '):
        
        obj_path    = os.path.join(self.path,self.folders['PROCESSED_DATA'],self.INFO['slices filename'])
        book_path   = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['slices book filename'])

        if os.path.exists(book_path):
            os.remove(book_path)
        if os.path.exists(obj_path):
            os.remove(obj_path)
        
        self.slices = self.Slices()
        self.slicesbook = None
    
    else:
        pass

def clear_dataset(self,auto=True):
    """ Function to clear dataset and its book """

    """
    if auto == True or 'n' not in input('Are you sure? (yes/no) '):
        os.remove(os.path.join(self.path,self.folders['3_DATASET'],self.INFO['dataset filename']))
        os.remove(os.path.join(self.path,self.folders['4_INFORMATION'],self.INFO['dataset book filename']))
    else:
        pass
    """