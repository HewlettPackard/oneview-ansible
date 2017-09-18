## Server profile with boot from SAN and server profile & volume migration

This demo is composed by 5 steps, each one associated with a playbook, that should be executed in the specified order: 

###  [Step 1 - Create server profile with boot from SAN](step_1_create_server_profile_boot_from_SAN.yml)
This playbook exemplifies how to create a server profile with boot from SAN (3PAR) without using a template. It performs 2 tasks:
1. The server profile 'profile_san' is created (if not already present) and assigned to server hardware in bay 1. You can check all parameters, including those related to the server hardware and those related to the storage as SAN connections and volume attachment. The volume must be ready to use. 
2. The server hardware is powered on.

### [Step 2 - Add an extra data volume attachment to the existing server profile](step_2_based_on_server_profile_boot_from_SAN_add_another_volume.yml)
This playbook exemplifies how to add an extra volume attachment to the existing server profile 'profile_san'. It performs only 1 task:
1. Updates server profile 'profile_san' (created on step 1) adding a new volume attachment identified by id 2. When this task is executed, the additional volume becomes available to the operating system.

### [Step 3 - Create server profile based on a server profile template](step_3_create_server_profile_from_template.yml)
This playbook exemplifies how to create a server profile using a server profile template. It performs 2 tasks:
1. The server profile 'profile_i3s' is created (if not already present) and assigned to server hardware in bay 12. In this case, all settings were configured in the template, including network connections and OS deployment plan to use Image Streamer. 
2. The server hardware is powered on.

### [Step 4 - Migrate a data volume to another server profile](step_4_migrate_data_volume.yml)
This playbook exemplifies how to migrate a data volume from one server profile to another. It performs 2 tasks:
1. Updates server profile 'profile_san' to match its original state on step 1, removing the data volume identified by id 2.
2. Updates server profile 'profile_i3s' inserting the data volume removed in the previous task. The connectionId used by the storage paths needs to be updated to match the SAN connections. In this case, the SAN connection ids in the server profile template were 4 and 5. 

### [Step 5 - Migrate server profile to another server hardware](step_5_migrate_server_profile.yml)
This playbook exemplifies how to migrate a server profile from one server hardware to another. For this use case only one task must be executed:
1. The server profile 'profile_san' is updated specifying the new server hardware. This task was copied from step 1 and just the server hardware name was changed. 
 
