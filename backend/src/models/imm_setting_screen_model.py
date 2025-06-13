from src import db
from sqlalchemy import SmallInteger, DateTime

class IMM_Setting(db.Model):
    __tablename__ = 'nox_assy_inv_mgt_master_new'

    id = db.Column(db.Integer, primary_key=True)
    設備グループID = db.Column(db.Unicode(50),nullable=False)
    設備機番 = db.Column(db.Unicode(50),nullable=False)
    設備グループ名称 = db.Column(db.Unicode(50),nullable=False)
    在庫管理グループID = db.Column(db.Unicode(50),nullable=False)
    在庫管理グループ名称 = db.Column(db.Unicode(50),nullable=False)
    基準在庫日数 = db.Column(db.SmallInteger)
    基準在庫管理幅 = db.Column(db.Unicode(50))
