from sqlalchemy import Column, String, Text, JSON, Integer, TIMESTAMP, Boolean, TEXT,DateTime,Float
from sqlalchemy.sql import func

from sqlservice.conn import Base


class foodTable(Base):
    __tablename__ = "foods"
    name = Column(String(20), primary_key=True, index=True)
    type = Column(String(20))
    intro = Column(Text)
    effect = Column(Text)
    harmType = Column(String(10))
    harmReason = Column(Text)
    out = Column(Text)
    ruler = Column(JSON)
    createtime = Column(DateTime, default=func.now())
    modiftime = Column(DateTime, default=func.now(), onupdate=func.now())



class recordTable(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String(30))
    time = Column(TIMESTAMP, default=func.now())
    ip = Column(String(45))
    food = Column(String(45))
    static = Column(Boolean)
    remarks = Column(TEXT)


class userTable(Base):
    __tablename__ = 'users'

    username = Column(String(30), primary_key=True, nullable=False)
    password = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    age = Column(Integer)
    gender = Column(String(2))
    height = Column(Float)
    weight = Column(Float)
    allergy = Column(JSON)
    allergyOther= Column(String(30))
    disease = Column(JSON)
    diseaseOther = Column(String(30))
    goals = Column(String(2))
    need = Column(JSON)
    needOther = Column(String(30))
    createtime = Column(TIMESTAMP, server_default=func.current_timestamp())
