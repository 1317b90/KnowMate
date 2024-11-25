from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from sql import get_db,Base
from sqlalchemy import Column, String, Text, JSON, DateTime
from sqlalchemy.sql import func

from datetime import datetime

from pydantic import BaseModel
from typing import Optional,List

app = APIRouter()

# 配料表模型
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
    religion =  Column(String(10))

class RulerItem(BaseModel):
    url: str
    title: str

class foodModel(BaseModel):
    name: str
    type: Optional[str]=None
    intro: Optional[str]=None
    effect: Optional[str]=None
    harmType: Optional[str]=None
    harmReason: Optional[str]=None
    out: Optional[str]=None
    ruler: Optional[List[RulerItem]] = None
    createtime: Optional[datetime]= None
    modiftime: Optional[datetime]= None
    religion: Optional[str]=None

# 查询配料数据
@app.get("/food", tags=["配料表"], summary="查询")
def get_food(name: str, db: Session = Depends(get_db)):
    return db.get(foodTable, name)


# 新增配料数据
@app.post("/food", tags=["配料表"], summary="新增")
def add_food(data: foodModel, db: Session = Depends(get_db)):
    if get_food(data.name,db):
        raise HTTPException(status_code=401, detail="该配料已存在")
    else:
        fooddb = foodTable(**data.dict())
        db.add(fooddb)
        db.commit()
        db.refresh(fooddb)


# 修改配料数据
@app.put("/foot", tags=["配料表"], summary="修改")
def set_food(data: foodModel, db: Session = Depends(get_db)):
    fooddb = get_food(data.name,db)
    if fooddb:
        for key, value in data.dict(exclude_unset=True).items():
            if hasattr(fooddb, key):
                setattr(fooddb, key, value)
        db.commit()
        db.refresh(fooddb)
    else:
        raise HTTPException(status_code=404, detail="该配料不存在")


# 删除配料数据
@app.delete("/food", tags=["配料表"], summary="删除")
def del_food(name: str, db: Session = Depends(get_db)):
    if get_food(name,db):
        db.query(foodTable).filter_by(name=name).delete()
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="该配料不存在")
    
# 查询食品表长度
@app.get("/food/total", tags=["配料表"], summary="查询配料表长度")
async def get_food_total(db: Session = Depends(get_db)):
    return db.query(foodTable).count()


# 分页查询配料数据
@app.get("/food/page", tags=["配料表"], summary="分页查询")
async def get_food_page(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(foodTable).offset(skip).limit(limit).all()