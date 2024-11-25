from fastapi import  Depends,APIRouter
from sqlalchemy.orm import Session
from sql import get_db,Base
from sqlalchemy import Column, String, Text, JSON, Integer, TIMESTAMP, DateTime, Float, Boolean
from sqlalchemy.sql import func


app = APIRouter()


class logTable(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=func.now())
    type = Column(String(10))
    username = Column(String(10), default='访客')
    ip = Column(String(45))
    input = Column(Text)
    output = Column(Text)
    state = Column(Boolean, default=True)

# 新增解析记录
def add_log(db: Session,logDict:dict):
    logdb = logTable(**logDict)

    db.add(logdb)
    db.commit()
    db.refresh(logdb)

# 查询记录表长度
@app.get("/log/total", tags=["记录表"], summary="查询记录表长度")
def get_log_total(db: Session = Depends(get_db)):
    return db.query(logTable).count()

# 分页查询记录数据
@app.get("/logPage", tags=["记录表"], summary="分页查询")
def get_log_page(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(logTable).offset(skip).limit(limit).all()
