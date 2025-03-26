from fastapi import  HTTPException, APIRouter

from Table import User, UserPydantic, UserInPydantic

app = APIRouter(tags=["用户数据表"])

# 获取单个用户数据
@app.get("/user/{username}", summary="查询")
async def get_user(username: str):
    return await User.filter(username=username).first()

# 新增用户数据
@app.post("/user/{username}", summary="增加")
async def add_user(username: str, data: UserInPydantic):
    existing_user = await User.filter(username=username).first()
    if existing_user:
        raise HTTPException(status_code=422, detail="该用户已存在")
    else:
        user_dict = data.model_dump(exclude_unset=True)
        user_dict["username"] = username
        user = await User.create(**user_dict)
        return await UserPydantic.from_tortoise_orm(user)

# 修改用户数据
@app.put("/user/{username}", summary="修改")
async def set_user(username: str, data: UserInPydantic):
    user = await User.filter(username=username).first()
    if user:
        user_data = data.model_dump(exclude_unset=True)
        await User.filter(username=username).update(**user_data)
        return True
    else:
        raise HTTPException(status_code=404, detail="该用户不存在")

# 删除用户数据
@app.delete("/user/{username}", summary="删除")
async def del_user(username: str):
    user = await User.filter(username=username).first()
    if user:
        await user.delete()
        return {"message": "删除成功"}
    else:
        raise HTTPException(status_code=404, detail="该用户不存在")

# 分页获取所有用户数据
@app.get("/users", summary="查询所有用户数据")
async def get_users(skip: int = 0, limit: int = 10):
    # 获取总数据条数
    total = await User.all().count()
    # 获取分页数据
    users = await User.all().offset(skip).limit(limit)
    # 返回分页数据和总数据条数
    return {
        "total": total,
        "data": users
    }




