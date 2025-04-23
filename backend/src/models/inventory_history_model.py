from src import db

class InventoryHistory(db.Model):
    __tablename__ = 'inventory_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assy_part_number = db.Column(db.String(50))
    subassy_part_number = db.Column(db.String(50))
    manufacturer = db.Column(db.String(100))
    shipping_classification = db.Column(db.String(100))
    airtightness_inspection = db.Column(db.Integer)
    scu = db.Column(db.Integer)
    water_vapor_test = db.Column(db.Integer)
    characteristic_inspection = db.Column(db.Integer)
    characteristic_inspection_fractional_items = db.Column(db.Integer)
    accessories = db.Column(db.Integer)
    fa = db.Column(db.Integer)
    fa_fractional_items = db.Column(db.Integer)
    visual_inspection = db.Column(db.Integer)
    update_date_and_time = db.Column(db.String(50))  # use db.DateTime if storing real datetime
