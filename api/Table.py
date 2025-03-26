from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# 配料表模型
class Food(models.Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=20, unique=True)
    type = fields.CharField(max_length=20, null=True)
    intro = fields.TextField(null=True)
    effect = fields.TextField(null=True)
    harmType = fields.CharField(max_length=10, null=True)
    harmReason = fields.TextField(null=True)
    risk = fields.TextField(null=True)
    ruler = fields.JSONField(null=True)
    createtime = fields.DatetimeField(auto_now_add=True)
    modiftime = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "foods"


class RulerItem(BaseModel):
    url: str
    title: str


# 创建Pydantic模型，用于响应
FoodPydantic = pydantic_model_creator(Food, name="Food")
FoodInPydantic = pydantic_model_creator(Food, name="FoodIn", exclude_readonly=True)

# 记录表模型
class Log(models.Model):
    id = fields.IntField(pk=True)
    time = fields.DatetimeField(auto_now_add=True)
    type = fields.CharField(max_length=10, null=True)
    username = fields.CharField(max_length=10, default='访客')
    ip = fields.CharField(max_length=45, null=True)
    input = fields.TextField(null=True)
    output = fields.TextField(null=True)
    state = fields.BooleanField(default=True)

    class Meta:
        table = "logs"


# 添加Log的Pydantic模型
LogPydantic = pydantic_model_creator(Log, name="Log")
LogInPydantic = pydantic_model_creator(Log, name="LogIn", exclude_readonly=True)

# 用户表模型
class User(models.Model):
    username = fields.CharField(max_length=30, pk=True)
    password = fields.CharField(max_length=30)
    email = fields.CharField(max_length=30, null=True)
    age = fields.IntField(null=True)
    gender = fields.CharField(max_length=2, null=True)
    height = fields.FloatField(null=True)
    weight = fields.FloatField(null=True)
    allergy = fields.JSONField(null=True, default=[])
    allergyOther = fields.CharField(max_length=30, null=True)
    disease = fields.JSONField(null=True, default=[])
    diseaseOther = fields.CharField(max_length=30, null=True)
    goals = fields.CharField(max_length=2, null=True)
    need = fields.JSONField(null=True, default=[])
    needOther = fields.CharField(max_length=30, null=True)
    createtime = fields.DatetimeField(auto_now_add=True)
    muslim = fields.BooleanField(default=False)

    class Meta:
        table = "users"

# 创建User的Pydantic模型
UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
