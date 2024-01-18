```

CREATE TABLE representitives
CREATE TABLE customers
CREATE TABLE orders
CREATE TABLE catalog
CREATE TABLE vendor

USE representitives

CREATE TABLE representitive_information (
	id int(64) primary_key auto_update,
	name	varchar(255),
	email	varchar(255),
	address	varchar(255),
	phone	varchar(16),
	active	boolean);

CREATE TABLE meetings (
	id	int(64) primary_key auto_update,
	when	date,
	customer_id	int(16),
	complete	bool,
	description	varchar(1024), 
	follow_up	bool,
	follow_up_when	date);

CREATE TABLE sales_and_satisfaction (
	id 	int(64),
	total_sold	int(64),
	num_transactions	int(64),
	average_customer_score	int(16),
	total_meetings	int(16),
	total_deals		int(16),
	total_income	int(64));


USE orders

CREATE TABLE pending_orders (
	order_id int(16) auto_update primary_key,
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
	description		varchar(255)
	);

CREATE TABLE order_history (
	order_id int(64),
	customer_id int(64),
	vendor_id	int(64),
	salesperson_id	int(64),
	items_ordered	varchar(255),
	total_price		int(64),
	total_collected	int(64),
	customer_satisfaction_level	int(16)
	);


USE customers

CREATE TABLE customer_information (
	customer_id int(16) primary_key auto_update,
	name varchar(255),
	email varchar(255),
	phone	varchar(16),
	address varchar(255),
	satisfaction_level(255),
	customer_since date,
	total_spent int(64),
	pending_orders varchar(255),
	historical_orders(255)
	);

CREATE TABLE customer_interactions (
	customer_id	int(16),
	method	varchar(255),
	salesperson_id int(16),
	description varchar(255)
	);

CREATE TABLE customer_orders (
	order_id int(16),
	customer_id int(16),
	complete bool,
	products varchar(255),
	price int(64),
	satisfaction int(64)
	);



USE catalog

CREATE TABLE products (
	id int(64) primary_key auto_update,
	name	varchar(255),
	description varchar(1024),
	unit_price	int(64),
	photograph blob,
	vendor_id int(16),
	price int(64)
);
```