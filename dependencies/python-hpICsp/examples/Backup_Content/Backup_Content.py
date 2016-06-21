#!/usr/bin/env python3


import hpICsp
import argparse
import configparser
import os
import stat
import time

#Retrieve various credentials from a configuration file.
parser = argparse.ArgumentParser(description='Process config file')
parser.add_argument('--file',
                    dest='configFile',
                    type=str,
                    help='Config File',
                    default='config.cfg')
args = parser.parse_args()
config = configparser.RawConfigParser()
config.read(args.configFile)

#Credentials to login to appliance.
applianceIP = config.get('Main', 'applianceIP')
applianceUser= config.get('Main', 'applianceUser')
appliancePassword = config.get('Main', 'appliancePassword')

#	Exports the content of an appliance, creating a file name containing the current time.
def main():
    #Creates a connection with the appliance.
	con=hpICsp.connection(applianceIP)
	#Create objects for all necessary resources.
	st=hpICsp.settings(con)

	#Login using parsed login information
	credential = {'userName': applianceUser, 'password': appliancePassword}
	con.login(credential)
	
	#Export appliance content 
	bytesContent=st.export_content()
	
	#Write content to zip file containing current time.
	name=("Backup " + time.strftime("%c") + ".zip")
	newFile = open (name, "wb")
	newFile.write(bytesContent)
	os.chmod(name, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
	newFile.close()
	
	#Logout of appliance
	con.logout()
		
if __name__ == '__main__':
	import sys
	sys.exit(main())
