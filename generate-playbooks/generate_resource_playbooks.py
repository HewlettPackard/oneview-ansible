#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

import json
import yaml
import os
import shutil
import copy
import re
import copy
import logging
import random
import string
from builtins import input

from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[logging.FileHandler("info.log"),
              logging.StreamHandler()])

config = {
    "ip": "10.50.4.100",
    "credentials": {
        "userName": "kattumun",
        "password": "P@ssw0rd!"
    },
    "image_streamer_ip": "",
    "api_version": 800
}

class Base(object):
    """Base class to keep all the common methods"""
    def __init__(self, uri=None, oneview_client=None, write=None):
        self.oneview_client = oneview_client
        self.uri =uri
        self.write= write

        self.task_vars = {}
        self.tasks = []
        self.import_plays = []

        self.fields_to_remove = ["created", "modified", "eTag", "uri",
                                 "scopesUri", "fabricUri"]
        self.playbook_template = [{"hosts": "all",
                                   "vars": {"config": "../oneview_config.json"},
                                   "tasks": []}]
        self.root_path = "./playbooks"
        self.playbook_dir = None

    def create_path(self):
        """Creates playbooks directory"""
        if self.playbook_dir:
            self.root_path = "{}/{}".format(self.root_path, self.playbook_dir)

        if not os.path.isdir(self.root_path):
            os.makedirs(self.root_path)

    def generate_facts_name(self, name):
        """Generates playbook name from resoure name"""
        if not name:
            letters = string.ascii_lowercase
            name = ''.join(random.choice(letters) for i in range(5))
            return name
        return re.sub('\s+', '_', name).lower()

    def delete_unwanted_fields(self, data, fields=None):
        """Deletes the unwanted fields from the resource
        response to use it as playbook data
        """
        if not data:
            return

        if fields is None:
            fields = self.fields_to_remove
        else:
            fields += self.fields_to_remove

        for field in fields:
            if field in data:
                del data[field]

    def pick_fields(self, data, fields_list):
        """ """
        new_data = { field:data[field] for field in fields_list}
        return new_data

    def get_task(self, resource_module_name, task_name, data, is_fact=False):
        """ """
        if is_fact:
            task = {"name": task_name,
                    resource_module_name: {"config": "{{config}}",
                                           "name": data["name"]  }}
        else:
            task = {"name": task_name,
                    resource_module_name: {"config": "{{config}}",
                                           "state": "present",
                                           "data": data}}
        return task

    def write_playbook(self, playbook_name, path=None):
        if not self.tasks:
            return

        if not path:
            path = self.root_path

        playbook_name = self.generate_facts_name(playbook_name)
        playbook  = copy.deepcopy(self.playbook_template)

        playbook[0]["tasks"] += self.tasks
        if self.task_vars:
            playbook[0]["vars"].update(self.task_vars)

        if self.import_plays:
            # Remove duplicate imports
            self.import_plays = set(self.import_plays)
            imports = [{'import_playbook': imp} for imp in self.import_plays]
            playbook = imports + playbook

        playbook_name = playbook_name + ".yaml"
        full_path = "{}/{}".format(path, playbook_name)

        with open(full_path, 'w')  as f:
            yaml.safe_dump(playbook, f, allow_unicode=True)

        return playbook_name


class EnclosureGroup(Base):
    def __init__(self, uri, oneview_client=None, write=True):
        super(EnclosureGroup, self).__init__(uri, oneview_client, write)

        self.enclosure_groups = self.oneview_client.enclosure_groups
        self.address_ranges = self.oneview_client.id_pools_ipv4_ranges

        self.playbook_dir = "enclosure_group"
        self.request_fields = ['ambientTemperatureMode', 'enclosureCount',
                               'interconnectBayMappings', 'ipAddressingMode',
                               'ipRangeUris', 'name', 'osDeploymentSettings',
                               'powerMode']

    def generate_playbook(self):
        data = self.enclosure_groups.get_by_uri(self.uri).data
        logging.info("Generating playbooks for Enclosure Group - {}".format(data["name"]))
        enclosure_group_data = self.pick_fields(data, self.request_fields)

        range_tasks, range_facts = self.get_ip_address_range_task(
            enclosure_group_data["ipRangeUris"])
        self.tasks += range_tasks
        enclosure_group_data["ipRangeUris"] = range_facts

        for index, lig in enumerate(enclosure_group_data["interconnectBayMappings"]):
            lig_uri = lig["logicalInterconnectGroupUri"]
            lig_obj = LogicalInterconnectGroup(lig_uri, self.oneview_client)
            lig_tasks, fact, fact_variable, lig_path = lig_obj.generate_playbook()

            self.import_plays.append("../lig/{}".format(lig_path))
            self.tasks.append(fact)

            lig_fact_name = "lig_{}".format(index)
            set_fact = {'set_fact': {lig_fact_name: '{{ '+ fact_variable +'[0]}}'}}
            self.tasks.append(set_fact)

            lig["logicalInterconnectGroupUri"] = '{{ '+ lig_fact_name +'["uri"] }}'

        eg_task = self.get_task("oneview_enclosure_group",
                                enclosure_group_data["name"],
                                enclosure_group_data)
        self.tasks.append(eg_task)

        if self.write:
            #Make sure the path exists
            self.create_path()
            playbook_path = self.write_playbook(enclosure_group_data["name"])
        else:
            playbook_path = None

        eg_fact_task = self.get_task("oneview_enclosure_group_facts",
                                enclosure_group_data["name"],
                                enclosure_group_data, is_fact=True)

        return self.tasks, eg_fact_task, 'enclosure_groups', playbook_path

    def get_ip_address_range_task(self, ip_ranges):
       range_facts = []
       tasks = []

       for index, uri in enumerate(ip_ranges):
           address_range = self.address_ranges.get(uri)
           subnet_uri = address_range["subnetUri"]

           network = Network(oneview_client=self.oneview_client)
           subnet_task, subnet, fact_data = network.get_subnet_task(subnet_uri)
           tasks.append(subnet_task)

           subnet_fact_name = "ip_range_subnet_{}".format(index)
           set_fact_for_subnet = {'set_fact': {subnet_fact_name: '{{ id_pools_ipv4_subnet }}'}}
           tasks.append(set_fact_for_subnet)

           range_task, data, range_data = network.get_address_range_task(subnet_fact_name, data=address_range)
           tasks.append(range_task)

           range_fact_name = "lig_range_{}".format(index)
           set_fact_for_ip_range = {'set_fact': {range_fact_name: '{{ id_pools_ipv4_range }}'}}
           tasks.append(set_fact_for_ip_range)

           range_facts.append('{{ '+ range_fact_name +'["uri"]}}')

       return tasks, range_facts


class LogicalInterconnectGroup(Base):
    def __init__(self, uri, oneview_client=None, write=True):
        super(LogicalInterconnectGroup, self).__init__(uri, oneview_client, write)

        self.lig_client = self.oneview_client.logical_interconnect_groups
        self.sas_lig_client = self.oneview_client.sas_logical_interconnect_groups

        self.playbook_dir = "lig"

    def generate_playbook(self):
        module_name, fact_module_name, fact_var, data = self.get_lig_module_info()
        logging.info("Generating playbooks for Logical Interconnect Group - {}".format(data["name"]))
        self.delete_unwanted_fields(data)
        self.delete_unwanted_fields(data.get("ethernetSettings"))

        uplink_sets = data.get("uplinkSets")
        if uplink_sets:
            uplink_tasks = self.add_uplinksets_task(uplink_sets)
            self.tasks += uplink_tasks

        interconnect_templates = data["interconnectMapTemplate"]["interconnectMapEntryTemplates"]
        for index, template in enumerate(interconnect_templates):
            self.delete_unwanted_fields(template, fields=["logicalDownlinkUri"])
            interconnect_type_uri = template["permittedInterconnectTypeUri"]

            if not interconnect_type_uri:
                continue

            interconnect_type = InterconnectType(interconnect_type_uri,
                                                 self.oneview_client)

            it_tasks, fact_variable = interconnect_type.generate_playbook()
            self.tasks += it_tasks

            interconnect_fact_name = "interconnect_type_{}".format(index)
            set_fact = {'set_fact': {interconnect_fact_name: '{{ ' + fact_variable + '[0] }}'}}
            self.tasks.append(set_fact)

            template["permittedInterconnectTypeUri"] = '{{ '+ interconnect_fact_name +'["uri"] }}'

        task = self.get_task(module_name, data["name"], data)
        self.tasks.append(task)

        if self.write:
            #Make sure the path exists
            self.create_path()
            playbook_path = self.write_playbook(data["name"])
        else:
            playbook_path

        fact_task = self.get_task(fact_module_name,
                                  data["name"],
                                  data,
                                  is_fact=True)

        return self.tasks, fact_task, fact_var, playbook_path

    def get_lig_module_info(self):
        data = module_name = fact_module_name = fact_variable = None
        if 'sas' in self.uri:
            data = self.sas_lig_client.get_by_uri(self.uri).data
            module_name = "oneview_sas_logical_interconnect_group"
            fact_module_name = "oneview_sas_logical_interconnect_group_facts"
            fact_variable = "sas_logical_interconnect_groups"
        else:
            data = self.lig_client.get_by_uri(self.uri).data
            module_name = "oneview_logical_interconnect_group"
            fact_module_name = "oneview_logical_interconnect_group_facts"
            fact_variable = "logical_interconnect_groups"

        return module_name, fact_module_name, fact_variable, data

    def add_uplinksets_task(self, uplink_sets):
        if not uplink_sets:
            return None

        uplink_tasks = []

        for uplink_index, uplink in enumerate(uplink_sets):
            network_uri_facts = []

            for index, network in enumerate(uplink["networkUris"]):
                network = Network(network, self.oneview_client)
                tasks, fact_task, fact_var, playbook_path = network.generate_playbook()
                uplink_tasks.append(fact_task)
                self.import_plays.append("../network/{}".format(playbook_path))

                uplink_network_fact_name = "uplink_network_{}_{}".format(uplink_index, index)
                set_fact = {'set_fact': {uplink_network_fact_name: '{{ ' + fact_var + '[0] }}'}}
                uplink_tasks.append(set_fact)

                network_uri_facts.append('{{ ' + uplink_network_fact_name + '["uri"] }}')

            uplink["networkUris"] = network_uri_facts

        return uplink_tasks


class StorageSystem(Base):
    def __init__(self, uri=None, oneview_client=None, write=True):
        super(StorageSystem, self).__init__(uri, oneview_client, write)

        self.storage_system_client = self.oneview_client.storage_systems

        self.playbook_dir = "storage_system"

    def generate_playbook(self):
        system_data = self.storage_system_client.get(self.uri)
        logging.info("Generating playbooks for Storage System - {}".format(system_data["name"]))

        request_data = {"hostname" : system_data["hostname"],
                        "username" : system_data["credentials"]["username"],
                        "password" : "",
                        "family" : system_data["family"],
                        "description" : system_data["description"]}

        task = self.get_task("oneview_storage_system",
                              system_data["hostname"],
                              request_data)
        self.tasks.append(task)

        fact_task = self.get_task("oneview_storage_system",
                                  system_data["name"],
                                  system_data, is_fact=True)
        if self.write:
            #Make sure the path exists
            self.create_path()
            playbook_path = self.write_playbook(request_data["hostname"])
        else:
            playbook_path = None

        return self.tasks, fact_task, "storage_system", playbook_path


class Firmware(Base):
    def __init__(self, uri=None, oneview_client=None, write=True):
        super(Firmware, self).__init__(uri, oneview_client, write)

        self.firmware_driver_client = self.oneview_client.firmware_drivers

        self.playbook_dir = "firmware"

    def generate_playbook(self):
        try:
            firmware_data = self.firmware_driver_client.get(self.uri)
            logging.info("Generating playbooks for Firmware - {}".format(firmware_data["name"]))
        except HPOneViewException as e:
            firmware_data = None
            logging.error("Not able to fetch the firmware details : {}".format(self.uri))

        playbook_path = None
        fact_task = None
        if firmware_data:
            iso_name = firmware_data["isoFileName"]
            file_path = "./{}".format(iso_name)
            task = {"name": iso_name,
                    "oneview_firmware_bundle": {"config": "{{config}}",
                                               "file_path": file_path,
                                               "state": "present"}}
            self.tasks.append(task)

            if self.write:
                #Make sure the path exists
                self.create_path()
                playbook_path = self.write_playbook(firmware_data["name"])

            fact_task = self.get_task("oneview_firmware_driver_facts",
                                      firmware_data["name"],
                                      firmware_data,
                                      is_fact=True)

        return self.tasks, fact_task, "firmware", playbook_path


class InterconnectType(Base):
    def __init__(self, uri, oneview_client=None):
        super(InterconnectType, self).__init__(uri, oneview_client)

        self.interconnect_type_client = self.oneview_client.interconnect_types
        self.sas_interconnect_type_client = self.oneview_client.sas_interconnect_types

    def generate_playbook(self):
        task_module, fact_variable, data = self.get_module_info()
        logging.info("Generating playbooks for Interconnect Type - {}".format(data["name"]))
        task = self.get_task(task_module, "Get interconnect type",
                             data, is_fact=True)
        self.tasks.append(task)

        return self.tasks, fact_variable

    def get_module_info(self):
        client = task_module = fact_variable = data = None
        if 'sas' in self.uri:
            client = self.sas_interconnect_type_client
            task_module = "oneview_sas_interconnect_type_facts"
            fact_variable = "sas_interconnect_types"
        else:
            client = self.interconnect_type_client
            task_module = "oneview_interconnect_type_facts"
            fact_variable = "interconnect_types"

        if client:
            data = client.get_by_uri(self.uri).data

        return task_module, fact_variable, data


class OSDeploymentPlan(Base):
    def __init__(self, uri=None, oneview_client=None):
        super(OSDeploymentPlan, self).__init__(uri, oneview_client)

        self.deployment_plan_client = self.oneview_client.os_deployment_plans

    def generate_playbook(self):
        data = self.deployment_plan_client.get_by_uri(self.uri).data
        logging.info("Generating playbooks for OS Deployment Plan - {}".format(data["name"]))
        task = self.get_task("oneview_os_deployment_plan_facts",
                             data["name"],
                             {"name": data["name"]}, is_fact=True)
        self.tasks.append(task)
        fact_variable =  "os_deployment_plans"

        return self.tasks, fact_variable


class ServerHardwareType(Base):
    def __init__(self, uri=None, oneview_client=None):
        super(ServerHardwareType, self).__init__(uri, oneview_client)

        self.server_hardware_type_client = self.oneview_client.server_hardware_types

    def generate_playbook(self):
        data = self.server_hardware_type_client.get_by_uri(self.uri).data
        logging.info("Generating playbooks for Server Hardware Type - {}".format(data["name"]))
        task = self.get_task("oneview_server_hardware_type_facts",
                             data["name"],
                             {"name": data["name"]}, is_fact=True)
        self.tasks.append(task)
        fact_variable =  "server_hardware_types"

        return self.tasks, fact_variable


class Volume(Base):
    def __init__(self, uri=None, oneview_client=None, write=True):
        super(Volume, self).__init__(uri, oneview_client, write)

        self.volume_client = self.oneview_client.volumes

        self.playbook_dir = "storage_volume"

    def generate_playbook(self):
        volume_data = self.volume_client.get(self.uri)
        logging.info("Generating playbooks for Volume - {}".format(volume_data["name"]))
        task = self.get_task("oneview_volume",
                              volume_data["name"],
                              volume_data)
        self.tasks.append(task)

        fact_task = self.get_task("oneview_volume",
                                  volume_data["name"],
                                  volume_data, is_fact=True)
        if self.write:
            #Make sure the path exists
            self.create_path()
            playbook_path = self.write_playbook(volume_data["name"])
        else:
            playbook_path = None

        return self.tasks, fact_task, "volume", playbook_path


class Network(Base):
    def __init__(self, uri=None, oneview_client=None, write=True):
      super(Network, self).__init__(uri, oneview_client, write)

      self.ethernet_networks =self.oneview_client.ethernet_networks
      self.fc_networks = self.oneview_client.fc_networks
      self.subnets = self.oneview_client.id_pools_ipv4_subnets
      self.subnet_client = self.oneview_client.id_pools_ipv4_subnets
      self.address_ranges = self.oneview_client.id_pools_ipv4_ranges

      self.playbook_dir = "network"

    def add_networkset_facts(self, networkset_data):
        ethernets = networkset_data["networkUris"]
        ethernet_facts = []

        for index, uri in enumerate(ethernets):
            network = Network(uri, self.oneview_client)
            tasks, fact_task, fact_variable, playbook_path = network.generate_playbook()

            self.import_plays.append("{}".format(playbook_path))

            self.tasks.append(fact_task)
            network_fact_name = "network_{}".format(index)
            set_fact_for_network = {'set_fact': {network_fact_name: '{{ '+ fact_variable +' }}'}}
            self.tasks.append(set_fact_for_network)
            ethernet_facts.append('{{ '+ network_fact_name +'["uri"]}}')

        networkset_data["networkUris"] = ethernet_facts

    def generate_playbook(self):
      module, fact_module, fact_variable, network_data = self.get_network_module_info()

      if module == "oneview_network_set":
          self.add_networkset_facts(network_data)

      if network_data.get("subnetUri"):
        subnet_task, data, subnet_create_data = self.get_subnet_task(network_data["subnetUri"])
        self.tasks.append(subnet_task)
        range_uris = data["rangeUris"]

        for range_uri in range_uris:
          task = self.get_address_range_task("id_pools_ipv4_subnet", uri=range_uri)[0]
          self.tasks.append(task)

        network_data["subnetUri"] = '{{ id_pools_ipv4_subnet["uri"] }}'

      fact_task = None
      playbook_path = None

      if network_data:
          logging.info("Generating playbooks for Network - {}".format(network_data["name"]))
          self.fields_to_remove += ["connectionTemplateUri", "fabricUri",
                                    "managedSanUri"]
          self.delete_unwanted_fields(network_data)
          task = self.get_task(module, network_data["name"], network_data)

          self.tasks.append(task)

          if self.write:
              #Make sure the path exists
              self.create_path()
              playbook_path = self.write_playbook(network_data["name"])

          fact_task = self.get_task(fact_module,
                                    network_data["name"],
                                    network_data,
                                    is_fact=True)

      return self.tasks, fact_task, fact_variable, playbook_path

    def get_network_module_info(self):
        data = {}
        module_name = None
        facts_module_name = None
        facts_var_name = None

        if 'ethernet' in self.uri:
            try:
                data = self.oneview_client.ethernet_networks.get_by_uri(self.uri).data
            except:
                data = {}
                logging.error("Ethernet network get request error:{}".format(self.uri))
            module_name = "oneview_ethernet_network"
            facts_module_name = "oneview_ethernet_network_facts"
            fact_var_name = "ethernet_networks"

        elif 'fc-network' in self.uri:
            try:
                data = self.oneview_client.fc_networks.get_by_uri(self.uri).data
            except:
                data = {}
                logging.error("Ethernet network get request error:{}".format(self.uri))
            module_name = "oneview_fc_network"
            facts_module_name = "oneview_fc_network_facts"
            fact_var_name = "fc_networks"

        elif 'network-sets' in self.uri:
            try:
                data = self.oneview_client.network_sets.get(self.uri)
            except:
                data = {}
                logging.error("Networkset get request error:{}".format(self.uri))
            module_name = "oneview_network_set"
            facts_module_name = "oneview_network_set_facts"
            fact_var_name = "network_sets"

        return (module_name, facts_module_name, fact_var_name, data)

    def get_address_range_task(self, subnet_fact_name, uri=None, data=None):
        if not data:
            data = self.address_ranges.get(uri)
        in_fields = ["name", "type", "rangeCategory", "subnetUri",
                     "startAddress", "endAddress"]
        range_data = self.pick_fields(data, in_fields)
        range_data["subnetUri"] = '{{ ' + subnet_fact_name + '["uri"] }}'

        task = self.get_task("oneview_id_pools_ipv4_range",
                             "Create address range: name:{}".format(data["name"]),
                             range_data)

        return task, data, range_data

    def get_subnet_task(self, subnet_uri=None, data=None):
        if not data and subnet_uri:
            data = self.subnets.get(subnet_uri)

        in_fields = ["name", "type", "networkId", "subnetmask", "gateway",
                     "domain", "dnsServers"]
        subnet_data = self.pick_fields(data, in_fields)
        subnet_data["name"] = data["name"] if data.get("name") else "subnet"

        task = self.get_task("oneview_id_pools_ipv4_subnet",
                             "Create subnet: name:{}".format(data["name"]),
                             subnet_data)

        return task, data, subnet_data


class ServerProfile(Base):
    def __init__(self, uri, oneview_client, write=True):
        super(ServerProfile, self).__init__(uri, oneview_client, write)

        self.profile_client = oneview_client.server_profiles
        self.profile_template_client = oneview_client.server_profile_templates
        self.storage_template_client = oneview_client.storage_volume_templates
        self.enclosure_client = oneview_client.enclosures
        self.playbook_dir = "server_profile"
        self.existing_connections = {}

    def generate_playbook(self):
        is_template = False
        if 'template' in self.uri:
            is_template = True
            self.data = self.profile_template_client.get_by_uri(self.uri).data
            self.playbook_dir = "server_profile_template"
            self.create_path()
        else:
            self.data = self.profile_client.get_by_uri(self.uri).data
            self.create_path()

        logging.info("Generating playbooks for Server Profile/Template - {}".format(self.data["name"]))

        self.delete_unwanted_fields(data=self.data, fields=['enclosureBay'])
        self.add_connections()
        self.add_enclosure_group()
        self.add_hardware()
        self.add_enclosure()
        self.add_firmware()
        self.add_os_deployment_settings()
        self.add_hardware_type()
        self.add_storage_system()

        if is_template:
            module_name = "oneview_server_profile_template"
        else:
            module_name = "oneview_server_profile"

        task = self.get_task(module_name,
                             self.data["name"], self.data)
        self.tasks.append(task)

        if self.write:
            self.write_playbook(self.data["name"])

        return self.tasks

    def add_connections(self):
        connections = self.data["connectionSettings"]["connections"]

        for index, connection in enumerate(connections):
            fields_to_remove = ["interconnectUri", "interconnectPort", "mac",
                                "networkName"]
            self.delete_unwanted_fields(data=connection, fields=fields_to_remove)

            network = Network(connection["networkUri"], self.oneview_client)
            tasks, fact_task, fact_variable, playbook_path = network.generate_playbook()
            network_fact_name = "network_{}".format(index)

            if not fact_task:
                self.task_vars[network_fact_name] = ''
                del connection["networkUri"]
                connection["networkName"] = '{{ '+ network_fact_name +' }}'
                continue

            # Avoid duplicate network facts
            exists = self.existing_connections.get(connection["networkUri"])
            if not exists:
                self.tasks.append(fact_task)
                self.import_plays.append('../network/{}'.format(playbook_path))
                self.existing_connections[connection["networkUri"]] = network_fact_name

                set_fact_for_network = {'set_fact': {network_fact_name: '{{ '+ fact_variable +'[0] }}'}}
                self.tasks.append(set_fact_for_network)
            else:
                network_fact_name = exists

            connection["networkUri"] = '{{ '+ network_fact_name +'["uri"]}}'

    def add_enclosure_group(self):
        enclosure_group = EnclosureGroup(self.data["enclosureGroupUri"], self.oneview_client)
        tasks, fact_task, fact_variable, playbook_path = enclosure_group.generate_playbook()
        self.tasks.append(fact_task)

        self.import_plays.append('../enclosure_group/{}'.format(playbook_path))
        self.data["enclosureGroupUri"] = '{{ ' + fact_variable + '[0]["uri"] }}'

    def add_firmware(self):
        firmware_det = self.data["firmware"]
        if firmware_det and firmware_det.get("firmwareBaselineUri"):
            uri = firmware_det["firmwareBaselineUri"]
            firmware = Firmware(uri, self.oneview_client)
            tasks, fact_task, fact_variable, playbook_path = firmware.generate_playbook()

            self.import_plays.append('../firmware/{}'.format(playbook_path))
            self.tasks.append(fact_task)
            self.data["firmware"]["firmwareBaselineUri"] = '{{ ' + fact_variable + '["uri"] }}'

    def add_os_deployment_settings(self):
        os_settings = self.data["osDeploymentSettings"]

        if not os_settings:
            return

        self.delete_unwanted_fields(os_settings, fields=["osVolumeUri"])

        if  os_settings.get("osCustomAttributes"):
            os_attributes = os_settings["osCustomAttributes"]

            for index, attribute in enumerate(os_attributes):
                if 'networkuri' in attribute.get("name", ""):
                    network_uri = attribute["value"]
                    network_fact_name = "os_network_{}".format(index)

                    network = Network(network_uri, self.oneview_client)
                    tasks, fact_task, fact_variable, playbook_path = network.generate_playbook()

                    exists = self.existing_connections.get(network_uri)
                    if not exists:
                        self.import_plays.append('../network/{}'.format(playbook_path))
                        self.existing_connections[network_uri] = network_fact_name
                        self.tasks.append(fact_task)

                        set_fact_for_network = {'set_fact': {network_fact_name: '{{ '+ fact_variable +'[0] }}'}}
                        self.tasks.append(set_fact_for_network)
                    else:
                        network_fact_name = exists

                    attribute["value"] = '{{ ' + network_fact_name +'["uri"] }}'

        if os_settings.get("osDeploymentPlanUri"):
            plan_uri = os_settings["osDeploymentPlanUri"]
            del os_settings["osDeploymentPlanUri"]
            os_settings["osDeploymentPlanName"] = '{{ os_deployment_plan_name }}'

            plan = OSDeploymentPlan(plan_uri, self.oneview_client)
            data =  plan.deployment_plan_client.get_by_uri(plan_uri).data
            self.task_vars["os_deployment_plan_name"] = data["name"]

            task, fact_variable = plan.generate_playbook()

    def add_hardware_type(self):
        hardware_type_uri = self.data["serverHardwareTypeUri"]
        hardware_type = ServerHardwareType(hardware_type_uri, self.oneview_client)
        tasks, fact_variable = hardware_type.generate_playbook()
        self.tasks += tasks
        self.data["serverHardwareTypeUri"] = '{{ ' + fact_variable + '[0]["uri"] }}'

    def add_hardware(self):
        # Let auto find feature find the suitable hardware
        if self.data.get("serverHardwareUri"):
            del self.data["serverHardwareUri"]

    def add_enclosure(self):
        if self.data.get("enclosureUri"):
            enclosure_uri = self.data["enclosureUri"]
            del self.data["enclosureUri"]

            self.data["enclosureName"] = '{{ enclosure_name }}'
            data = self.enclosure_client.get_by_uri(enclosure_uri).data
            self.task_vars["enclosure_name"] = data["name"]

    def add_storage_system(self):
        san_storage = self.data["sanStorage"]
        volume_attachments = san_storage.get("volumeAttachments")
        storage_systems = []

        if volume_attachments:
            for index, attachment in enumerate(volume_attachments):
                self.delete_unwanted_fields(attachment, fields=["associatedTemplateAttachmentId"])
                volume = attachment["volume"]
                volume_uri = attachment["volumeUri"]
                storage_system_uri = attachment["volumeStorageSystemUri"]

                if storage_system_uri and storage_system_uri not in storage_systems:
                    system = StorageSystem(storage_system_uri, self.oneview_client)
                    tasks, fact_task, fact_variable, playbook_path = system.generate_playbook()

                    system_fact_name = "storage_system_{}".format(index)
                    del attachment["volumeStorageSystemUri"]
                    self.task_vars[system_fact_name] = ''
                    attachment["volumeStorageSystemName"] = "{{" + system_fact_name + "}}"

                if volume_uri:
                    volume = Volume(volume_uri, self.oneview_client)
                    tasks, fact_task, fact_variable, playbook_path = volume.generate_playbook()

                    volume_fact_name = "storage_volume_{}".format(index)
                    del attachment["volumeUri"]
                    self.task_vars[volume_fact_name] = ''
                    attachment["volumeName"] = "{{" + volume_fact_name + "}}"

                elif volume:
                    if volume.get("properties") and volume["properties"].get("storagePoolUri"):
                        del volume["properties"]["storagePoolUri"]
                        storage_pool_name = "storage_pool_name_{}".format(index)
                        self.task_vars[storage_pool_name] = ''
                        volume["properties"]["storagePoolName"] = "{{ "+ storage_pool_name + " }}"

                    if volume.get("templateUri"):
                        del volume["templateUri"]
                        volume_template_name = "volume_template_name_{}".format(index)
                        self.task_vars[volume_template_name] = ''
                        volume["templateName"] = "{{" + volume_template_name + "}}"


class ExportOVResources(object):
    def __init__(self, oneview_client=None):
        self.oneview_client = oneview_client

    def ethernet(self):
        ethernets = self.oneview_client.ethernet_networks.get_all()
        user_input, data = select_resource(ethernets, "Ethernets")

        for number in user_input:
            ethernet = Network(ethernets[number-1]["uri"],
                               oneview_client=self.oneview_client)
            ethernet.generate_playbook()

    def network_set(self):
        network_sets = self.oneview_client.network_sets.get_all()
        user_input, data = select_resource(network_sets, "Network Sets")

        for number in user_input:
            network_set = Network(network_sets[number-1]["uri"],
                                  oneview_client=self.oneview_client)
            network_set.generate_playbook()

    def fc_network(self):
        fcs = self.oneview_client.fc_networks.get_all()
        user_input, data = select_resource(fcs, "FC networks")

        for number in user_input:
            fc = Network(fcs[number-1]["uri"],
                         oneview_client=self.oneview_client)
            fc.generate_playbook()

    def enclosure_group(self):
        egs = self.oneview_client.enclosure_groups.get_all()
        user_input, data = select_resource(egs, "Enclosure Groups")

        for number in user_input:
            eg = EnclosureGroup(egs[number-1]["uri"],
                                oneview_client=self.oneview_client)
            eg.generate_playbook()

    def logical_interconnect_group(self):
        ligs = self.oneview_client.logical_interconnect_groups.get_all()
        user_input, data = select_resource(ligs, "Logical Interconnect Groups")

        for number in user_input:
            lig = LogicalInterconnectGroup(ligs[number-1]["uri"],
                                oneview_client=self.oneview_client)
            lig.generate_playbook()

    def firmware(self):
        firmwares = self.oneview_client.firmware_drivers.get_all()
        user_input, data = select_resource(firmwares, "Firmware")

        for number in user_input:
            firmware = Firmware(firmwares[number-1]["uri"],
                                oneview_client=self.oneview_client)
            firmware.generate_playbook()

    def storage_system(self):
        storage_systems = self.oneview_client.storage_systems.get_all()
        user_input, data = select_resource(storage_systems, "Storage Systems")

        for number in user_input:
            system = StorageSystem(storage_systems[number-1]["uri"],
                                   oneview_client=self.oneview_client)
            system.generate_playbook()

    def server_profile(self):
        profiles = self.oneview_client.server_profiles.get_all()
        user_input, data = select_resource(profiles, "Server Profile")

        for number in user_input:
            server_profile = ServerProfile(profiles[number-1]["uri"],
                                           oneview_client=self.oneview_client)
            server_profile.generate_playbook()

    def server_profile_template(self):
        templates = self.oneview_client.server_profile_templates.get_all()
        user_input, data = select_resource(templates, "Server Profiles Templates")

        for number in user_input:
            template = ServerProfile(templates[number-1]["uri"],
                                     oneview_client=self.oneview_client)
            template.generate_playbook()


def select_resource(resources, name):
        """Method to collect user input for resource selection"""
        user_input = []
        selector = {0: 'all'}
        print("\n###### {} ######". format(name.capitalize()))

        for index, resource in enumerate(resources):
          selector[index+1] =  resource

        if len(selector) > 1:
          for key, resource in selector.items():
            resource_name = "all" if resource == "all" else resource["name"]
            print("{}:{}".format(key, resource_name))

          while True:
            user_input = input("Select the number of {} from the above list(" \
                "Type comma seperated numbers for multiple resources):".format(name))

            if user_input:
              try:
                user_input = [int(i) for i in user_input.split(',')]
              except ValueError:
                print("\nYou have entered an invalid value")
                continue

              if set(user_input).issubset(set(selector.keys())):
                break
              else:
                print("\nInvalid selection")

            else:
                print("\nProvide a valid number")
        else:
          print("\nSelected resources are not available")

        if 0 in user_input:
          del(selector[0])
          user_input = selector.keys()

        return user_input, selector


if __name__ == '__main__':
    oneview_client = OneViewClient(config)
    export = ExportOVResources(oneview_client)

    resources = [{"name": "Networks", "methods":[export.fc_network, export.ethernet]},
                 {"name": "Network Sets", "methods": [export.network_set]},
                 {"name": "Logical Interconnect Groups", "methods": [export.logical_interconnect_group]},
                 {"name": "Enclosure Groups", "methods": [export.enclosure_group]},
                 {"name": "Storage Systems", "methods": [export.storage_system]},
                 {"name": "Firmwares", "methods": [export.firmware]},
                 {"name": "Server Profile Templates", "methods": [export.server_profile_template]},
                 {"name": "Server Profiles", "methods": [export.server_profile]}]

    user_input, data = select_resource(resources, "resources")
    for number in user_input:
        for method in resources[number-1]["methods"]:
            method()
