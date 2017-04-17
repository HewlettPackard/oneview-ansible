#!/usr/bin/env python3

###
# (C) Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

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
