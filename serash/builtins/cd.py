import os
from serash.constants import *

def cd(args):
    HOME = os.getenv("HOME")
    
    if not args :
        os.chdir(HOME)
        print (HOME)
    else :
        try :
            os.chdir(args[0])
        except OSError :
            print ("Error path ! ")

    return stat_r
