-- nyc_taxi.vendor definition
-- Drop table
-- DROP TABLE nyc_taxi.vendor;
CREATE TABLE nyc_taxi.vendor (
	vendor_id text NULL,
	"name" text NULL,
	address text NULL,
	city text NULL,
	state text NULL,
	zip int8 NULL,
	country text NULL,
	contact text NULL,
	"current" text NULL
);