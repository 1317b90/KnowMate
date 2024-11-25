import base64
import json
import shutil
import time
from fastapi.responses import StreamingResponse

import requests
from fastapi import  Depends, File, UploadFile, HTTPException, Request,APIRouter
from sqlalchemy.orm import Session
from zhipuai import ZhipuAI
from sql import get_db,Base
from food import get_food,add_food
from log import add_log
from user import get_user, get_user_info
app = APIRouter()
client = ZhipuAI(api_key="28698839aff97f518ef798ee22384d74.zrQb5Xa9s7QicZMP")


# 百度ocr的token
ocrToken="24.e9986dfe2aecedda2bee6f505b437269.2592000.1729494390.282335-55556153"
apiKey = "FWKwWT9J0yQrmLpoODrgAVWF"
secretKey = "3cFDSoogWETTNPpkckdINBpVCXAj6Cq8"  

# ---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr
# 从ocr结果中提取配料列表
def get_foodList(ocrText):
    nowTime = time.time()
    result = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "system",
                "content": """
# 角色
你是一位专业的食品安全审查员，负责从 OCR 识别的食品配料表中提取配料并进行校对。

# 任务
从用户提供的 OCR 识别结果中提取所有配料，修正识别错误，确保每项配料准确无误。返回结果的格式为一个配料列表（`['配料1', '配料2', ..., '配料N']`），列表中每项配料之间用英文逗号分隔，列表之外不需要包含任何多余的说明和文字。

# 规则
- 修正错别字或因 OCR 误差产生的拼写错误
- 只提取配料名称，忽略多余信息（如百分比含量、数字等）
- 确保返回的格式为标准的 Python 列表形式

# 示例输入：
'糖，盐，鸡精，谷朊粉，防腐剂（山梨酸钾），天然色素（红曲米）'

# 示例输出：
['糖', '盐', '鸡精', '谷朊粉', '山梨酸钾', '红曲米']
"""
            },
            {
                "role": "user",
                "content":ocrText
            }
        ],
        temperature=0.01,
        stream=False,
    )
    result = json.loads(result.json())
    print("AI识别列表用时：",time.time()-nowTime)


    if result.get("choices") is not None:
        resultList = eval(result["choices"][0]["message"]["content"])
        return [{"id": i, "name": resultList[i], "editing": False} for i in range(len(resultList))]
    else:
        raise HTTPException(status_code=401, detail="配料列表提取失败")


# 更新token的装饰器
def update_ocr_token(func):
    def wrapper(*args, **kwargs):
        global ocrToken
        result = func(*args, **kwargs)
        if result == "token失效":
            url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
            payload = ""
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                response = response.json()
                ocrToken = response.get("access_token")
                return func(*args, **kwargs)
            else:
                raise HTTPException(status_code=504, detail="更新token失败")
        return result
    return wrapper


# 读取图片并进行ocr识别
@update_ocr_token
def get_ocr_text(file_path):
    nowTime = time.time()
    # 读取保存的图片文件
    with open(file_path, "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode()
    
    params = {"image": img_base64, "probability": "true"}

    # accurate_basic 高精度
    # general_basic 基础版
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + ocrToken
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    
    if response.status_code == 200:
        response = response.json()
        error_msg = response.get("error_msg")
        if error_msg:
            if "token" in error_msg:
                return "token失效"
            else:
                raise HTTPException(status_code=504, detail=error_msg)
        else:
            # 总准确度
            probabilitys = 0
            # 总识别文字
            words = ""
            # 总识别行数
            i = 0
            for wordJson in response['words_result']:
                words += wordJson.get("words")
                probabilitys += wordJson.get("probability")['average']
                i += 1
            if i == 0:
                raise HTTPException(status_code=504, detail="图片中没有识别到任何文字")
            elif probabilitys / i < 0.85:
                raise HTTPException(status_code=504, detail="图片识别精度过低，请重新上传")
            else:
                print("OCR用时：",time.time()-nowTime)
                return get_foodList(words)
    else:
        raise HTTPException(status_code=504, detail="图片识别请求失败，请重试！")

# 接收图片并进行ocr识别
@app.post("/ocrImg", tags=["ocr识别"],summary="上传图片进行ocr识别")
def ocr_img(file: UploadFile = File(...)):
    # 生成唯一的文件名
    filename = f"{int(time.time())}-{file.filename}"
    file_path = f"./images/up/{filename}"
    
    # 保存上传的图片
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return get_ocr_text(file_path)

@app.get("/ocrImg", tags=["ocr识别"],summary="识别测试图片")
def ocr_img_test(fileName:str):
    return get_ocr_text(f"./images/test/{fileName}")




# ----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析

# 角色定位
role = {
    "role": "system",
    "content": """
    你是一个食品配料方面的专家，拥有广泛的食品科学知识和营养学背景。
    你的任务是为用户提供食品配料相关的专业、准确、具体、有见地的解释和建议，帮助他们理解和解析食品配料表。
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
@app.get("/parsing", tags=["解析配料"], summary="解析单项配料")
def get_parsing(foodName, request: Request, username: str = '访客', db: Session = Depends(get_db)):
    # 查询数据库中是否存在
    Food = get_food(foodName,db )

    # 记录
    logDict={
        "ip":request.client.host,
        "state":True,
        "username":username,
        "type":"parsing",
        "input":foodName
    }

    # 如果存在，直接返回结果
    if Food:

        logDict["output"]= "从数据库中返回结果"
        add_log(db, logDict)
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
                Food = {
                    "name":foodName,
                    "type":resultJson.get("类别"),
                    "intro":resultJson.get("简介"),
                    "effect":resultJson.get("在食品中的作用"),
                    "harmType":resultJson.get("对人体是否有害或有益"),
                    "harmReason":resultJson.get("对人体有害或有益或不确定的原因"),
                    "out":resultJson.get("不适宜人群"),
                    "ruler":foodRuler
                }
                add_food(db, Food)

                logDict["output"] = json.dumps(Food.dict())
                add_log(db, logDict)

                # 为啥要加这一句？我也不知道，反正不加就会报错
                print(Food.name)
                return Food
            else:
                logDict["output"] ="配料解析失败"
                logDict.state = False
                add_log(db, logDict)

                raise HTTPException(status_code=400, detail="配料解析失败！")
        else:
            logDict["output"] = "不是一项食品配料"
            logDict.state = False
            add_log(db, logDict)

            raise HTTPException(status_code=444, detail="不是一项食品配料！")


def chat_feadr(foodListText,user_info=None):
    content="食品配料表："+foodListText+"\n"
    if user_info:
        content += "请从营养价值和健康影响两方面对该食品进行综合评价，另外我是一名"+user_info+",是否推荐我食用该食品？"
    else:
        content += "请从营养价值和健康影响两方面对该食品进行综合评价，并给出饮食建议"

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
            "role": "system",
            "content": """
            你是一个食品配料方面的专家，拥有广泛的食品科学知识和营养学背景。
            你的任务是为用户提供食品配料相关的专业、准确、具体、有见地的解释和建议，帮助他们理解和解析食品配料表。
            """
        },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=0.01,
        stream=True,
    )

    for chunk in response:
        try:
            text_chunk = chunk.choices[0].delta.content
        except:
            text_chunk = ""
        yield text_chunk
     

# 食品评价与饮食建议
@app.get("/feadr", tags=["解析配料"], summary="食品评价与饮食建议")
def get_feadr(foodListText: str,request: Request,username: str = '访客', db: Session = Depends(get_db)):
    # 记录
    logDict = {
        "ip": request.client.host,
        "state": True,
        "username": username,
        "type": "feadr",
    }


    user_info = get_user_info(username,db )

    return StreamingResponse(chat_feadr(foodListText,user_info), media_type="text/plain")