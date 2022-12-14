from . import instrument,facility
from .import_tools import *
loadlib = {
            'imap_lo_em':instrument.IMAP_lo_EM.load
            }

def load(loc,instrument = 'imap_lo_em',dtype = 'TOF_DE_sample',version = 'v001',load_type = 'file'):
    if load_type is 'file':
        return(loadlib[instrument](loc,dtype,version))
    elif load_type is 'directory':
        return(get_all_dat(loc,dtype,loadlib[instrument],{'dtype':dtype,'version':version}))



