from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mange import food,log,user
import os
import parsing
import time 
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="KnowMate")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# 设置静态目录images
mount_path = "/images"
# 检查并创建images目录
if not os.path.exists(mount_path):
    os.makedirs(mount_path)

app.mount(mount_path, StaticFiles(directory="images"), name="images")

app.include_router(food.app)
app.include_router(log.app)
app.include_router(parsing.app)
app.include_router(user.app)



USERNAME='root'
PASSWORD='Fu0xuan.112'
HOSTNAME='47.109.71.57'
PORT='3306'
DATABASE='kmdb'
CHARSET='utf8mb4'
SQL_URL=('mysql://'+
        USERNAME+':'+PASSWORD+'@'+
        HOSTNAME+':'+PORT+'/'+
        DATABASE)

register_tortoise(
    app,
    db_url=SQL_URL,  # 这里可以根据需要更换为其他数据库，如 PostgreSQL
    modules={'models': ['Table']},  
    generate_schemas=True, # 自动生成数据库表
    add_exception_handlers=False,# 数据库调试信息
)


@app.get("/")
async def read_root(req:Request):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("当前时间:", current_time)
    # 打印请求信息
    print("来自", req.url)
    body = await req.body()
    print("请求体:", body)
    print("请求头:", req.headers)
    # 打印当前时间

    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)