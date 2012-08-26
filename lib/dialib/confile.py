#----------------------------------
# configuration file management
#----------------------------------

import logging
from os import chdir
from os.path import basename, dirname
from re import search
class getconfig(object):
    """ get the complete config file into a dictionary"""
    def __init__(self,f):
        self.f=f
        self.config={}
        try:
            self.cfile=open(self.f,'r')
        except:
            print("confile:cannot open confile : {}",format(self.f))

    def getconfig(self):
        for l in self.cfile:
            r=search('([^\s]+)\s+([^\s]+)',l)
            if r != None:
                self.config[r.group(1)]=r.group(2)
        return self.config

    def close(self):
        self.cfile.close()



class confile(object):
    """configuration file management"""
    
    def __init__(self,f):
        self.f=f
        try:
            self.cfile=open(self.f,'r')
        except:
            print("FATAL ERROR :\n")
            print("Configuration file is not present.\n")
            print("File expected : {}".format(self.f))


    def get_val(self,pat):
#        logging.debug("confile:get_val; pat=%s",pat)
        while 1:
            l=self.cfile.readline()
            r=search('([^\s]+)\s+([^\s]+)',l)
            if r != None:
#                logging.debug("confile:get_val;line %s;%s",
#                              r.group(1),r.group(2))
                if r.group(1) == pat:
#                    logging.debug("confile:get_val;match !! %s->%s",
#                                  r.group(1),r.group(2))
                    return r.group(2)
                else:
                    continue
            else:
#                logging.warning("confile:get_val:%s not found",pat)
                return "NOT FOUND"

    def close(self):
        self.cfile.close()

