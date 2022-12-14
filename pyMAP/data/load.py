from . import instrument,facility
from .import_tools import *
loadlib = {
            'imap_lo_em':instrument.IMAP_lo_EM.load
            }

def load(loc,instrument = 'imap_lo_em',
                            dtype = 'TOF_DE_sample',
                            load_params = {}):
    import os
    if os.path.isfile(loc):
        return(loadlib[instrument](loc,dtype,**load_params))
    elif os.path.isdir(loc):
        return(get_all_dat(loc,dtype,loadlib[instrument],**load_params))



