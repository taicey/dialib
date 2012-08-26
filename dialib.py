#!/usr/bin/python3
#import sqlite3
import logging
import cherrypy
import argparse
from os import walk, chdir
from os.path import join,exists,basename
from lib.dialib.confile import getconfig
from lib.dialib.sqlite3 import SQLite

##### Argument management#####
parser = argparse.ArgumentParser()
parser.add_argument("-l","--log", help="log level",
                    type=str,default="warning",
                    choices=['debug','info','warning','error','critical'])
parser.add_argument("-c","--config", help="path to config file",
                    type=str,required=True)
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
logging.basicConfig(filename=join(logpath,"dialib.log"),
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=args.log.upper(),
                    datefmt='%Y%m%d %H:%M:%S')

### test ###

class dialib(object):
    def __init__(self,config):
        logging.info("START dialib")
        self.dbf=config["dbfile"]
        self.htmlconf=config["html"]
        self.html ={}
        self.photo ={}

        f=open(self.htmlconf,'r')
        try:
            for ligne in f:
                if ligne[:2] == '[*':
                    label=ligne[2:]
                    label=label[:-1].strip()
                    label=label[:-2]
                    logging.debug("label=%s",label)
                    text=""
                else:
                    if ligne[:5]=="#####":
                        self.html[label]=text
                    else:
                        text+=ligne
        finally:
            f.close()
                        
        chdir(config["photopath"])


    def navigation(self,path='.'):
        #### getting list of directory in current folder
        db=SQLite(join(config["rootpath"],config["dbfile"]))
        req='select dirname from folder where folder.rowid in\n'
        req+='(select id_folder_son from folderParent\n'
        req+='inner join folder on id_folder_father=folder.rowid\n'
        req+='and dirname="{}")'.format(path)
        res=db.select(req)
        
        affpath="/"+path[2:]
        contenu='<table border=0>\n'
        ### affichage de l'arbo
        contenu+='<tr>\n<td valign="top">\n'
        contenu+='<div class="menu">'
        contenu+='<a href="navigation?path=.">\
        <img src="/highslide/home.png" width=25 height=25></a>'
        contenu+='{}\n<ul>\n'.format(affpath)
        for r in res:
            contenu+='<li><a href="navigation?path={}">{}</a></li>\n'.\
              format(r[0],basename(r[0]))
        contenu+='</ul>\n</td>\n'
        contenu+='</div>\n'

        #### getting list of image in current folder
        db=SQLite(join(config["rootpath"],config["dbfile"]))
        req='select filename from files where id_dir=\n'
        req+='(select rowid from folder where dirname="{}")'.format(path)
        res=db.select(req)

        #### affichage des thumbs
        contenu+='<td>\n'
        if res!=[]:
            for p in res:
                contenu+='<a class="highslide" '
                contenu+='href="/photos/{}/{}" '.format(path,p[0])
                contenu+='onclick="return hs.expand(this)">\n'
                contenu+='<img \
                src="/photos/{}/.Thumbnails/{}"/>'.format(path,p[0])
                contenu+='</a>\n'
    
    
        contenu+="</td></tr>\n</table>"
        HTMLpage=self.html["globalTemplate"].format(contenu)
        return HTMLpage
    
    navigation.exposed=True

cherrypy.quickstart(dialib(config),
                    config=join(config["rootpath"],config["cherrypy"]))
