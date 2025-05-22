from src import db
class WIP_Inventories(db.Model):
    __tablename__ = 'nox_assy_wip_inventories_history'

    ASSY_Part_Number = db.Column(db.Unicode(10),primary_key=True,nullable=False)
    SUBASSY = db.Column(db.Unicode(10),nullable=False)
    Manufacturer = db.Column(db.Unicode(20),nullable=False)
    Shipping_Class = db.Column(db.Unicode(20),nullable=False)
    Airtight_inspection = db.Column(db.Integer,nullable=False)
    SCU = db.Column(db.Integer,nullable=False)
    Water_Vapor_Inspection = db.Column(db.Integer,nullable=False)
    Characteristics_inspection = db.Column(db.Integer,nullable=False)
    Characteristic_inspection_odd_lot = db.Column(db.Integer,nullable=False)
    Accessories = db.Column(db.Integer,nullable=False)
    FA = db.Column(db.Integer,nullable=False)
    FA_fractional_items = db.Column(db.Integer,nullable=False)
    Visual_inspection = db.Column(db.Integer,nullable=False)
    Updated = db.Column(db.Integer,nullable=False)
