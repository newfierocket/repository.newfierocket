import re
import xbmc, xbmcgui, xbmcplugin
import sys
import os



mlb_host = 'mlb-ws-mf.media.mlb.com'
nhl_host = 'mf.svc.nhl.com'
old_ip 	 = '188.240.208.152'
new_ip   = '107.6.182.249'

path     = '/storage/.config/hosts.conf'



####ADD BOTH HOSTS FOR NEW INSTALLATION####
def add_both(path, mlb_host, nhl_host, new_ip):
	add = '\n' + new_ip + '   ' + nhl_host + '\n' + new_ip + '   ' + mlb_host + '\n'
	file = open(path, 'a')
	file.writelines(add)
	file.close()

	# xbmcgui.Dialog().ok ('Hosts Config', 'Host added', 'Please Restart Kodi')

	return


####EDIT HOST IF ENTRY EXISTS#####
def edit_ip(old_ip, new_ip):

	with open(path, 'r') as file:
		filedata = file.read()

	filedata = filedata.replace(old_ip, new_ip)

	with open(path, 'w') as file:
		file.write(filedata)
	
	# xbmcgui.Dialog().ok ('Hosts Config', 'Host added', 'Please Restart Kodi')
	
	return 

####ADD NHL ENTRY IF MLB EXISTS ALREADY####
def add_NHL(path, nhl_host, old_ip, new_ip):
	add = '\n' + new_ip + '   ' + nhl_host + '\n'
	file = open(path, 'a')
	file.writelines(add)
	file.close()
	
	# xbmcgui.Dialog().ok ('Hosts Config', 'Host added', 'Please Restart Kodi')

	return


####ADD MLB IF NHL ALREADY EXISTS####
def add_MLB(path, mlb_host, old_ip, new_ip):
	add = '\n' + new_ip + '   ' + mlb_host + '\n'
	file = open(path, 'a')
	file.writelines(add)
	file.close()

	# xbmcgui.Dialog().ok ('Hosts Config', 'Host added', 'Please Restart Kodi')



	return



def update_function(path, mlb_host, nhl_host, old_ip, new_ip):
	xbmcgui.Dialog().ok ('Hosts Config', 'Adding or editing Host for NHL.tv and MLB.tv', 'Please Stand By!!')

	#### Getting file Path to check if hosts exists and which to edit.####
	with open(path, 'r') as file:
		read_host = file.read()
	
	if nhl_host in read_host and mlb_host in read_host:
		# xbmcgui.Dialog().ok ('Hosts Config', 'MLB and NHL found. We will Try to update your Host File', 'Please stand by, Push OK to Continue')
		edit_ip(old_ip, new_ip)


	elif nhl_host not in read_host and mlb_host not in read_host:
		# xbmcgui.Dialog().ok ('Hosts Config', 'Adding NHL and MLB to Host, Please stand by.', 'You sexy Mother Fucker You')
		add_both(path, mlb_host, nhl_host, new_ip)

	elif mlb_host not in read_host:
		# xbmcgui.Dialog().ok ('Hosts Config', 'Found NHL adding MLB to Host, Please stand by.', 'You sexy Mother Fucker You')
		add_MLB(path, mlb_host, old_ip, new_ip)


	elif nhl_host not in read_host:
		# xbmcgui.Dialog().ok ('Hosts Config', 'Found MLB adding NHL to Host, Please stand by.', 'You sexy Mother Fucker You')
		add_NHL(path, nhl_host, old_ip, new_ip)


	else:
		xbmcgui.Dialog().ok ('Hosts Config', "Looks Like You're good to Go!!.", 'You sexy Mother Fucker You')

		pass



if __name__ == '__main__':

	if xbmcgui.Dialog().yesno ('Hosts Config', 'Would you like to wipe hosts file clean?', 'If unsure select Yes'):

		file = open(path, 'w')
		file.writelines('')
		file.close()

		update_function(path, mlb_host, nhl_host, old_ip, new_ip)
		
		xbmcgui.Dialog().ok ('Hosts Config', 'Host File Wiped and new hosts added', 'Please restart', 'You Sexy Mother Fucker You')


	else:
		update_function(path, mlb_host, nhl_host, old_ip, new_ip)
		
		

	
