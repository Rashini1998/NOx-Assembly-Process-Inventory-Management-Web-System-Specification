from src import db
from sqlalchemy import DateTime
from sqlalchemy import BigInteger

class LabelStatus(db.Model):
    __tablename__ = 'realtime_shelf_label_status'

    ID = db.Column(db.Integer, primary_key=True)
    ShelfTagID = db.Column(db.Unicode(16))
    PartNumber = db.Column(db.Unicode(20),nullable=False)
    NextProcessName = db.Column(db.Unicode(200),nullable=False)
    ProcessingLot = db.Column(db.Unicode(24),nullable=False)
    Quantity = db.Column(db.Integer,nullable=False)
    WorkStatus = db.Column(db.Integer,nullable=False)
    ShelfTagRegistrationDate = db.Column(DateTime, nullable=False)
    ShelfTagUpdateDate = db.Column(DateTime, nullable=False)
    DurationOfStay = db.Column(db.Integer,nullable=False)
