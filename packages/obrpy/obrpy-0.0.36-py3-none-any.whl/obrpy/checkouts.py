import os


def settings_file_checkout(self,stop=True):
    """ Settings file checkout """

    settings_file =   os.path.join(self.path,self.folders['INFORMATION'],self.INFO['settings filename'])

    if not os.path.exists(settings_file):
        print('No settings file found')
        self.genSettingsTemplate()
        exit() if stop else None

def OBR_checkout(self, verbose=True):

    """ OBR checkout """

    # Check if OBRfiles are already computed
    if len(self.OBRfiles) == 0:
        print('No OBRbook created, creating and computing ...') if verbose else None
        self.mainOBR()

    if not any([hasattr(OBRfile, 'Data') for key, OBRfile in self.OBRfiles.items()]):
        print('No data in OBRfiles, computing...') if verbose else None
        self.computeOBR()
    else:
        print('OBR data already computed') if verbose else None
        pass

def slices_checkout(self):

    # Check if slices were previously created
    if not isinstance(self.slices,bool) and len(self.slices.slices) != 0 : 
        ans = input('\nSLICES already computed (append/overwrite/quit):')
        if 'a' in ans:
            pass
        if 'o' in ans:
            self.clear_slices(auto=True)
        if 'q' in ans:
            return False
        
    else:
        return True