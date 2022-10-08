import re
import xbmc, xbmcgui, xbmcplugin
import sys
import os
import socket



mlb_host 	 = 'mlb-ws-mf.media.mlb.com'
nhl_host 	 = 'mf.svc.nhl.com'
mlb_playback = 'playback.svcs.mlb.com'
host_name 	 = 'nhl.freegamez.ga'
update_ip = ''
regex = r'(\d.*).*'
readfile = []
updatedfile = []
extra_entries = []

path     = '/storage/.config/hosts.conf'


def check(updatedfile, extra_entries):
	check_string = ''
	for line in updatedfile:
		check_string += line

	if mlb_host and nhl_host and mlb_playback in check_string:
		with open(path, 'w') as f:
			f.writelines(updatedfile)
		return
	else:
		extra_string = ''
		for line in extra_entries:
			extra_string += line

		with open(path, 'w') as f:
			f.writelines(update_ip + '     ' + mlb_playback + '\n' +
						 update_ip + '     ' + mlb_host + '\n' +
						 update_ip + '     ' + nhl_host + '\n' +
						 extra_string + '\n')

def updateIP(hostName, line):
	found = re.match(regex + hostName, line).group(1)
	if found == update_ip:
		updatedfile.append(line + '\n')
	else:
		updatedfile.append(update_ip + '     ' + hostName + '\n')

# def add_entries(path, mlb_host, nhl_host, mlb_playback, host_name):
	
# 	add = '\n' + update_ip + '   ' + nhl_host + '\n' + update_ip + '   ' + mlb_host + '\n' + update_ip + '   ' + mlb_playback + '\n'
# 	file = open(path, 'a')
# 	file.writelines(add)
# 	file.close()


if __name__ == '__main__':

	if xbmcgui.Dialog().yesno ('Hosts Config', 'This will wipe or update host file and edit it to work with LazyMan', 'Are you sure?'):
		
		update_ip = "128.199.46.251" #socket.gethostbyname(host_name)
		
		with open(path) as f:
			for line in f:
				readfile.append(line)

		for line in readfile:
			if re.match(regex + mlb_host, line):
				updateIP(mlb_host, line)	
			elif re.match(regex + mlb_playback, line):
				updateIP(mlb_playback, line)
			elif re.match(regex + nhl_host, line):
				updateIP(nhl_host, line)
			else:
				extra_entries.append(line)
				updatedfile.append(line)

		check(updatedfile, extra_entries)
		
		# add_entries(path, mlb_host, nhl_host, mlb_playback, host_name)

		
		xbmcgui.Dialog().ok ('Hosts Config', 'Host File Wiped and new hosts added', 'Please restart', 'You Sexy Mother Fucker You')


	else:
		pass