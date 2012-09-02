import logging
from lib.dialib.confile import getconfig


class hmenu(object):
    def __init__(self,langconfig):
        messagefile=getconfig(langconfig)
        self.messages=messagefile.getconfig()
        messagefile.close()


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
            ### user manangement
            buttons+='<td class="hmenu_left" width="10" height="32"></td>\n'
            buttons+='<td class="hmenu_center"><a href="/usermgt">'
            buttons+='{}</a></td>\n'.format(self.messages['usermgt'])
            buttons+='<td class="hmenu_right" width="10"></td>\n'
            buttons+='<td width="10"></td>\n'
            ### group management
            buttons+='<td class="hmenu_left" width="10" height="32"></td>\n'
            buttons+='<td class="hmenu_center"><a href="/groupmgt">'
            buttons+='{}</a></td>\n'.format(self.messages['groupmgt'])
            buttons+='<td class="hmenu_right" width="10"></td>\n'
            buttons+='<td width="10"></td>\n'
            ### folder management
            buttons+='<td class="hmenu_left" width="10" height="32"></td>\n'
            buttons+='<td class="hmenu_center"><a href="/foldermgt">'
            buttons+='{}</a></td>\n'.format(self.messages['foldermgt'])
            buttons+='<td class="hmenu_right" width="10"></td>\n'
    
            buttons+='</tr>\n</table>\n'
        
        return buttons
