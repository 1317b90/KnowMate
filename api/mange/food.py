from fastapi import HTTPException, APIRouter
from Table import Food, FoodPydantic, FoodInPydantic

app = APIRouter(tags=["配料数据表"])

# 查询配料数据
@app.get("/food/{name}", summary="查询")
async def get_food(name: str):
    food = await Food.filter(name=name).first()
    if not food:
        return None
    return food

# 新增配料数据
@app.post("/food", summary="新增")
async def add_food(data: FoodInPydantic):
    if await Food.filter(name=data.name).exists():
        raise HTTPException(status_code=401, detail="该配料已存在")
    else:
        food_dict = data.model_dump(exclude_unset=True)
        food = await Food.create(**food_dict)
        return await FoodPydantic.from_tortoise_orm(food)

# 新增配料数据函数
async def add_food_func(data: dict):
    if await Food.filter(name=data.get("name")).exists():
        pass
    else:
        await Food.create(**data)


# 修改配料数据
@app.put("/food/{id}", summary="修改")
async def set_food(id: int, data: FoodInPydantic):
    food = await Food.filter(id=id).first()
    if food:
        food_dict = data.model_dump(exclude_unset=True)
        await Food.filter(id=id).update(**food_dict)
        return True
    else:
        raise HTTPException(status_code=404, detail="该配料不存在")

# 删除配料数据
@app.delete("/food/{name}", summary="删除")
async def del_food(name: str):
    food = await Food.filter(name=name).first()
    if food:
        await food.delete()
    else:
        raise HTTPException(status_code=404, detail="该配料不存在")

# 分页查询配料数据表
@app.get("/foods", summary="分页查询")
async def get_food_page(
    skip: int = 0,  # 跳过的记录数
    limit: int = 10,  # 每页显示的记录数
):
    # 获取总记录数
    total = await Food.all().count()
    # 分页查询数据
    foods = await Food.all().offset(skip).limit(limit)
    # 返回分页结果
    return {
        "total": total,
        "data": foods,
    }

