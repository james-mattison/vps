CREATE DATABASE customers;
CREATE DATABASE products;
CREATE DATABASE employees;
CREATE DATABASE orders;
CREATE DATABASE additional_info;
CREATE DATABASE interfacing_methods;
CREATE DATABASE config;


/*
   DB: employees
   This database contains information about the people selling this product.
   Should contain information about the salesperson, their scheduled meetings,
   their customer satisfaction level,
 */
USE employees;
CREATE TABLE representitive_information (
	id int(4) not null auto_increment,
	name	varchar(255),
	email	varchar(255),
	address	varchar(255),
	phone	varchar(16),
	active	boolean,
	primary key(id));

CREATE TABLE meetings (
	salesperson_id	int(4) not null auto_increment,
	meeting_date	int(4),
	customer_id	int(16),
	complete	bool,
	description	varchar(1024),
	follow_up	bool,
	follow_up_when	int(4),
	primary key (salesperson_id));

CREATE TABLE sales_and_satisfaction (
	salesperson_id 	int(4) not null,
	total_sold	int(64),
	num_transactions	int(64),
	average_customer_score	int(16),
	total_meetings	int(16),
	total_deals		int(16),
	total_income	int(64),
	primary key (salesperson_id));


/*
 DB: orders
 Contains information about pending orders for products, placed by customers
 and then completed orders
 */
USE orders;

CREATE TABLE pending_orders (
	order_id int(16) not null auto_increment,
	customer_id	int(16),
	salesperson_id	int(16),
	vendor_id	int(16),
	when_placed	date,
	current_status	varchar(255),
	recipient_address	varchar(255),
	total_price		int(64),
	total_received	int(64),
	total_outlay	int(64),
	shipping_price	int(64),
	num_items		int(64),
	description		varchar(255),
	primary key (order_id)
	);

CREATE TABLE order_history (
	order_id int(64) not null,
	customer_id int(64),
	vendor_id	int(64),
	salesperson_id	int(64),
	items_ordered	varchar(255),
	total_price		int(64),
	total_collected	int(64),
	customer_satisfaction_level	int(16),
	primary key (order_id)
	);


/*
 DB: customers
 Contains information about the customer themselves, how our interactions have gone with this
 customer, and the orders placed by this customer
 */
USE customers;

CREATE TABLE customer_information (
	customer_id int(16) auto_increment,
	name varchar(255),
	email varchar(255),
	phone	varchar(16),
	address varchar(255),
	satisfaction_level varchar(255),
	customer_since int(4),
	total_spent int(64),
	pending_orders varchar(255),
	historical_orders varchar(255),
	primary key (customer_id)
	);

CREATE TABLE customer_interactions (
	customer_id	int(16),
	method	varchar(255),
	salesperson_id int(16),
	description varchar(255)
);

CREATE TABLE customer_orders (
	order_id int(16) not null auto_increment,
	customer_id int(16),
	complete bool,
	products varchar(255),
	price int(64),
	satisfaction int(4),
	primary key (order_id)
	);


/*
 DB: catalog
 Information about the products available, to be used by the web portal.
 */

USE products;

CREATE TABLE products (
	product_id int(64) auto_increment,
	name	varchar(255),
	description varchar(1024),
	unit_price	int(64),
	photograph blob,
	vendor_id int(16),
	price int(64),
	in_stock    int(4),
	primary key (product_id)
);


/*
 DB: vendor
 Information about our specific customer.
 */
USE config;

CREATE TABLE vendor (
    vendor_id   int(64) auto_increment,
    name    varchar(255),
    email   varchar(255),
    phone   varchar(16),
    address varchar(255),
    contact_person  varchar(255),
    customer_since  int(4),
    total_spent     int(64),
    total_orders    int(64),
    primary key (vendor_id)
);

CREATE TABLE modules (
    module_id   int(16),
    name        varchar(255),
    enabled     boolean,
    price       float,
    unique key (name)
);

CREATE TABLE invoice (
    invoice_id  int(16) auto_increment,
    price       float,
    services    varchar(255),
    due_date    int(4),
    primary key (invoice_id)
);

CREATE TABLE service_auth (
    service_name  varchar(255)  not null,
    username    varchar(255),
    password    varchar(255),
    token       varchar(255) default null
);

CREATE TABLE portal_aliases (
    key_name varchar(255),
    value varchar(255)
);

CREATE TABLE portal_users (
    user_id int not null,
    username varchar(255),
    password varchar(255),
    email   varchar(255)
);

CREATE TABLE license (
    customer_id int(4) not null,
    expiration  int(4) not null,
    enabled bool not null,
    portal_enabled  bool not null,
    portal_url  varchar(255) not null,
    certificate varchar(255) not null,
    modules_enabled varchar(255),
    server_url  varchar(255),
    server_addr varchar(24)
);

use interfacing_methods;

CREATE TABLE interfacing_methods (
    id  int(4) not null auto_increment,
    name    varchar(255) not null,
    enabled bool,
    primary key (id)
);

use additional_info;

CREATE TABLE module_info (
    module_id   int(4) not null,
    info_key    varchar(255),
    info_value  varchar(255)
);

CREATE TABLE order_info (
    order_id    int(4) not null,
    info_key    varchar(255),
    info_value  varchar(255)
);


/* insert into interfacing_methods.interfacing_methods
   - phone
   - sms
   - email
   - tablet
   - portal
 */

USE interfacing_methods;
INSERT INTO interfacing_methods (id, name, enabled) VALUES (1, 'phone', 0);
INSERT INTO interfacing_methods (id, name, enabled) VALUES (2, 'sms', 0);
INSERT INTO interfacing_methods (id, name, enabled) VALUES (3, 'email', 0);
INSERT INTO interfacing_methods (id, name, enabled) VALUES (4, 'tablet', 0);
INSERT INTO interfacing_methods (id, name, enabled) VALUES (5, 'portal', 0);

USE config;
INSERT INTO modules (module_id, name, enabled, price) VALUES (0, 'send_sms', 1, 0.0);
INSERT INTO modules (module_id, name, enabled, price) VALUES (1, 'send_email', 1, 0.0);
INSERT INTO modules (module_id, name, enabled, price) VALUES (2, 'reporting', 1, 0.0);
INSERT INTO modules (module_id, name, enabled, price) VALUES (3, 'remind', 1, 0.0);


