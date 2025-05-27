from src import db
class IITS_Master(db.Model):
    __tablename__ = 'nox_assy_inv_mgt_thresh'

    # Part_Number = db.Column(db.Unicode(20),primary_key=True,nullable=False)
    # Inventory_Management_Group_Name = db.Column(db.Unicode(100),primary_key=True)
    # Standard_Stock_Quantity = db.Column(db.Unicode(50),nullable=False)
    # Standard_Inventory_Limit = db.Column(db.Unicode(50),nullable=False)
    # Standard_Stock_Minimum_Quantity = db.Column(db.Unicode(50),nullable=False)

    品番 = db.Column(db.Unicode(20),primary_key=True,nullable=False)
    在庫管理グループ名称 = db.Column(db.Unicode(100),primary_key=True)
    基準在庫数 = db.Column(db.Unicode(50),nullable=False)
    基準在庫上限数 = db.Column(db.Unicode(50),nullable=False)
    基準在庫下限数 = db.Column(db.Unicode(50),nullable=False)
