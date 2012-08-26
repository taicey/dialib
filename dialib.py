#!/usr/bin/python3
#import sqlite3
import logging
import cherrypy
import argparse
from os import walk, chdir
from os.path import join
from lib.dialib.confile import confile
from lib.dialib.sqlite3 import SQLite

##### Argument management#####
parser = argparse.ArgumentParser()
parser.add_argument("-l","--log", help="log level",
                    type=str,default="warning",
                    choices=['debug','info','warning','error','critical'])
args=parser.parse_args()

##### Logging Management #####
logging.basicConfig(filename="dialib.log",
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=args.log.upper(),
                    datefmt='%Y%m%d %H:%M:%S')

### test ###

class dialib(object):
    def __init__(self,root="/share/perso/photos/test"):
        logging.info("START dialib")
        dbc=confile("/share/perso/dialib/conf/db.conf")
        self.dbf=dbc.get_val("dbfile")
        self.htmlconf=dbc.get_val("html")
        self.html ={}
        self.arbo ={}
        self.photo ={}
        self.prevarbo ={}

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
                        
        chdir(root)
        for cur,dirs,files in walk("."):
            self.arbo[cur]=dirs
            self.photo[cur]=files
            if cur != ".":
                self.prevarbo[cur]=prev
            prev=cur
            


    def navigation(self,path='.'):
        affpath="/"+path[2:]
        contenu='<table border=0>\n'
        ### affichage de l'arbo
        contenu+='<tr>\n<td valign="top">\n'
        contenu+='<div class="menu">'
        contenu+='<a href="navigation?path=.">\
        <img src="/highslide/home.png" width=25 height=25></a>'
        contenu+='{}\n<ul>\n'.format(affpath)
        for p in self.arbo[path]:
            contenu+='<li><a href="navigation?path={}">{}</a></li>\n'.\
              format(join(path,p),p)
        contenu+='</ul>\n</td>\n'
        contenu+='</div>\n'

        #### affichage des thumbs
        contenu+='<td>\n'
        if self.photo[path]!=[]:
            for p in self.photo[path]:
                contenu+='<a class="highslide" '
                contenu+='href="/photos/{}/{}" '.format(path,p)
                contenu+='onclick="return hs.expand(this)">\n'
                contenu+='<img \
                src="/photos/{}/.Thumbnails/{}"/>'.format(path,p)
                contenu+='</a>\n'
    
    
    
    
        contenu+="</td></tr>\n</table>"
        HTMLpage=self.html["globalTemplate"].format(contenu)
        return HTMLpage
    
    navigation.exposed=True

cherrypy.quickstart(dialib(),config="/share/perso/dialib/conf/dialib.conf")
