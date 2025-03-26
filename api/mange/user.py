from sqlalchemy import Column, String, JSON, Integer, TIMESTAMP, Float, Boolean
from sqlalchemy.sql import func

from sql import get_db,Base

from fastapi import  Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session

from datetime import datetime

from pydantic import BaseModel
from typing import Optional,Union as TypingUnion


app = APIRouter(tags=["用户数据表"])

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
    allergyOther = Column(String(30))
    disease = Column(JSON)
    diseaseOther = Column(String(30))
    goals = Column(String(2))
    need = Column(JSON)
    needOther = Column(String(30))
    createtime = Column(TIMESTAMP, server_default=func.current_timestamp())
    religion =  Column(Boolean, server_default='0')



class userModel(BaseModel):
    username: str
    password: str
    email: Optional[str]= None
    age: Optional[int]= None
    gender: Optional[str]= None
    height: Optional[TypingUnion[float, int]]= None
    weight: Optional[TypingUnion[float, int]]= None
    allergy: Optional[list]= None
    allergyOther : Optional[str]= None
    disease: Optional[list]= None
    diseaseOther : Optional[str] = None
    goals: Optional[str]= None
    need:Optional[list]= None
    needOther : Optional[str] = None
    createtime: Optional[datetime]= None
    religion: Optional[bool] = None

# 获取单个用户数据
@app.get("/user",  summary="查询")
def get_user(username: str, db: Session = Depends(get_db)):
    return db.get(userTable, username)


# 获取用户的个人信息作为饮食建议的输入
def get_user_info(username: str):
    with next(get_db()) as db:
        user = get_user(username, db)
        if user is None:
            return None
        else:
            user_info=""
            if user.age:
                user_info += str(user.age) + "岁，"
            if user.height:
                user_info += "身高" + str(user.height) + "cm，"
            if user.weight:
                user_info += "体重" + str(user.weight) + "kg，"
            if user.allergy is not None and len(user.allergy) > 0:
                user_info += "对"
                for allergy in user.allergy:
                    if allergy != "其他":
                        user_info += allergy + "，"
                    else:
                        if user.allergyOther:
                            user_info += user.allergyOther
                user_info += "过敏，"

            if user.disease is not None and len(user.disease) > 0:
                user_info += "有"
                for disease in user.disease:
                    if disease != "其他":
                        user_info += disease + "，"
                    else:
                        if user.diseaseOther:
                            user_info += user.diseaseOther

            if user.goals and user.goals != "无":
                user_info += "，体重目标为" + user.goals

            if user.need is not None and len(user.need) > 0:
                user_info += "，饮食需求为"
                for need in user.need:
                    if need != "其他":
                        user_info += need + "，"
                    else:
                        if user.needOther:
                            user_info += user.needOther

            if user.gender:
                user_info += "的" + user.gender + "性"
            else:
                user_info += "的人"
            return user_info


# 新增用户数据
@app.post("/user", summary="增加")
def add_user(data: userModel, db: Session = Depends(get_db)):
    if get_user(data.username,db):
        raise HTTPException(status_code=422, detail="该用户已存在")
    else:
        userdb = userTable(**data.dict())
        db.add(userdb)
        db.commit()
        db.refresh(userdb)


# 修改用户数据
@app.put("/user", summary="修改")
def set_user(data: userModel, db: Session = Depends(get_db)):
    if  get_user(data.username,db):
        user = get_user(data.username,db)
        for key, value in data.dict(exclude_unset=True).items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(status_code=404, detail="该用户不存在")

# 删除用户数据
@app.delete("/user", summary="删除")
def del_user(username: str, db: Session = Depends(get_db)):
    if  get_user(username,db):
        db.query(userTable).filter_by(username=username).delete()
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="该用户不存在")

# 分页获取所有用户数据
@app.get("/users",summary="查询所有用户数据")
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query=db.query(userTable)
    # 获取总数据条数
    total = query.count()
    # 获取分页数据
    users = query.offset(skip).limit(limit).all()
    # 返回分页数据和总数据条数
    return {
        "total": total,
        "data": users
    }


# 查询用户表长度
@app.get("/user/total", summary="查询用户表长度")
def get_user_total(db: Session = Depends(get_db)):
    return db.query(userTable).count()


# 分页查询用户数据
@app.get("/user/page", summary="分页查询")
def get_user_page(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(userTable).offset(skip).limit(limit).all()


# 登陆
@app.post("/user/login", summary="登陆")
def login(data: userModel, db: Session = Depends(get_db)):
    user = get_user(data.username,db)
    if user is None:
        raise HTTPException(status_code=404, detail="该用户不存在")
    else:
        if user.password != data.password:
            raise HTTPException(status_code=400, detail="账号或密码错误")
        else:
            return "登陆成功"

