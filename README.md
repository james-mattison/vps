```
                                               _   __   ___    ____
                                              | | / /  / _ \  / __/
                                              | |/ /  / ___/ _\ \  
                                              |___/  /_/    /___/  
                                                                  
                                            Vendor Product Services
```

![process diagram](etc/diagram.png)

## Vendor Product Services (VPS) 

This repository contains the development version of the VPS Sales Management System.

This system provides a lightweight and complete product management system that can be extended with custom, dynamically loaded modules.

**The code in this repository is pre-alpha, and will be subject to change. This repository is likely to be deprecated in the near future.**


## Components

This project is composed of three components:

### 1. vps-lib

This consists of a series of interfaces to manage and manipulate customers, orders, products, and empoyees.

### 2. vps-portal

An internal management interface that allows the customer to add, remove, or otherwise manipulate products, orders, customers, and employees.

### 3. vps-subloader

A dynamic module loading interface allowing the user to extend the functionality of the `vps-core`.

Each module provides a function that allows the user to extend the `vps-core` in whatever way he/she sees fit. The purpose of the `vps-subloader` is to permit a high level of customization in the management of data, 
as well as basic interfaces for using that data in a variety of ways (eg, to send SMS messages, provide metrics, process payments, etc.)

## Modules

What makes this system special is the highly extensible usage of **modules**, components that provide additional functionality to the `vps-core` and `vps-portal`. Modules are intended to be added or removed at will 
depending on customer requirements.

Each module is loaded into the running `vps-core` via the `subloader`.

By default, the following modules are loaded:
- `send_sms` - a module to send SMS messages
- `send_email` - a module to send emails
- `remind` - a module to schedule tasks, such as recurring orders or email/SMS reminders
- `reporting` - a module to provide basic business intelligence based on user-provided data


## Configuration

### 1. Bootstrapping the Host

Bootstrapping the VPS host involves provisioning a virtual private server with the cloud houst of your choice. For testing and configuration purposes, this project has used [vultr]("http://vultr.com"). 

1. Set up a base Ubuntu 22.04 (or latest LTS) VM
2. Copy your ssh key to root's `authorized_keys`
3. Execute `python3 bin/install.py`

### 2. Loading the DB Schema

1. SSH to the VPS VM
2. `cd /vps/db`
3. `./load-schema.sh`

### 3. (Optional) Adding test customer data

1. SSH to the VPS VM
2. `cd /vps`
3. `. venv/bin/activate`
4. `python3 db/generate_test_customers.py` to load 25 randomly
generated test customers into the DB.

### 4. Start the VPS system

1. `vpsctl start`

