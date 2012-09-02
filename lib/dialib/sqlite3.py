#----------------------------
# SQLite3 management
#----------------------------

import sqlite3
import logging
import random
import bcrypt
from re import search


class SQLite(object):
    '''
    SQLite3 management
    '''

    def __init__(self, dbf):
        self.dbf=dbf

    def runSQL(self,req,action):
        '''
        run SQL command 
        do call this function outside the Object
        '''
        try:
            logging.debug("SQLite:opendb:file db:%s",self.dbf)
            self.conn=sqlite3.connect(self.dbf)
            self.cur=self.conn.cursor()
        except Exception as err:
            logging.critical("SQLite:opendb:db file cannot been opened!")
            return action+"KO"
        try:
            logging.debug("SQLite:runSQL:%s",req)
            self.cur.execute(req)
        except Exception as err:
            logging.error("SQLite:runSQL:%s",err)
            if action != "select":
                return action+"KO"

        if action!= "select":
            self.conn.commit()
            return action+"OK"
        else: 
            result=self.cur.fetchall()
            self.conn.commit()
            return result


    def select(self,request):
        result=self.runSQL(request,"select")
        logging.debug("SQLite:select:closedb")
        self.conn.close()
        return result


    def upd_ins(self,request):
        status=self.runSQL(request,"upd_ins")
        logging.debug("SQLite:upd_ins:closedb")
        self.conn.close()
        return status
            
    def create(self,conffile):
        '''
        table creation according to conffile definition
        expected in conffile : 
            table name
            field name
            file type
        separated with ":"

        creation of admin group and admin user
        default password for admin is admin !

        '''
        try:
            logging.debug("SQLite:create:conffile:%s",conffile)
            cf=open(conffile,"r")
        except Exception as err:
            logging.error("SQLite:create:%s ",err)
            return "createKO"

        req="create table "
        table=""
        for line in cf:
            s=search('([^:]+):([^:]+):([^:]+)',line)
            if s.group(1)!=table:
                if table == "":
                    req=req+"{} ({} {}".format(s.group(1),s.group(2),s.group(3))
                    table=s.group(1)
                else:
                    req=req+")".format(s.group(2),s.group(3))
                    status=self.runSQL(req,"create")
                    table=s.group(1)
                    req="create table {} ({} {} ".\
                        format(table,s.group(2),s.group(3))
            else:
                req=req+" ,{} {}".format(s.group(2),s.group(3))
        req=req+")"
        status=self.runSQL(req,"create")

        ### user and group admin creation
        ### insert a random number of row in the table user before create admin
        ### to avoid havin always id_admin = 0
        id=random.randrange(10,100)
        reqi='insert into users (name) values ("rand")'
        reqd='delete from users where name="rand"'
        i=0
        while i<id:
            status=self.runSQL(reqi,"upd_ins")
            i+=1
        
        self.runSQL(reqd,"upd_ins")
        req='insert into groups values("admin")'
        self.runSQL(req,"upd_ins")
        req='select rowid from groups where name="admin"'
        result=self.runSQL(req,"select")
        hashadmin=bcrypt.hashpw("admin",bcrypt.gensalt())
        req='insert into users (name,hashpass,id_group) '
        req+='values ("admin","{}",{})'.format(hashadmin,result[0][0])
        self.runSQL(req,"upd_ins")


        logging.debug("SQLite:closedb")
        self.conn.close()
        return status
            
