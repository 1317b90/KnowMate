from datetime import datetime

from pydantic import BaseModel, conint, constr, condecimal
from typing import Optional,Union as TypingUnion,List


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

class recordModel(BaseModel):
    id: Optional[int]= None
    username:Optional[str]= None
    time: Optional[datetime]= None
    ip: Optional[str]= None
    food: Optional[str]
    static: Optional[bool]= None
    remarks: Optional[str]= None


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