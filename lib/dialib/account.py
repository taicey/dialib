from lib.dialib.sqlite3 import SQLite
import logging
import bcrypt
import cherrypy


class account(object):
    def __init__(self,name,pwd,dbfile):
        db=SQLite(dbfile)
        logging.debug("account:dbfile:%s",dbfile)
        req="select rowid,hashpass,id_group from users "
        req+='where name="{}"'.format(name)
        result=db.select(req)
        if result==[]:
            logging.info("account:user %s does not exist",name)
            cherrypy.session['mess']="userKO"
        else:
            id_name=result[0][0]
            hashpass=result[0][1]
            id_group=result[0][2]
            if bcrypt.hashpw(pwd,hashpass) == hashpass:
                ## password has been verified
                cherrypy.session['name']=name
                cherrypy.session['id_name']=id_name
                cherrypy.session['id_group']=id_group
                cherrypy.session['mess']="OK"
                logging.info("account:user %s:loged in",name)
            else:
                logging.info("account:user %s:wrong password",name)
                cherrypy.session['mess']="pwdKO"


    def hashpassword(self,pwd):
        return bcrypt.hashpw(pwd,bcrypt.gensalt())

