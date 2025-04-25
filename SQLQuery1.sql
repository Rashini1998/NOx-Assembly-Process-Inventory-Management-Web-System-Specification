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

select * from realtime_shelf_label_status;
drop table realtime_shelf_label_status;