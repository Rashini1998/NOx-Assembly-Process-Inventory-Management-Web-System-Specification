create database InventoryManagement;
Use InventoryManagement;
drop database InventoryManagement;
create table inventory_history(
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ASSY_Part_Number VARCHAR(50),
    SUBASSY_Part_Number VARCHAR(50),
    Manufacturer NVARCHAR(100),
    Shipping_Classification NVARCHAR(100),
    Airtightness_Inspection INT,
    SCU INT,
    Water_Vapor_Test INT,
    Characteristic_Inspection INT,
    Characteristic_Inspection_Fractional_Items INT,
    Accessories INT,
    FA INT,
    FA_Fractional_Items INT,
    Visual_Inspection INT,
    Update_Date_And_Time VARCHAR(50)

);
select * from inventory_history;
drop table inventory_history;
ALTER TABLE inventory_history
ALTER COLUMN Shipping_Classification NVARCHAR(100);

create table  realtime_shelf_label_status(
	ID INT IDENTITY(1,1) PRIMARY KEY,
	ShelfTagID              nvarchar(16) ,
    PartNumber              nvarchar(20) NOT NULL,
    NextProcessName         nvarchar(200) NOT NULL,
    ProcessingLot           nvarchar(24) NOT NULL UNIQUE,
    Quantity                int NOT NULL,
    WorkStatus              int NOT NULL, -- 0: Waiting, 1: White BG, 2: Black BG, 3: Red BG
    ShelfTagRegistrationDate    datetime2 NOT NULL,
    ShelfTagUpdateDate          datetime2 NOT NULL,
    DurationOfStay              int NOT NULL
);

create table  realtime_shelf_label_status(
	ID INT IDENTITY(1,1) PRIMARY KEY,
	ShelfTagID              nvarchar(16) ,
    PartNumber              nvarchar(20) NOT NULL,
    NextProcessName         nvarchar(200) NOT NULL,
    ProcessingLot           nvarchar(24) NOT NULL UNIQUE,
    Quantity                int NOT NULL,
    WorkStatus              int NOT NULL, -- 0: Waiting, 1: White BG, 2: Black BG, 3: Red BG
    ShelfTagRegistrationDate    nvarchar(200) NOT NULL,
    ShelfTagUpdateDate          nvarchar(200) NOT NULL,
    DurationOfStay              int NOT NULL
);


select * from realtime_shelf_label_status;
drop table realtime_shelf_label_status;

create table spare_capacity_weekly(
	ID INT IDENTITY(1,1) PRIMARY KEY,
	Product_Number	nvarchar(20) NOT NULL UNIQUE,
	Manufacturer	nvarchar(40) NOT NULL,
	Shipping_Classification	nvarchar(40) NOT NULL,
	Airtightness_Inspection	int NOT NULL,
	SCU	int NOT NULL,
	Water_Vapor_Test int NOT NULL,
	Characteristic_Inspection int NOT NULL,	
	Characteristic_Inspection_Odd_Lot int NOT NULL,	
	Accessories int NOT NULL,	
	FA int NOT NULL,	
	FA_Fractional_Items int NOT NULL,	
	Visual_Inspection int NOT NULL,	
	Stock_Receipt_Record int NOT NULL,	
	Pre_Shipment_Inventory int NOT NULL,	
	Plan_1 int NOT NULL,	
	Plan_2 int NOT NULL,	
	Plan_3 int NOT NULL,	
	Plan_4 int NOT NULL,	
	Plan_5 int NOT NULL,	
	Plan_6 int NOT NULL,	
	Plan_7 int NOT NULL,	
	Updated int NOT NULL,
);

select * from spare_capacity_weekly;
ALTER TABLE spare_capacity_weekly
ALTER COLUMN Updated DATETIME NOT NULL;

create table interim_inventory_transition(																									
	ID INT IDENTITY(1,1) PRIMARY KEY,
	ASSY_Part_Number	nvarchar(10) NOT NULL UNIQUE,
	SUBASSY nchar(10) NOT NULL UNIQUE,
	Manufacturer nvarchar(20) NOT NULL UNIQUE,
	Shipping_Class nvarchar(20) NOT NULL UNIQUE,
	Airtight_inspection int NOT NULL,
	SCU int NOT NULL,
	Water_Vapor_Inspection int NOT NULL,
	Characteristics_inspection int NOT NULL,
	Characteristic_inspection_odd_lot int NOT NULL,
	Accessories int NOT NULL,
	FA int NOT NULL,
	FA_fractional_items int NOT NULL,
	Visual_inspection int NOT NULL,
	Updated int NOT NULL,
);

CREATE TABLE interim_inventory_transition (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ASSY_Part_Number NVARCHAR(10) NOT NULL,
    SUBASSY NCHAR(10) NOT NULL,
    Manufacturer NVARCHAR(20) NOT NULL,
    Shipping_Class NVARCHAR(20) NOT NULL,
    Airtight_inspection INT NOT NULL,
    SCU INT NOT NULL,
    Water_Vapor_Inspection INT NOT NULL,
    Characteristics_inspection INT NOT NULL,
    Characteristic_inspection_odd_lot INT NOT NULL,
    Accessories INT NOT NULL,
    FA INT NOT NULL,
    FA_fractional_items INT NOT NULL,
    Visual_inspection INT NOT NULL,
    Updated DATETIME NOT NULL,  -- Changed from INT to DATETIME
    CONSTRAINT uq_inventory UNIQUE (
        Updated,
        ASSY_Part_Number,
        SUBASSY,
        Manufacturer,
        Shipping_Class
    )
);

create table interim_inventory_transition(																									
	ASSY_Part_Number nvarchar(10) NOT NULL PRIMARY KEY,
	SUBASSY nchar(10) NOT NULL ,
	Manufacturer nvarchar(20) NOT NULL ,
	Shipping_Class nvarchar(20) NOT NULL ,
	Airtight_inspection int NOT NULL,
	SCU int NOT NULL,
	Water_Vapor_Inspection int NOT NULL,
	Characteristics_inspection int NOT NULL,
	Characteristic_inspection_odd_lot int NOT NULL,
	Accessories int NOT NULL,
	FA int NOT NULL,
	FA_fractional_items int NOT NULL,
	Visual_inspection int NOT NULL,
	Updated int NOT NULL,
);

select * from nox_assy_wip_inventories_history;
select * from nox_assy_inv_mgt_thresh;

drop table interim_inventory_transition;
ALTER TABLE interim_inventory_transition
ALTER COLUMN Updated nvarchar(10) NOT NULL;
