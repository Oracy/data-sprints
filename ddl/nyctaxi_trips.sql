-- nyc_taxi.nyctaxi_trips definition
-- Drop table
-- DROP TABLE nyc_taxi.nyctaxi_trips;
CREATE TABLE nyc_taxi.nyctaxi_trips (
	vendor_id text NULL,
	pickup_datetime text NULL,
	dropoff_datetime text NULL,
	passenger_count int8 NULL,
	trip_distance float8 NULL,
	pickup_longitude float8 NULL,
	pickup_latitude float8 NULL,
	rate_code float8 NULL,
	store_and_fwd_flag float8 NULL,
	dropoff_longitude float8 NULL,
	dropoff_latitude float8 NULL,
	payment_type text NULL,
	fare_amount float8 NULL,
	surcharge float8 NULL,
	tip_amount float8 NULL,
	tolls_amount float8 NULL,
	total_amount float8 NULL,
	weekday int8 NULL,
	diff_trip_seconds int8 NULL
);