from src import db
from sqlalchemy import DateTime
from sqlalchemy import BigInteger,SmallInteger

class LabelStatus(db.Model):
    __tablename__ = 'realtime_shelf_label_status'

    # ID = db.Column(db.Integer, primary_key=True)
    # ShelfTagID = db.Column(db.Unicode(16))
    # PartNumber = db.Column(db.Unicode(20),nullable=False)
    # NextProcessName = db.Column(db.Unicode(200),nullable=False)
    # ProcessingLot = db.Column(db.Unicode(24),nullable=False)
    # Quantity = db.Column(db.Integer,nullable=False)
    # WorkStatus = db.Column(db.Integer,nullable=False)
    # ShelfTagRegistrationDate = db.Column(DateTime, nullable=False)
    # ShelfTagUpdateDate = db.Column(DateTime, nullable=False)
    # DurationOfStay = db.Column(db.Integer,nullable=False)
    
    ID = db.Column(db.Integer, primary_key=True)
    ShelfTagID = db.Column(db.Unicode(16))
    PartNumber = db.Column(db.Unicode(20),nullable=False)
    NextProcessName = db.Column(db.Unicode(200),nullable=False)
    ProcessingLot = db.Column(db.Unicode(24),nullable=False)
    Quantity = db.Column(db.Integer,nullable=False)
    WorkStatus = db.Column(db.Integer,nullable=False)
    ShelfTagRegistrationDate = db.Column(db.Unicode(200),nullable=False)
    ShelfTagUpdateDate = db.Column(db.Unicode(200),nullable=False)
    DurationOfStay = db.Column(db.Integer,nullable=False)

class LabelStatusNew(db.Model):
    __tablename__ = 'nox_assy_esl_status'

    ID = db.Column(db.Integer, primary_key=True)
    棚札ID = db.Column(db.Unicode(50))
    品番 = db.Column(db.BigInteger,nullable=False)
    次工程名称 = db.Column(db.Unicode(50),nullable=False)
    加工Lot = db.Column(db.Unicode(50),nullable=False)
    数量 = db.Column(db.SmallInteger,nullable=False)
    作業状況 = db.Column(db.SmallInteger,nullable=False)
    棚札登録日時 = db.Column(db.Unicode(50),nullable=False)
    棚札更新日時 = db.Column(db.Unicode(50),nullable=False)
    滞留日数 = db.Column(db.SmallInteger,nullable=False)