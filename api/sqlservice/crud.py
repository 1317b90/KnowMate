from sqlalchemy.orm import Session

from sqlservice import models, schemas


# ---------食品配料表---------食品配料表---------食品配料表---------食品配料表---------食品配料表---------食品配料表

# 根据name查询配料信息
def get_food(db: Session, name: str):
    return db.get(models.foodTable, name)


# 查询配料数据表长度
def get_food_total(db: Session):
    return db.query(models.foodTable).count()


# 分页查询配料数据表
def get_food_page(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.foodTable).offset(skip).limit(limit).all()


# 新增配料信息
def add_food(db: Session, food: schemas.foodModel):
    fooddb = models.foodTable(**food.dict())
    db.add(fooddb)
    db.commit()
    db.refresh(fooddb)


# 修改配料信息
def set_food(db: Session, food: schemas.foodModel):
    fooddb = get_food(db, food.name)
    for key, value in food.dict(exclude_unset=True).items():
        if hasattr(fooddb, key):
            setattr(fooddb, key, value)
    db.commit()
    db.refresh(fooddb)

# 删除配料数据
def del_food(db: Session, name: str):
    db.query(models.foodTable).filter_by(name=name).delete()
    db.commit()

# ---------记录表---------记录表---------记录表---------记录表---------记录表---------记录表

# 新增记录信息
def add_record(db: Session, record: schemas.recordModel):
    recorddb = models.recordTable(**record.dict())
    db.add(recorddb)
    db.commit()
    db.refresh(recorddb)

# --------用户表--------用户表--------用户表--------用户表--------用户表--------用户表

# 根据usernmae查询用户
def get_user(db: Session, username: str):
    return db.get(models.userTable, username)
# 增加用户
def add_user(db: Session, data: schemas.userModel):
    userdb = models.userTable(**data.dict())
    db.add(userdb)
    db.commit()
    db.refresh(userdb)

# 查询用户数据表长度
def get_user_total(db: Session):
    return db.query(models.userTable).count()

# 分页查询用户数据表
def get_user_page(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.userTable).offset(skip).limit(limit).all()

# 修改用户数据
def set_user(db: Session, data: schemas.userModel):
    user = get_user(db, data.username)
    for key, value in data.dict(exclude_unset=True).items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)

# 删除配料数据
def del_user(db: Session, username: str):
    db.query(models.userTable).filter_by(username=username).delete()
    db.commit()

# 注册
def register(db: Session, data: schemas.userModel):
    userdb = models.userTable(**data.dict())
    db.add(userdb)
    db.commit()
    db.refresh(userdb)