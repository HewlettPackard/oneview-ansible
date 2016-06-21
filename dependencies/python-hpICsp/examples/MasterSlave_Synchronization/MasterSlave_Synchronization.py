#!/usr/bin/env python3


import hpICsp
import argparse
import configparser
import os
import stat

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

#Credentials to login to master Insight Control server provisioning appliance.
parentIP = config.get('Main', 'parentIP')
parentUser = config.get('Main', 'parentUser')
parentPassword = config.get('Main', 'parentPassword')
#Parse list of slave appliance credentials.
childIPs=[x.strip() for x in config.get('Main', 'childIPs').split(',')]
childUsers=[x.strip() for x in config.get('Main', 'childUsers').split(',')]
childPasswords=[x.strip() for x in config.get('Main', 'childPasswords').split(',')]

#	Connects to a master appliance and some amount of slave appliances. Exports the master content and synchronizes it amongst the slaves.
def main():
    #Creates a connection with the appliance.
	con=hpICsp.connection(parentIP)
	#Create objects for all necessary resources.
	st=hpICsp.settings(con)

	#Login into master/parent appliance.
	credential = {'userName': parentUser, 'password': parentPassword}
	con.login(credential)

	#Export appliance content 
	bytesContent=st.export_content()
	#Write content to a zip file and set appropriate permissions.
	newFile = open ("content.zip", "wb")
	newFile.write(bytesContent)
	os.chmod("content.zip", stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
	newFile.close()
	#Logout of parent appliance.
	con.logout()
	
	#For each child appliance, create a connection, log in, import the master's content, and log out.
	for x in range(0, len(childIPs)):
		con=hpICsp.connection(childIP[x])
		credential = {'userName': childUsers[x], 'password': childPasswords[x]}
		con.login(credential)
		st=hpICsp.settings(con)
		st.import_content("content.zip")
		con.logout()

		
if __name__ == '__main__':
	import sys
	sys.exit(main())
