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

import re
from os import chdir, walk
from os.path import basename,exists,join
import logging
import argparse
from lib.dialib.sqlite3 import SQLite
from lib.dialib.confile import getconfig
from lib.python.EXIF import process_file

##### Argument management#####
parser = argparse.ArgumentParser()
parser.add_argument("-l","--log", help="log level",
                    type=str,default="info",
                    choices=['debug','info','warning','error','critical'])
parser.add_argument("-c","--config", help="path to config file",
                    type=str,required=True)
parser.add_argument("-t","--createTables", help="recreate tables in db",
                    action="store_true")
args=parser.parse_args()

### getting conf in config file
if not exists(args.config):
    print("searchPhoto:provided config file does not exist")
    quit()
cfile=getconfig(args.config)
config=cfile.getconfig()
cfile.close()
##### Logging Management #####
logpath=join(config["rootpath"],config["logpath"])
logging.basicConfig(filename=join(logpath,"searchPhoto.log"),
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=args.log.upper(),
                    datefmt='%Y%m%d %H:%M:%S')

def thumbnail(fichier):
    return True

def getPathInDb(path):
    ### check folder into db
    reqs="select rowid from folder where dirname='{}'".format(path)
    db=SQLite(join(config["rootpath"],config["dbfile"]))
    return db.select(reqs)

def insertPathInDb(path):
    ### insert folder into db
    reqi="insert into folder values ('{}',0)".format(path)
    db=SQLite(join(config["rootpath"],config["dbfile"]))
    return db.upd_ins(reqi)




logging.info("START searchPhoto")
logging.info("searchPhoto:config file: %s",args.config)

### -t args have been passed : 
if args.createTables:
    logging.info("searchPhoto:createTable will run")
    db=SQLite(join(config["rootpath"],config["dbfile"]))
    res=db.create(join(config["rootpath"],config["tables"]))
    if res=="createOK":
        logging.info("searchPhoto:createTable run successfully")
    else:
        logging.error("searchPhoto:createTable run with error")

### start searching for files from photopath
bl=[]
filebl=open(join(config["rootpath"],config["blacklist"]),'r')
for l in filebl:
    bl.append(l[:-1])

chdir(config["photopath"])
### first, check/insert for "." path presence in db
res=getPathInDb(".")
if res==[]:
    insertPathInDb(".")

for root,dirs,files in walk("."):
    ### ignoring bliacklisted folders
    if basename(root) in bl:
        logging.debug("%s folder in blacklist",root)
        continue

    print(root)
    logging.debug("searchPhoto:folder:%s",root)
    ### check/insert folder into db
    res=getPathInDb(root)
    for rep in dirs:
        if rep not in bl:
            r=getPathInDb(join(root,rep))
            if r==[]:
                insertPathInDb(join(root,rep))
                r=getPathInDb(join(root,rep))
            ### link folder father and son...
            req='insert into folderParent values({},{})'.\
                 format(res[0][0],r[0][0])
            db=SQLite(join(config["rootpath"],config["dbfile"]))
            db.upd_ins(req)



    #### no files treatment if folder is emptu
    if files==[]:
        logging.debug("no files in %s",root)
        continue

    idDir=res[0]
    for f in files:
        logging.debug("searchPhoto:%s",join(root,f))
        ####### recherche si le fichier existe deja en base
        req="select id_dir,filename from files "
        req=req+"where id_dir = {} ".format(idDir[0])
        req=req+"and filename='{}'".format(f)
        res=db.select(req)
        if res==[]:
            fh=open(join(root,f),'rb')
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

    
    
    
