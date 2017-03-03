# Ansible for HPE OneView and Image Streamer

This repository contains a collection of sample ansible playbooks for using HPE Image Streamer to deploy, update and revert Golden Images to OS boot/run volumes for HPE Synergy compute module servers.

## Requirements

* [Ansible >= 2.0.2](http://docs.ansible.com/ansible/intro_installation.html)
* Linux host (Ubuntu, CentOS, etc)
* [HPE OneView Python SDK](https://github.com/HewlettPackard/python-hpOneView#installation)
* Python >= 2.7.9
* [Ansible modules for HPE OneView](https://github.com/HewlettPackard/oneview-ansible)

If you are new to ansible, here's an interesting resource to get started: [Introduction to Ansible webinar  series](https://www.ansible.com/webinars-training/introduction-to-ansible)

## Setup

   [OneView-Ansible setup](https://github.com/HewlettPackard/oneview-ansible#setup)

   
###Project structure
The ansible playbooks are organized in folders to promote modularity and readability.

```
| - group_vars
	| - group.yml
  - host_vars
     | - host1.yml
      -  host2.yml
      -  host3.yml
  - tasks
     | - task1.yml
       - task2.yml
       - task3.yml
  - hosts
    playbook1.yml
    playbook2.yml
    playbook3.yml
  
```

**group_vars** - This folder contains all information for a group of hosts. In a typical server deployment scenario, the deployment network, server hardware and enclosure group would be the same across similar hosts, the information can be captured and stored here. This can be referenced later as variables while writing playbooks.

**host_vars** - This folder contains all host specific information.

**tasks** - This folder may contain tasks which can be reused across different playbooks to promote modularity or independent tasks for each playbook

**hosts** - It is a text file to store inventory related information.

**playbook<1..n>.yml** - This is the entry point of ansible tasks, and this is where we tell ansible of what we want to achieve. Typical examples may include creation of server profile, powering on all server hardwares or updating firmware across all server hardwares.

##Usage
To run the playbooks,
```$ ansible-playbook -i /path/to/playbookdirectory/playbook.yml```



## Example

This example shows how ansible can be leveraged for complex automation tasks like creation of server profiles and updating them. In this example we have shown how to get a list of deployment plans and their OS custom attributes and use them for server profile creation.

***1) Retrieve all deployment plans and their OS custom attributes***

```yaml
- hosts: all
  gather_facts: no
  vars:
    config: "{{ playbook_dir }}/oneview_config.json"
    destination_path: "{{ playbook_dir }}/vars"
    deploymentplans_info_directory: "{{ playbook_dir}}/data/deployment-plans"
  tasks:
    - name: Create a folder to store deployment plan related information
      file: path="{{ deploymentplans_info_directory }}" state=directory
      delegate_to: localhost
      
    - name: Gather facts about all OS Deployment Plans
      oneview_os_deployment_plan_facts:
        config :  '{{ config }}'
      delegate_to: localhost

    - name: Gather facts about each OS Deployment Plan Custom Attributes
      oneview_os_deployment_plan_facts:
        config: '{{ config }}'
        name : '{{ item.name }}'
        options:
          - osCustomAttributesForServerProfile
      with_items:
          - "{{ os_deployment_plans }}"
      register: dp_facts
      delegate_to: localhost

    - name: Export each deployment plan's OS custom attributes to deploymentPlanName.yml
      copy:
        content="{{ item.os_deployment_plan_custom_attributes | to_nice_yaml }}"
        dest="{{ deploymentplans_info_directory }}/{{ item.os_deployment_plans.0.name }}.yml"
      with_items:thaty yo
       - "{{ dp_facts.results | map(attribute='ansible_facts') | list  }}"
      delegate_to: localhost

```

​	This playbook will retrieve all deployment plans in image streamer and store them at  ```/data/deployment-plans/<deploymentplanname.yml> ``` . The deploymentplanname.yml file generated would have oscustom attributes listed in the following fashion,

```yaml
os_custom_attributes_for_server_profile:
- name: Hostname
  value: 'localhost'
- name: 'ip_address'
  value: '10.10.7.1' 
```

***2) Create a server profile using a deployment plan***

```yaml

- name: Deploy RHEL 7.2 servers
  hosts: all
  gather_facts: no
  vars:
    - config: "{{ playbook_dir }}/oneview_config.json"
    - deployment_plan_name: 'install-RHEL7.2'    

  tasks:
    - name : "Create server profile with deployment plan {{ deployment_plan_name }}"
      delegate_to: localhost
      oneview_server_profile:
        config: "{{ config }}"
        data:
            name: "{{ inventory_hostname }}"
            server_template: "webserver-template"                                            
            osDeploymentSettings:
              osDeploymentPlanName: "{{ deployment_plan_name }}"
              osCustomAttributes:
                - name: Hostname
                  value: 'localhost'
                - name: 'ip_address'
                  value: '10.10.7.1' 

```

This playbook shows how to create a server profile using a deployment plan with the help of image streamer. The example shown above shows server profile creation with a template already created. The template should have all network connections defined and server hardware type specified. Additionally the vars section contains the deployment_plan_name with which the profile will be created.

The playbook expects you to specify a deployment plan name and the OS custom attributes that you may want to be personalized during profile creation.If you want the osCustomAttributes for a deployment plan name, you could use the example1 to retrive OS custom attributes for a deployment plan and use the infomation under ```osCustomAttributes``` 



***3) Update a server profile***

```yaml
- name: Update RHEL 7.2 servers
  hosts: all
  gather_facts: no
  vars:
    - config: "{{ playbook_dir }}/oneview_config.json"
    - deployment_plan_name: 'update-RHEL7.2'    

  tasks:
    - name : "Update server profile with deployment plan {{ deployment_plan_name }}"
      delegate_to: localhost
      oneview_server_profile:
        config: "{{ config }}"
        state: "present"
        data:
            name: "{{ inventory_hostname }}"
            server_template: "webserver-template"                                            
            osDeploymentSettings:
              osDeploymentPlanName: "{{ deployment_plan_name }}"
              osCustomAttributes:
                - name: Hostname
                  value: 'mydevmachine'
                - name: 'ip_address'
                  value: '10.10.7.2' 

```

This playbook shows how to update a server profile with a new deployment plan and new OS custom attributes. 


***4) Rolling updates of server profile***

```yaml
- name: Update RHEL 7.2 servers
  hosts: all
  gather_facts: no
  serial: 1
  vars:
    - config: "{{ playbook_dir }}/oneview_config.json"
    - deployment_plan_name: 'update-RHEL7.2'    

  tasks:
    - name : "Update server profile with deployment plan {{ deployment_plan_name }}"
      delegate_to: localhost
      oneview_server_profile:
        config: "{{ config }}"
        state: "present"
        data:
            name: "{{ inventory_hostname }}"
            server_template: "webserver-template"                                            
            osDeploymentSettings:
              osDeploymentPlanName: "{{ deployment_plan_name }}"
              osCustomAttributes:
                - name: Hostname
                  value: 'mydevmachine'
                - name: 'ip_address'
                  value: '10.10.7.2' 

```

This playbook shows how to perform rolling updates of server profiles. The playbook expects a variable called serial, if its set to 1, the updates of server profile are performed serially. The typical use cases include updates of servers under a load balancer where the service is still available even when servers are performing updates. 

 
