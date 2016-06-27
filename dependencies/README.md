# Dependencies

## python-hpICsp

The library provides a pure Python interface to the HPE Insight Control server provisioning RESTful API.

It is a modified copy of https://github.com/HewlettPackard/python-hpICsp, with some specific changes for the `hpe_icsp` module.

### Installation
From source

```
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
$ cd dependencies/python-hpICsp
$ python setup.py install --user  # to install in the user directory (~/.local)
$ sudo python setup.py install    # to install globally
```
