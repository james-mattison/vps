
CREATE DATABASE representitives;
CREATE DATABASE customers;
CREATE DATABASE orders;
CREATE DATABASE catalog;
CREATE DATABASE vendor;


/*
   DB: representitives
   This database contains information about the people selling this product.
   Should contain information about the salesperson, their scheduled meetings,
   their customer satisfaction level,
 */
USE representitives;
CREATE TABLE representitive_information (
	id int(64) not null auto_increment,
	name	varchar(255),
	email	varchar(255),
	address	varchar(255),
	phone	varchar(16),
	active	boolean,
	primary key(id));

CREATE TABLE meetings (
	salesperson_id	int(64) not null auto_increment,
	meeting_date	date,
	customer_id	int(16),
	complete	bool,
	description	varchar(1024),
	follow_up	bool,
	follow_up_when	date,
	primary key (salesperson_id));

CREATE TABLE sales_and_satisfaction (
	salesperson_id 	int(64) not null,
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
	customer_since date,
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
	order_id int(16) not null,
	customer_id int(16),
	complete bool,
	products varchar(255),
	price int(64),
	satisfaction int(64)
	);


/*
 DB: catalog
 Information about the products available, to be used by the web portal.
 */

USE catalog;

CREATE TABLE products (
	product_id int(64) auto_increment,
	name	varchar(255),
	description varchar(1024),
	unit_price	int(64),
	photograph blob,
	vendor_id int(16),
	price int(64),
	primary key (product_id)
);


/*
 DB: vendor
 Information about specific vendors
 */
USE vendor;

CREATE TABLE vendor (
    vendor_id   int(64) auto_increment,
    name    varchar(255),
    email   varchar(255),
    phone   varchar(16),
    address varchar(255),
    contact_person  varchar(255),
    customer_since  date,
    total_spent     int(64),
    total_orders    int(64),
    primary key (vendor_id)
)