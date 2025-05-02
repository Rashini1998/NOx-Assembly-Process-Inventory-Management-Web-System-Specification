from src import db
from datetime import datetime

class InventoryAvailability(db.Model):
    __tablename__ = 'spare_capacity_weekly'

    ID = db.Column(db.Integer, primary_key=True) 
    Product_Number = db.Column(db.Unicode(20),nullable=False)
    Manufacturer =	db.Column(db.Unicode(40),nullable=False)
    Shipping_Classification = 	db.Column(db.Unicode(40),nullable=False)
    Airtightness_Inspection	= db.Column(db.Integer,nullable=False)
    SCU	= db.Column(db.Integer,nullable=False)
    Water_Vapor_Test =  db.Column(db.Integer,nullable=False)
    Characteristic_Inspection = db.Column(db.Integer,nullable=False)	
    Characteristic_Inspection_Odd_Lot = db.Column(db.Integer,nullable=False)
    Accessories = db.Column(db.Integer,nullable=False)	
    FA = db.Column(db.Integer,nullable=False)	
    FA_Fractional_Items =db.Column(db.Integer,nullable=False)	
    Visual_Inspection = db.Column(db.Integer,nullable=False)	
    Stock_Receipt_Record = db.Column(db.Integer,nullable=False)	
    Pre_Shipment_Inventory = db.Column(db.Integer,nullable=False)	
    Plan_1 = db.Column(db.Integer,nullable=False)	
    Plan_2 = db.Column(db.Integer,nullable=False)	
    Plan_3 = db.Column(db.Integer,nullable=False)	
    Plan_4 = db.Column(db.Integer,nullable=False)	
    Plan_5 = db.Column(db.Integer,nullable=False)	
    Plan_6 = db.Column(db.Integer,nullable=False)	
    Plan_7 = db.Column(db.Integer,nullable=False)	
    # Updated = db.Column(db.Integer,nullable=False)
    Updated = db.Column(db.DateTime, nullable=False)

    
