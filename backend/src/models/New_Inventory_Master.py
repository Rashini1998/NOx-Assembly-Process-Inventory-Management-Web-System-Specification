from src import db
from datetime import datetime

class New_Inventory_Master(db.Model):
    __tablename__ = 'all_new_interim_transactions'

    ASSYPartNumber = db.Column(db.String(10), primary_key=True, nullable=False)  # nvarchar(10)
    SUBASSY = db.Column(db.String(10))  # nchar(10)
    Manufacturer = db.Column(db.String(20), nullable=False)  # nvarchar(20)
    ShippingClass = db.Column(db.String(20), nullable=False)  # nvarchar(20)
    AirtightInspection = db.Column(db.Integer)
    SCU = db.Column(db.Integer)
    WaterVaporInspection = db.Column(db.Integer)
    CharacteristicsInspection = db.Column(db.Integer)
    CharacteristicInspectionOddLot = db.Column(db.Integer)
    Accessories = db.Column(db.Integer)
    FA = db.Column(db.Integer)
    FAFractionalItems = db.Column(db.Integer)
    VisualInspection = db.Column(db.Integer)
    Updated = db.Column(db.DateTime)
    InventoryManagementGroupName = db.Column(db.String(40))  # nvarchar(40)
    StandardStockQuantity = db.Column(db.String(50))  # nvarchar(50)
    StandardInventoryLimit = db.Column(db.String(50))  # nvarchar(50)
    StandardStockMinimumQuantity = db.Column(db.String(50))  # nvarchar(50)
