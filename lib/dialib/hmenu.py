import logging
import cherrypy
from lib.dialib.confile import getconfig
from lib.dialib.sqlite3 import SQLite


class hmenu(object):
    def __init__(self,langconfig,dbfile):
        messagefile=getconfig(langconfig)
        self.messages=messagefile.getconfig()
        messagefile.close()
        self.db=SQLite(dbfile)


    def menuButton(self,message,link,anchor=""):
        '''
        create a button to navigate in the menu
        parameters:
        1 : message to print in the button (to be found in lang
        config files)
        2 : link to next web page

        '''
        htmlpage='<td class="hmenu_left" width="10" height="32"></td>\n'
        htmlpage+='<td class="hmenu_center"><a href="{}"'.format(link)
        if anchor!="":
            htmlpage+=' class="highslide" id="{}" '.format(anchor)
            htmlpage+='onclick="return hs.htmlExpand(this,'
            htmlpage+='{objectType: \'iframe\', outlineType: '
            htmlpage+='\'rounded-white\'})"\n'
        htmlpage+='>{}</a></td>\n'.format(self.messages[message])
        htmlpage+='<td class="hmenu_right" width="10"></td>\n'
        htmlpage+='<td width="10"></td>\n'

        return htmlpage

    def actionfor(self,name):
        '''
        will create the appropriate menu for 'name' depending on its right
        firstly for admin user ...
        '''

        logging.debug('menu:actionfor %s',cherrypy.session['name'])
        buttons='<table border="0" cellspacing="0">\n<tr>\n'
        buttons+='<td>{} : </td>'.format(cherrypy.session['name'])
        if name=="admin":
            ### return to main menu
            buttons+=self.menuButton('retour','/')
            ### user manangement
            buttons+=self.menuButton('usermgt','/usermgt')
            ### folder management
            buttons+=self.menuButton('foldermgt','/foldermgt')
    
        buttons+='</tr>\n</table>\n'
        
        return buttons

    def manageList(self,message,req):
        '''
        manage a list of element (allow to list, add, delete element)
        '''

        List=self.db.select(req)
        htmlpage='<h3>{}</h3>\n'.format(self.messages[message])
        for element in List:
            htmlpage+='<p><a href="highslide/users.html" class="highslide"'
            htmlpage+=' onclick="return hs.htmlExpand(this,'
            htmlpage+='{objecType:\'iframe\', outlineType: \'rounded-white\'})">\n'
            try:
                htmlpage+='{}</a> [{}]</p>\n'.format(element[0],element[1])
            except:
                htmlpage+='{}</a></p>\n'.format(element[0])

        ### table for action button
        htmlpage+='<table border="0" cellspacing="0">\n<tr>\n'
        link="/highslide/{}.html".format(message)
        htmlpage+=self.menuButton('create',link,message)
        htmlpage+='</tr>\n</table>\n'

        return htmlpage


    def usersAndGroup(self):
        ''' 
        page to manage users and group
        '''
        ### menu for userAndGroup page
        logging.debug("in usersAndGroup[%s]",cherrypy.session['name'])
        actions='<table border="0" cellspacing="0">\n<tr>\n'
        actions+='<td>{} : </td>'.format(cherrypy.session['name'])
        actions+=self.menuButton('retour','/')
        actions+='</tr>\n</table>\n'

        ### user manangement
        htmlpage='<td valign="top">\n'
        ### get list of users from db
        req='select users.name,groups.name from users,groups '
        req+='where users.id_group=groups.rowid'
        htmlpage+=self.manageList('listuser',req)

        ### end of user management
        htmlpage+='</td>\n'

        htmlpage+='<td width="20"></td>'

        ### group management
        htmlpage+='<td valign="top">\n'
        ### get list of groups from db
        req='select name from groups'
        htmlpage+=self.manageList('listgroup',req)

        ### end of folder management
        htmlpage+='</td>\n'

        return [actions,htmlpage]


    def foldersAndGroup(self):
        ''' 
        page to folder and group
        '''
        ### menu for folderAndGroup page
        logging.debug("in foldersAndGroup[%s]",cherrypy.session['name'])
        actions='<table border="0" cellspacing="0">\n<tr>\n'
        actions+='<td>{} : </td>'.format(cherrypy.session['name'])
        actions+=self.menuButton('retour','/')
        actions+='</tr>\n</table>\n'
        ### folder manangement
        htmlpage='<table border="0" cellspacing="0">\n<tr>\n'
        htmlpage+='<td>{} : </td>'.format(cherrypy.session['name'])
        htmlpage+='</tr>\n</table>\n'

        return htmlpage

    def unknown(self):
        '''
        only return button for unknown users
        '''
        htmlpage='<table border="0" cellspacing="0">\n<tr>\n'
        htmlpage+='<p class="error">{}</p>'.format(self.messages['notconnect'])
        htmlpage+=self.menuButton('retour','/')
        htmlpage+='</tr>\n</table>\n'

        return htmlpage

