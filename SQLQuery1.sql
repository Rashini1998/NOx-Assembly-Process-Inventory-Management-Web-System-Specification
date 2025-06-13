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

            "ASSY品番": r.,
            "SUBASSY品番": r.,
            "メーカ": r.,
            "出荷区分": r.,
            "気密検査": r.,
            "SCU": r.,
            "水蒸気検査": r.,
            "特性検査": r.,
            "特性検査端数品": r.,
            "アクセサリ": r.,
            "FA": r.FA,
            "FA端数品": r.,
            "外観検査": r.,
            "更新日時": r.,

select * from nox_assy_wip_inventories_history;

SELECT  *
FROM nox_assy_wip_inventories_history
WHERE ASSY品番 = '1144780280' AND  ;


EXEC sp_rename 'nox_assy_wip_inventories_history.ASSY_Part_Number', N'ASSY品番', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.SUBASSY', N'SUBASSY品番', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Manufacturer', N'メーカ', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Shipping_Class', N'出荷区分', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Airtight_inspection', N'気密検査', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.SCU', N'SCU', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Water_Vapor_Inspection', N'水蒸気検査', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Characteristics_inspection', N'特性検査', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Characteristic_inspection_odd_lot', N'特性検査端数品', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Accessories', N'アクセサリ', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.FA', N'FA', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.FA_fractional_items', N'FA端数品', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Visual_inspection', N'外観検査', 'COLUMN';
EXEC sp_rename 'nox_assy_wip_inventories_history.Updated', N'更新日時', 'COLUMN';


ALTER TABLE nox_assy_wip_inventories_history
ADD CONSTRAINT pk_nox_assy_wip_composite
PRIMARY KEY (ASSY_Part_Number, SUBASSY, Manufacturer, Shipping_Class, Updated);


select * from nox_assy_inv_mgt_thresh;

EXEC sp_rename 'nox_assy_inv_mgt_thresh.Part_Number', N'品番', 'COLUMN';
EXEC sp_rename 'nox_assy_inv_mgt_thresh.Inventory_Management_Group_Name', N'在庫管理グループ名称', 'COLUMN';
EXEC sp_rename 'nox_assy_inv_mgt_thresh.Standard_Stock_Quantity', N'基準在庫数', 'COLUMN';
EXEC sp_rename 'nox_assy_inv_mgt_thresh.Standard_Inventory_Limit', N'基準在庫上限数', 'COLUMN';
EXEC sp_rename 'nox_assy_inv_mgt_thresh.Standard_Stock_Minimum_Quantity', N'基準在庫下限数', 'COLUMN';

SELECT DISTINCT 在庫管理グループ名称 
FROM nox_assy_inv_mgt_thresh;

ALTER TABLE nox_assy_inv_mgt_thresh
ADD CONSTRAINT pk_nox_assy_inv_mgt_thresh
PRIMARY KEY (Part_Number, Inventory_Management_Group_Name);

drop table interim_inventory_transition;
ALTER TABLE interim_inventory_transition
ALTER COLUMN Updated nvarchar(10) NOT NULL;

SELECT DISTINCT Inventory_Management_Group_Name FROM nox_assy_inv_mgt_thresh;
SHOW CREATE TABLE nox_assy_inv_mgt_thresh;
ALTER TABLE nox_assy_inv_mgt_thresh CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



SELECT DISTINCT Inventory_Management_Group_Name 
FROM nox_assy_inv_mgt_thresh;

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'nox_assy_inv_mgt_thresh';


SELECT COUNT(*) FROM nox_assy_inv_mgt_thresh;




select * from nox_assy_inv_mgt_thresh;


SELECT 
    -- From WIP_Inventories
    W.ASSY_Part_Number AS ASSYPartNumber,
    W.SUBASSY,
    W.Manufacturer,
    W.Shipping_Class AS ShippingClass,
    W.Airtight_inspection AS AirtightInspection,
    W.SCU,
    W.Water_Vapor_Inspection AS WaterVaporInspection,
    W.Characteristics_inspection AS CharacteristicsInspection,
    W.Characteristic_inspection_odd_lot AS CharacteristicInspectionOddLot,
    W.Accessories,
    W.FA,
    W.FA_fractional_items AS FAFractionalItems,
    W.Visual_inspection AS VisualInspection,
    W.Updated,

    -- From IITS_Master (can be NULL)
    I.Inventory_Management_Group_Name AS InventoryManagementGroupName,
    I.Standard_Stock_Quantity AS StandardStockQuantity,
    I.Standard_Inventory_Limit AS StandardInventoryLimit,
    I.Standard_Stock_Minimum_Quantity AS StandardStockMinimumQuantity

FROM 
    nox_assy_wip_inventories_history W
LEFT OUTER JOIN 
    nox_assy_inv_mgt_thresh I
    ON W.ASSY_Part_Number = I.Part_Number;


SELECT 
    W.ASSY_Part_Number AS ASSYPartNumber,
    W.SUBASSY,
    W.Manufacturer,
    W.Shipping_Class AS ShippingClass,
    W.Airtight_inspection AS AirtightInspection,
    W.SCU,
    W.Water_Vapor_Inspection AS WaterVaporInspection,
    W.Characteristics_inspection AS CharacteristicsInspection,
    W.Characteristic_inspection_odd_lot AS CharacteristicInspectionOddLot,
    W.Accessories,
    W.FA,
    W.FA_fractional_items AS FAFractionalItems,
    W.Visual_inspection AS VisualInspection,
    W.Updated,

    I.Inventory_Management_Group_Name AS InventoryManagementGroupName,
    I.Standard_Stock_Quantity AS StandardStockQuantity,
    I.Standard_Inventory_Limit AS StandardInventoryLimit,
    I.Standard_Stock_Minimum_Quantity AS StandardStockMinimumQuantity

INTO all_new_interim_transactions
FROM 
    nox_assy_wip_inventories_history W
LEFT OUTER JOIN 
    nox_assy_inv_mgt_thresh I
    ON W.ASSY_Part_Number = I.Part_Number;



ALTER TABLE all_new_interim_transactions
ADD id INT IDENTITY(1,1);

ALTER TABLE all_new_interim_transactions
ADD CONSTRAINT PK_all_new_interim_transactions PRIMARY KEY (id);


select * from all_new_interim_transactions;

select distinct InventoryManagementGroupName from all_new_interim_transactions;

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'all_new_interim_transactions';

ALTER TABLE all_new_interim_transactions
ALTER COLUMN InventoryManagementGroupName nvarchar(40) ;

SELECT InventoryManagementGroupName, COUNT(*) 
FROM new_inventory_table 
GROUP BY InventoryManagementGroupName;


drop table new_inventory_table;

SELECT  COUNT(*) as count
FROM all_new_interim_transactions 


SELECT *
FROM all_new_interim_transactions
WHERE InventoryManagementGroupName = '?????'


SELECT c.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu ON tc.CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
JOIN INFORMATION_SCHEMA.COLUMNS c ON c.TABLE_NAME = tc.TABLE_NAME AND c.COLUMN_NAME = ccu.COLUMN_NAME
WHERE tc.TABLE_NAME = 'all_new_interim_transactions' AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY';


SELECT ASSYPartNumber,  COUNT(*)
FROM all_new_interim_transactions
GROUP BY ASSYPartNumber
HAVING COUNT(*) > 1;


select * from nox_assy_esl_status;

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'nox_assy_esl_status';


ALTER TABLE nox_assy_esl_status
ADD id INT IDENTITY(1,1);

ALTER TABLE nox_assy_esl_status
ADD CONSTRAINT PK_all_nox_assy_esl_status PRIMARY KEY (id);


select * from nox_assy_wip_inventories2;
drop table nox_assy_wip_inventories2;

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'nox_assy_wip_inventories2';


ALTER TABLE nox_assy_wip_inventories2
ADD id INT IDENTITY(1,1);

ALTER TABLE nox_assy_wip_inventories2
ADD CONSTRAINT PK_all_nox_assy_wip_inventories2 PRIMARY KEY (id);


select * from nox_assy_wip_inventories_new;


SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'nox_assy_wip_inventories_new';


ALTER TABLE nox_assy_wip_inventories_new
ADD id INT IDENTITY(1,1);

ALTER TABLE nox_assy_wip_inventories_new
ADD CONSTRAINT PK_all_nox_assy_wip_inventories_new PRIMARY KEY (id);



select * from nox_assy_inv_mgt_master_new;

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'nox_assy_inv_mgt_master_new';

ALTER TABLE nox_assy_inv_mgt_master_new
ADD id INT IDENTITY(1,1);

ALTER TABLE nox_assy_inv_mgt_master_new
ADD CONSTRAINT PK_all_nox_assy_inv_mgt_master_new PRIMARY KEY (id);