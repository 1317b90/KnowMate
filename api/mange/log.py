from fastapi import APIRouter
from Table import Log
from typing import Dict, Any


app = APIRouter(tags=["记录表"])


# 新增解析记录函数
async def add_log(logDict: Dict[str, Any]):
    await Log.create(**logDict)


@app.get("/logs", summary="分页查询记录")
async def get_logs(skip: int = 0, limit: int = 10):
    # 获取总记录数
    total = await Log.all().count()
    # 获取分页数据
    logs = await Log.all().offset(skip).limit(limit)
    
    return {
        "total": total,
        "data": logs
    }