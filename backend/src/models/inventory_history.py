from src import db
from sqlalchemy import BigInteger,SmallInteger, DateTime

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


class InventoryHistoryNew(db.Model):
    __tablename__ = 'nox_assy_wip_inventories_new'

    ID = db.Column(db.Integer, primary_key=True)
    ASSY品番 = db.Column(db.BigInteger)
    SUBASSY品番 = db.Column(db.BigInteger)
    メーカ = db.Column(db.Unicode(50))
    出荷区分 = db.Column(db.Unicode(50))
    気密検査 = db.Column(db.SmallInteger)
    SCU = db.Column(db.SmallInteger)
    水蒸気検査 = db.Column(db.SmallInteger)
    特性検査 = db.Column(db.SmallInteger)
    特性検査端数品 = db.Column(db.SmallInteger)
    アクセサリ = db.Column(db.SmallInteger)
    FA = db.Column(db.SmallInteger)
    FA端数品 = db.Column(db.SmallInteger)
    外観検査 = db.Column(db.SmallInteger)
    更新日時 = db.Column(db.Unicode(50))
