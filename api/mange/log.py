from fastapi import  Depends,APIRouter
from sqlalchemy.orm import Session
from sql import get_db,Base
from sqlalchemy import Column, String, Text, JSON, Integer, TIMESTAMP, DateTime, Float, Boolean
from sqlalchemy.sql import func


app = APIRouter(tags=["记录表"])


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

# 新增解析记录函数
def add_log(logDict:dict):
    with next(get_db()) as db:
            logdb = logTable(**logDict)
            db.add(logdb)
            db.commit()
            db.refresh(logdb)


@app.get("/logs", summary="分页查询记录")
def get_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query=db.query(logTable)
    # 获取总记录数
    total = query.count()
    # 获取分页数据
    logs = query.offset(skip).limit(limit).all()
    return {
        "total": total,
        "data": logs
    }