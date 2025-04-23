# from src import db

# class InventoryHistory(db.Model):
#     __tablename__ = 'inventory_history'

#     ID = db.Column(db.Integer, primary_key=True)
#     ASSY_Part_Number = db.Column(db.String(50))
#     SUBASSY_Part_Number = db.Column(db.String(50))
#     Manufacturer = db.Column(db.String(100))
#     Shipping_Classification = db.Column(db.String(100))
#     Airtightness_Inspection = db.Column(db.Integer)
#     SCU = db.Column(db.Integer)
#     Water_Vapor_Test = db.Column(db.Integer)
#     Characteristic_Inspection = db.Column(db.Integer)
#     Characteristic_Inspection_Fractional_Items = db.Column(db.Integer)
#     Accessories = db.Column(db.Integer)
#     FA = db.Column(db.Integer)
#     FA_Fractional_Items = db.Column(db.Integer)
#     Visual_Inspection = db.Column(db.Integer)
#     Update_Date_And_Time = db.Column(db.String(50))

from src import db

class InventoryHistory(db.Model):
    __tablename__ = 'inventory_history'

    ID = db.Column(db.Integer, primary_key=True)
    ASSY_Part_Number = db.Column(db.String(50))
    SUBASSY_Part_Number = db.Column(db.String(50))
    Manufacturer = db.Column(db.Unicode(100))
    Shipping_Classification = db.Column(db.Unicode(100))
    Airtightness_Inspection = db.Column(db.Integer)
    SCU = db.Column(db.Integer)
    Water_Vapor_Test = db.Column(db.Integer)
    Characteristic_Inspection = db.Column(db.Integer)
    Characteristic_Inspection_Fractional_Items = db.Column(db.Integer)
    Accessories = db.Column(db.Integer)
    FA = db.Column(db.Integer)
    FA_Fractional_Items = db.Column(db.Integer)
    Visual_Inspection = db.Column(db.Integer)
    Update_Date_And_Time = db.Column(db.String(50))
