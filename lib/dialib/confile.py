#----------------------------------
# configuration file management
#----------------------------------

import logging
from os import chdir
from os.path import basename, dirname
from re import search

class confile(object):
    """configuration file management"""
    
    def __init__(self,file):
        self.d=dirname(file)
        self.f=basename(file)
        chdir(self.d)

        try:
            self.cfile=open(self.f,'r')
        except:
            print("FATAL ERROR :\n")
            print("Configuration file is not present.\n")
            print("File expected : {}/{}".format(self.d,self.f))
            quit()

    def get_val(self,pat):
        logging.debug("confile:get_val; pat=%s",pat)
        while 1:
            l=self.cfile.readline()
            r=search('([^\s]+)\s+([^\s]+)',l)
            if r != None:
                logging.debug("confile:get_val;line %s;%s",
                              r.group(1),r.group(2))
                if r.group(1) == pat:
                    logging.debug("confile:get_val;match !! %s->%s",
                                  r.group(1),r.group(2))
                    return r.group(2)
                else:
                    continue
            else:
                logging.debug("confile:get_val:%s not found",pat)
                return "NOT FOUND"
