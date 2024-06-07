import base64
import json

import requests
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from zhipuai import ZhipuAI

from sqlservice import crud, schemas
from sqlservice.conn import SessionLocal

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


client = ZhipuAI(api_key="28698839aff97f518ef798ee22384d74.zrQb5Xa9s7QicZMP")


# ---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr
# ocr鉴权
def get_access_token():
    apiKey = "FWKwWT9J0yQrmLpoODrgAVWF"
    secretKey = "3cFDSoogWETTNPpkckdINBpVCXAj6Cq8"
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    result = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
    return result.get("access_token")


# 从ocr结果中提取配料列表
def get_foodList(ocrText):
    result = client.chat.completions.create(
        model="glm-3-turbo",
        messages=[
            {
                "role": "user",
                "content":
                    f"""
                请帮我从以下食品配料表的OCR识别结果字符串中提取每一项配料，并确保修正其中的错别字。
                我希望得到一个配料列表，格式如下：['配料1', '配料2', ..., '配料N']。
                OCR识别结果字符串为：，{ocrText}
                请确保返回的列表中每一项配料都准确无误，并且格式规范,除了列表外不需要任何多余说明和文字。
                """
            }
        ],
        temperature=0.01,
        stream=False,
    )
    result = json.loads(result.json())

    if result.get("choices") is not None:
        resultList = eval(result["choices"][0]["message"]["content"])
        return [{"id": i, "name": resultList[i], "editing": False} for i in range(len(resultList))]
    else:
        raise HTTPException(status_code=401, detail="配料列表提取失败")


# 接收图片并进行ocr识别
@app.post("/ocrImage", tags=["ocr识别"])
async def get_ocr_Text(file: UploadFile = File(...)):
    imgContents = await file.read()
    params = {"image": base64.b64encode(imgContents), "probability": "true"}
    try:
        # accurate_basic 高精度
        # general_basic 基础版
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        # response = None
        if response:
            # 总准确度
            probabilitys = 0
            # 总识别文字
            words = ""
            # 总识别行数
            i = 0
            for wordJson in response.json()['words_result']:
                words += wordJson.get("words")
                probabilitys += wordJson.get("probability")['average']
                i += 1
            # 如果平均识别精度小于0.85
            if probabilitys / i < 0.85:
                return {"error": "图片精度过低"}
            else:
                return get_foodList(words)
        else:
            raise HTTPException(status_code=401, detail="请求返回体为空")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# ----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析

# 角色定位
role = {
    "role": "system",
    "content": """
    你是一个食品配料方面的专家，拥有广泛的食品科学知识和营养学背景。你的任务是为用户提供食品配料相关的专业、准确、具体、有见地的解释和建议，帮助他们理解和解析食品配料表。
    """
}

# 获取配料法律法规,同时也是验证该配料名称是否合理的方法
def getRuler(foodName):
    rulerUrl = "http://foodcloud.cnif.cn/api/v1/regulations/search?keyword=" + foodName + "&current_page=1&page_size=5"
    rulerRes = requests.get(rulerUrl)
    if rulerRes.status_code == 200:
        rulerRes = json.loads(rulerRes.text)
        if rulerRes.get("status") == "ok":
            rulerList = rulerRes["data"]["list"]
            newRulerList = []
            for ruler in rulerList:
                if ruler.get("status") == "现行有效":
                    title = ruler.get("title").replace("<em>", '')
                    title = title.replace("</em>", '')
                    url = ruler.get("gb_online_url")
                    if url == "":
                        url = ruler.get("file")

                    newRulerList.append({
                        "title": title,
                        "url": url
                    })
            if len(newRulerList) == 0:
                return False
            else:
                return newRulerList

        else:
            raise HTTPException(status_code=401, detail="法规查询请求失败！")
    else:
        raise HTTPException(status_code=401, detail="法规查询请求失败！")


# 解析配料
@app.get("/parsing", tags=["解析配料"])
async def get_parsing(foodName, request: Request, username: str = '访客', db: Session = Depends(get_db)):
    # 查询数据库中是否存在
    Food = crud.get_food(db, foodName)

    # 记录
    Record = schemas.recordModel(
        ip=request.client.host,
        food=foodName,
        static=True,
        username=username
    )
    # 如果存在，直接返回结果
    if Food:
        crud.add_record(db, Record)
        print(Food.name)
        return Food
    # 如果不存在，当即查询
    else:
        foodRuler = getRuler(foodName)
        if foodRuler:
            result = client.chat.completions.create(
                model="glm-3-turbo",
                messages=[
                    role,
                    {
                        "role": "user",
                        "content": f"""
                        请详细分析食品配料“{foodName}”，并严格按照以下JSON格式返回分析结果，每个键的值尽量不为空：
                        {{
                            "类别": "给出{foodName}的类别",
                            "简介": "请提供关于{foodName}的简短介绍，包括其来源、特性等",
                            "在食品中的作用": "详细描述{foodName}在食品中所起到的功能和作用",
                            "对人体是否有害或有益": "请从以下选项中选择：[有益，有害，不确定]",
                            "对人体有害或有益或不确定的原因": "根据现有科学研究或食品安全标准，解释为何{foodName}对人体有益、有害或不确定",
                            "不适宜人群": "列出哪些人群不适合食用含有{foodName}的食品，或可能对{foodName}产生过敏反应"
                        }}
                        请确保您的分析基于最新的科学研究、食品安全标准以及可靠的资料。您的回复应当清晰、准确，并尽可能详尽地满足上述JSON格式的要求。
                        """
                    }
                ],
                # top_p=0.01,
                temperature=0.01,
                stream=False,
            )
            result = json.loads(result.json())
            if result.get("choices") is not None:
                resultText = result["choices"][0]["message"]["content"]
                resultText = resultText.strip().replace('json', '').replace('\n', '').replace('```', '').replace(
                    ' ', '')
                resultJson = json.loads(resultText)
                Food = schemas.foodModel(
                    name=foodName,
                    type=resultJson.get("类别"),
                    intro=resultJson.get("简介"),
                    effect=resultJson.get("在食品中的作用"),
                    harmType=resultJson.get("对人体是否有害或有益"),
                    harmReason=resultJson.get("对人体有害或有益或不确定的原因"),
                    out=resultJson.get("不适宜人群"),
                    ruler=foodRuler
                )
                crud.add_food(db, Food)

                crud.add_record(db, Record)
                # 为啥要加这一句？我也不知道，反正不加就会报错
                print(Food.name)
                return Food
            else:
                Record.static = False
                Record.remarks = "配料解析失败"
                crud.add_record(db, Record)
                raise HTTPException(status_code=400, detail="配料解析失败！")
        else:
            Record.static = False
            Record.remarks = "不是一项食品配料"
            crud.add_record(db, Record)
            raise HTTPException(status_code=444, detail="不是一项食品配料！")

# 食品评价与饮食建议
@app.get("/feadr", tags=["评分"])
async def get_feadr(foodListText: str, username: str = "访客", db: Session = Depends(get_db)):
    try:
        if username == "访客":
            content = "请营养价值和健康影响两方面对该食品进行综合评价，并给出饮食建议"
        else:
            user = crud.get_user(db, username)

            if user is None:
                content = "请营养价值和健康影响两方面对该食品进行综合评价，并给出饮食建议"
            else:
                content = "请营养价值和健康影响两方面对该食品进行综合评价，另外我是一名"
                if user.age:
                    content += str(user.age) + "岁，"
                if user.height:
                    content += "身高" + str(user.height) + "cm，"
                if user.weight:
                    content += "体重" + str(user.weight) + "kg，"
                if user.allergy is not None and len(user.allergy) > 0:
                    content += "对"
                    for allergy in user.allergy:
                        if allergy != "其他":
                            content += allergy + "，"
                        else:
                            if user.allergyOther:
                                content += user.allergyOther
                    content += "过敏，"

                if user.disease is not None and len(user.disease) > 0:
                    content += "有"
                    for disease in user.disease:
                        if disease != "其他":
                            content += disease + "，"
                        else:
                            if user.diseaseOther:
                                content += user.diseaseOther

                if user.goals and user.goals != "无":
                    content += "，体重目标为" + user.goals

                if user.need is not None and len(user.need) > 0:
                    content += "，饮食需求为"
                    for need in user.need:
                        if need != "其他":
                            content += need + "，"
                        else:
                            if user.needOther:
                                content += user.needOther

                if user.gender:
                    content += "的" + user.gender + "性，是否推荐我食用该食品？"

        result = client.chat.completions.create(
            model="glm-3-turbo",
            messages=[
                role,
                {
                    "role": "user",
                    "content": f"""
                    以下是某食品的配料表：{foodListText}，
                   {content},
                   返回html格式的文本，加粗重点部分，对健康不利的部分用红色字体
                    """
                }
            ],
            temperature=0.01,
            stream=False,
        )
        result = json.loads(result.json())
        if result.get("choices") is not None:
            return result["choices"][0]["message"]["content"]
        else:
            return "解析失败！"
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))


# ---------登陆注册---------登陆注册---------登陆注册---------登陆注册---------登陆注册---------登陆注册---------登陆注册
# 登陆
@app.post("/login", tags=["登陆注册"], summary="登陆")
def login(data: schemas.userModel, db: Session = Depends(get_db)):
    try:
        user = crud.get_user(db, data.username)
        if user is None:
            return "用户不存在，请先注册！"
        else:
            if user.password != data.password:
                return "账号或密码错误"
            else:
                return "登陆成功"
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))


# 注册
@app.post("/register", tags=["登陆注册"], summary="注册")
def register(data: schemas.userModel, db: Session = Depends(get_db)):
    try:
        user = crud.get_user(db, data.username)
        if user is None:
            return crud.register(db, data)
        else:
            return "用户名已存在"
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))


# ---------用户表操作---------用户表操作---------用户表操作---------用户表操作---------用户表操作---------用户表操作
# 获取单个用户数据
@app.get("/user", tags=["用户表操作"], summary="获取单个用户数据")
async def get_user(username: str, db: Session = Depends(get_db)):
    return crud.get_user(db, username)


# 修改用户数据
@app.post("/user", tags=["用户表操作"], summary="修改用户数据")
async def set_user(data: schemas.userModel, db: Session = Depends(get_db)):
    try:
        return crud.set_user(db, data)
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 新增用户数据
@app.post("/addUser", tags=["用户表操作"], summary="新增用户数据")
async def add_user(data: schemas.userModel, db: Session = Depends(get_db)):
    try:
        if crud.get_food(db, data.username):
            raise HTTPException(status_code=401, detail="该用户已存在")
        else:
            crud.add_user(db, data)
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 修改用户数据
@app.post("/setFood", tags=["用户表操作"], summary="修改配料数据")
async def set_user(data: schemas.userModel, db: Session = Depends(get_db)):
    try:
        if crud.get_user(db, data.username):
            crud.set_user(db, data)
        else:
            raise HTTPException(status_code=401, detail="该用户不存在！")
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 删除用户数据
@app.get("/delUser", tags=["用户表操作"], summary="删除用户数据")
async def del_user(username: str, db: Session = Depends(get_db)):
    try:
        crud.del_user(db, username)
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 查询用户表长度
@app.get("/userTotal", tags=["用户表操作"], summary="查询用户表长度")
async def get_user_total( db: Session = Depends(get_db)):
    return crud.get_user_total(db)

# 分页查询用户数据
@app.get("/userPage", tags=["用户表操作"], summary="分页查询用户数据")
async def get_user_page(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_user_page(db, skip, limit)

# ---------配料表操作---------配料表操作---------配料表操作---------配料表操作---------配料表操作---------配料表操作
# 查询配料数据
@app.get("/food", tags=["配料表操作"], summary="查询配料数据")
async def get_food(name: str, db: Session = Depends(get_db)):
    return crud.get_food(db, name)

# 新增配料数据
@app.post("/addFood", tags=["配料表操作"], summary="新增配料数据")
async def add_food(data: schemas.foodModel, db: Session = Depends(get_db)):
    try:
        if crud.get_food(db, data.name):
            raise HTTPException(status_code=401, detail="该配料已存在")
        else:
            crud.add_food(db, data)
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 修改配料数据
@app.post("/setFood", tags=["配料表操作"], summary="修改配料数据")
async def set_food(data: schemas.foodModel, db: Session = Depends(get_db)):
    try:
        if crud.get_food(db, data.name):
            crud.set_food(db, data)
        else:
            raise HTTPException(status_code=401, detail="该配料不存在！")
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 删除配料数据
@app.get("/delFood", tags=["配料表操作"], summary="删除配料数据")
async def del_food(name: str, db: Session = Depends(get_db)):
    try:
        crud.del_food(db, name)
    except Exception as e:
        raise HTTPException(status_code=401, detail="代码报错" + str(e))

# 查询食品表长度
@app.get("/foodTotal", tags=["配料表操作"], summary="查询食品表长度")
async def get_food_total( db: Session = Depends(get_db)):
    return crud.get_food_total(db)

# 分页查询配料数据
@app.get("/foodPage", tags=["配料表操作"], summary="分页查询配料数据")
async def get_food_page(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_food_page(db, skip, limit)