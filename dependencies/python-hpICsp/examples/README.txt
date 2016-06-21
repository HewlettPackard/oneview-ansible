These samples provide an overview of what can be done with the HP ICsp library. 

 Add_Server:
	Add a server from its iLo credentials, runs a build plan to install an OS on it, run a network personalization job.
	
MasterSlave_Synchronization:
	Connects to a master appliance and some amount of slave appliances. Exports the master content and synchronizes it amongst the slaves.
	
Backup_Content:
	Exports the content of an appliance, creating a file name containing the current time.
	
In all cases, a configuration file is read in and parsed to obtain all necessary credentials and IDs.