#!/usr/bin/python3
#--------------------------
#   search for photo from the path given in parameter
#    directory in blacklist config file will be ignore
#    --> 2 parameters : 
#        root path
#        black list file recheche des nouvelles photos
#--------------------------
# TODO
# TODO : si le fichier existe dans un autre repertoire : gestion du move ?
# TODO optimisation en regardant la date de derniere modification du rep
#      si mtime > mtime.db alors nouveau fichier dans le rep...
#      sinon rep suivant...

import os
import re
from os.path import basename
import logging
import argparse
from lib.dialib.sqlite3 import SQLite
from lib.python.EXIF import process_file

##### Argument management#####
parser = argparse.ArgumentParser()
parser.add_argument("-l","--log", help="log level",
                    type=str,default="warning",
                    choices=['debug','info','warning','error','critical'])
parser.add_argument("-b","--blacklist", help="path to blacklist file",
                    type=str,required=True)
parser.add_argument("-p","--path", help="root path for searching",
                    type=str,required=True)
args=parser.parse_args()

##### Logging Management #####
logging.basicConfig(filename="searchPhoto.log",
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=args.log.upper(),
                    datefmt='%Y%m%d %H:%M:%S')

def thumbnail(fichier):
    return True


logging.info("START searchPhoto")
os.chdir(args.path)
bl=[]
filebl=open(args.blacklist,'r')
for l in filebl:
    bl.append(l[:-1])

for root,dirs,files in os.walk("."):
    if basename(root) in bl:
        logging.debug("%s folder in blacklist",root)
        continue

    if files==[]:
        logging.debug("no files in %s",root)
        continue

    print(root)
    reqs="select rowid from folder where dirname='{}'".format(root)
    logging.debug("searchPhoto:%s",root)
    db=SQLite("/share/perso/dialib/sqlite3db/dialib.db")
    res=db.select(reqs)
    if res==[]:

        reqi="insert into folder values ('{}',0)".format(root)
        result=db.upd_ins(reqi)
        db=SQLite("/share/perso/dialib/sqlite3db/dialib.db")
        res=db.select(reqs)


    idDir=res[0]
    for f in files:
        logging.debug("searchPhoto:%s",os.path.join(root,f))
        ####### recherche si le fichier existe deja en base
        req="select id_dir,filename from files "
        req=req+"where id_dir = {} ".format(idDir[0])
        req=req+"and filename='{}'".format(f)
        res=db.select(req)
        if res==[]:
            fh=open(os.path.join(root,f),'rb')
            ######## check thumbnail
            thumbnail(fh)
            ######## get Exif
            data=process_file(fh,details=True)
            req="insert into files values ({},'{}',".format(idDir[0],f)
            if data=={}:
                req=req+"'','','','','','','','')"
                
            else:
                #x=list(data.keys())
                #x.sort()
                #for tag in x:
                #    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
                #        try:
                #            print("Key: {}; value {}".format(tag,data[tag]))
                #        except:
                #            print("error : {}".format(tag))
                try:
                    req=req+"{},".format(data['Image Model'].printable[1:])
                except:
                    req=req+"'',"
                try:
                    req=req+"'{}',".format(data['Image Orientation'])
                except:
                    req=req+"'',"
                try:
                    req=req+"{},".format(
                        data['EXIF DateTimeOriginal'].printable[1:])
                except:
                    req=req+"'',"
                try:
                    req=req+"'{}',".format(data['EXIF ExposureTime'])
                except:
                    req=req+"'',"
                try:
                    req=req+"'{}',".format(data['EXIF FNumber'])
                except:
                    req=req+"'',"
                try:
                    req=req+"'{}',".format(data['EXIF ExposureIndex'])
                except:
                    try:
                        req=req+"'{}',".\
                              format(data['EXIF ISOSpeedRatings'])
                    except:
                        req=req+"'',"
                try:
                    req=req+"'{}',".format(data['EXIF Flash'])
                except:
                    req=req+"'',"
                try:
                    req=req+"'{}')".format(data['EXIF FocalLength'])
                except:
                    req=req+"'')"


            result=db.upd_ins(req)
            fh.close()
        else:
            logging.debug("searchPhoto:file already in db")

    
    
    
