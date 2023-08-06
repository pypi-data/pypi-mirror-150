/*Use this table to fetch meta info on the scanner station where image was recorded. Rememder to use USERT for this table*/
CREATE TABLE IF NOT EXISTS scanning_station_table (
    id SERIAL PRIMARY KEY,
	station_name TEXT UNIQUE,
	institution_name TEXT,
	institution_address TEXT,
	manufacturer_name TEXT,
    operators_name TEXT, 
    device_serialnumber TEXT,
    manufacturer_modelname TEXT,
    software_versions TEXT,
    date_of_lastcalibration TIMESTAMP WITHOUT TIME ZONE
);
