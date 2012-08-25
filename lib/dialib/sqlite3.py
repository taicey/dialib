#----------------------------
# SQLite3 management
#----------------------------

import sqlite3
import logging
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
            logging.debug("SQLite:runSQL:closedb")
            self.conn.close()
            if action != "select":
                return action+"KO"

        if action!= "select":
            logging.debug("SQLite:closedb")
            self.conn.commit()
            self.conn.close()
            return action+"OK"
        else: 
            result=self.cur.fetchall()
            logging.debug("SQLite:closedb")
            self.conn.commit()
            self.conn.close()
            return result


    def select(self,request):
        result=self.runSQL(request,"select")
        return result


    def upd_ins(self,request):
        status=self.runSQL(request,"upd_ins")
        return status
            
    def create(self,conffile):
        '''
        table creation according to conffile definition
        expected in conffile : 
            table name
            field name
            file type
        separated with ":"
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
        return status



        self.conn.commit()
        logging.debug("SQLite:closedb")
        self.conn.close()
        return status
            
