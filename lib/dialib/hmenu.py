import logging
from lib.dialib.confile import getconfig


class hmenu(object):
    def __init__(self,langconfig):
        messagefile=getconfig(langconfig)
        self.messages=messagefile.getconfig()
        messagefile.close()


    def menuButton(self,message,link):
        '''
        create a button to navigate in the menu
        parameters:
        1 : message to print in the button (to be found in lang
        config files)
        2 : link to next web page

        '''
        htmlpage='<td class="hmenu_left" width="10" height="32"></td>\n'
        htmlpage+='<td class="hmenu_center"><a href="{}">'.format(link)
        htmlpage+='{}</a></td>\n'.format(self.messages[message])
        htmlpage+='<td class="hmenu_right" width="10"></td>\n'
        htmlpage+='<td width="10"></td>\n'

        return htmlpage

    def actionfor(self,name):
        '''
        will create the appropriate menu for 'name' depending on its right
        firstly for admin user ...
        '''

        logging.debug('menu:actionfor %s',name)
        buttons=""
        if name=="admin":
            buttons+='<table border="0" cellspacing="0">\n<tr>\n'
            buttons+='<td>{} : </td>'.format(name)
            ### return to main menu
            buttons+=self.menuButton('retour','/')
            ### user manangement
            buttons+=self.menuButton('usermgt','/usermgt')
            ### folder management
            buttons+=self.menuButton('foldermgt','/foldermgt')
    
            buttons+='</tr>\n</table>\n'
        
        return buttons

    def usersAndGroup(self,name):
        ''' 
        page to manage users and group
        '''
        ### menu for userAndGroup page
        actions='<table border="0" cellspacing="0">\n<tr>\n'
        actions+='<td>{} : </td>'.format(name)
        actions+=self.menuButton('retour','/')
        actions+='</tr>\n</table>\n'
        ### affichage du menu
        htmlpage='<table border="0" cellspacing="0">\n<tr>\n'
        htmlpage+='<td>{} : </td>'.format(name)
        ### user manangement
        htmlpage+='</tr>\n</table>\n'

        return [actions,htmlpage]


    def foldersAndGroup(self,name):
        ''' 
        page to folder and group
        '''
        ### menu for userAndGroup page
        actions='<table border="0" cellspacing="0">\n<tr>\n'
        actions+='<td>{} : </td>'.format(name)
        actions+=self.menuButton('retour','/')
        actions+='</tr>\n</table>\n'
        ### affichage du menu
        htmlpage='<table border="0" cellspacing="0">\n<tr>\n'
        htmlpage+='<td>{} : </td>'.format(name)
        ### user manangement
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

