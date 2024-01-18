```
                                __      _______   _____
                                \ \    / /  __ \ / ____|
                                 \ \  / /| |__) | (___
                                  \ \/ / |  ___/ \___ \
                                   \  /  | |     ____) |
                                    \/   |_|    |_____/
                               Vendor  Product  Services
```

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

By default, the following modules are loaded:
- `send_sms` - a module to send SMS messages
- `send_email` - a module to send emails
- `remind` - a module to schedule tasks, such as recurring orders or email/SMS reminders
- `reporting` - a module to provide basic business intelligence based on user-provided data

