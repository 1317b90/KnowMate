import base64
import json
import shutil
import time
from fastapi.responses import StreamingResponse

import requests
from fastapi import  Depends, File, UploadFile, HTTPException, Request,APIRouter
from sqlalchemy.orm import Session
from openai import OpenAI
from sql import get_db,Base
from mange.food import get_food,add_food_func
from mange.log import add_log
from mange.user import get_user, get_user_info
import AI
import io
import ast
from pydantic import BaseModel
from typing import List, Literal


app = APIRouter(tags=["解析配料"])

# ---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr---------ocr
# 从ocr结果中提取配料列表
def get_foodList(ocrText):
    nowTime = time.time()
    print(ocrText)
    messages=[
            {
                "role": "system",
                "content": """
# 角色
你是一位专业的食品安全审查员，负责从食品配料表文本中提取配料并进行校对。

# 任务
1.  **精准提取：** 从用户提供的配料表文本中精确提取所有配料名称。
2.  **错误修正：** 修正识别错误，包括错别字和 OCR 误差导致的拼写错误。
3.  **格式化输出：** 返回结果的格式为一个Json格式的纯粹的 Python 列表（`['配料1', '配料2', ..., '配料N']`），列表中每项配料之间用英文逗号分隔，列表之外不包含任何多余的说明和文字。
4.  **无配料处理：** 如果文本中不包含任何配料，则仅返回文本"无配料"。

# 规则
1.  **仅提取配料：** 只提取配料的名称，忽略任何其他信息，如百分比含量、数字、附加说明等。
2.  **标准列表格式：** 确保返回的格式严格符合标准的 Python 列表形式。
3.  **精确校对：** 努力达到最高的配料名称识别和校对准确性。

# 示例输入：
'糖，盐，鸡精，谷朊粉，防腐剂（山梨酸钾），天然色素（红曲米）'

# 示例输出：
['糖', '盐', '鸡精', '谷朊粉', '山梨酸钾', '红曲米']

# 补充说明：
* 请严格按照示例输出的格式进行输出。
* 请注意一些配料的名称可能会包含括号，请保留括号内的内容。
"""
            },
            {
                "role": "user",
                "content":ocrText
            }
        ]
    result = AI.chat(
        messages=messages,
        isJson=True,
    )
    if "无配料" in result:
        raise HTTPException(400,"上传的不是一张配料表图片!")
    try:
        return ast.literal_eval(result)
    except:
        raise HTTPException(500,"AI识别列表失败!")

# 接收图片并进行ocr识别
@app.post("/ocrImg", tags=["ocr识别"],summary="上传图片进行ocr识别")
def ocr_img(file: UploadFile = File(...)):
    # 检查文件大小是否超过10MB
    if file.size > 10 * 1024 * 1024:  # 10MB in bytes
        raise HTTPException(status_code=400, detail="文件大小不能超过10MB")

    # 检查文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只能上传图片文件")

    # 读取文件内容并转换为base64
    contents = file.file.read()
    base64_image = base64.b64encode(contents).decode('utf-8')

    # 获取图片格式
    image_format = file.content_type.split('/')[-1]

    # 根据图片格式构建img_url
    img_url = {"url": f"data:image/{image_format};base64,{base64_image}"}

    return get_foodList(AI.ocr(img_url))

# ----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析----------配料解析
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
        add_log(logDict)
        return Food

    # 如果不存在，当即查询
    else:
        foodRuler = getRuler(foodName)
        result = AI.chat(
            messages=[
                {
                    "role": "system",
                    "content": """
# 角色
你是一位专业的食品配料分析师，擅长基于权威科学研究、食品安全标准或行业共识，为指定的食品配料生成专业分析报告。你的报告需确保内容的科学性与客观性。

## 技能
### 技能1: 食品配料识别
- 判断用户的输入是否是一项食品配料，并用布尔值表示。
- 根据《食品添加剂使用标准》或国际食品分类系统确定食品配料的类别。

### 技能2: 食品配料简介
- 描述食品配料的化学特性、自然存在形式及工业制备方式（如适用）。
- 以通俗易懂的语言进行描述，避免使用专业术语，但保持表述严谨。

### 抗能3: 食品配料的作用
- 分析食品配料在食品中的物理、化学、生物等不同作用机制。
- 确保分析内容基于可验证的科学研究数据或官方食品安全文件。

### 技能4: 健康影响评估
- 根据EFSA（欧洲食品安全局）、FDA（美国食药监局）或中国卫健委最新评估结论，判断食品配料对人体是否有害或有益。
- 提供明确的科学依据来支持有害或有益的结论，否则标记为不确定。
- 引用的研究数据应优先采用最近5年内的数据，并注明研究机构和研究年份。

### 技能5: 风险提示
- 对明确存在的不良反应进行风险提示，包括敏感人群、典型症状和安全摄入量。
- 区分普通人群和特殊人群的风险差异。
- 如果无明确的风险，请保持空值。

## 限制
- 所有信息必须基于可验证的科学研究数据或官方食品安全文件。
- 当存在学术争议时，应说明不同研究结论并保持中立立场。
- 数值指标需注明出处及研究年份。
- 使用通俗语言避免专业术语，但需保持表述严谨。
- 严格遵循以下Python的JSON格式，使用中文输出：

```json
{
    "是否是食品配料": "判断用户的输入是否是一项食品配料，用布尔值表示",
    "类别": "根据《食品添加剂使用标准》或国际食品分类系统确定",
    "简介": "包含化学特性、自然存在形式、工业制备方式（如适用）",
    "在食品中的作用": "区分物理、化学、生物等不同作用机制",
    "对人体是否有害或有益": "可选值（有害，有益，不确定），需要有非常明确的相应科学依据来证明有害或有益，否则为不确定",
    "有害或有益的科学依据": "根据(研究年份，采用最近5年内数据优先)(研究机构，引用权威机构名称,)提出（结论概要，不超过50字的关键结论,）",
    "风险提示": {
        "敏感人群": "按年龄、生理状态、遗传特征分类说明",
        "典型症状": "列举临床确认的不良反应类型",
        "安全摄入量": "标明体重基准的毫克/千克值"
    }
}
```

- 如某字段无可靠数据支持，请保持空值。
- 对存在剂量依赖性的成分需明确表述阈值效应。
- 需区分普通人群和特殊人群的风险差异。
"""
                },
                {
                    "role":"user",
                    "content":foodName
                }
            ],
            stream=False,
            isJson=True,
        )
        logDict["output"] =result
        resultJson = json.loads(result)
        if not resultJson.get("是否是食品配料"):
            logDict["output"] =foodName+ "不是食品配料"
            logDict["state"]=False
            add_log(logDict)
            raise HTTPException(status_code=401, detail="不是食品配料！")
        risk=resultJson.get("风险提示","")
        riskStr=""
        if type(risk) == dict:
            for key,value in risk.items():
                riskStr+=key+":"+value+"\n"
        else:
            riskStr=risk
        Food = {
            "name":foodName,
            "type":resultJson.get("类别",""),
            "intro":resultJson.get("简介",""),
            "effect":resultJson.get("在食品中的作用",""),
            "harmType":resultJson.get("对人体是否有害或有益",""),
            "harmReason":resultJson.get("有害或有益的科学依据",""),
            "risk":riskStr,
            "ruler":foodRuler
        }
        add_food_func(Food)
        add_log(logDict)
        return Food



# 食品评价与饮食建议
@app.get("/feadr", tags=["解析配料"], summary="食品评价与饮食建议")
def get_feadr(foodListText: str,username: str = '访客'):
    def chat_feadr(foodListText,user_info=None):
        content="食品配料表："+foodListText+"\n"
        if user_info:
            content += "请从营养价值和健康影响两方面对该食品进行综合评价，另外我是一名"+user_info+",是否推荐我食用该食品？"
        else:
            content += "请从营养价值和健康影响两方面对该食品进行综合评价，并给出饮食建议"

        response = AI.chat(
            messages=[
                {
                "role": "system",
                "content": """
                你是一个食品配料方面的专家，拥有广泛的食品科学知识和营养学背景。
                你的任务是为用户提供食品配料相关的专业、准确、具体、有见地的解释和建议，帮助他们理解和解析食品配料表。
                # 请注意：
                1.  **严重注意！无需对每一项配料进行详细解释**。
                2.  重点关注整体的营养价值和健康影响。
                3.  挑重点说，只用**重点叙述营养价值较高和健康影响较大的部分**，不用一一叙述
                4.  给出综合的饮食评价，例如是否应该少吃，以及过量食用可能带来的影响
                5.  用markdown语法叙述
                """
            },
                {
                    "role": "user",
                    "content": content
                }
            ],
            stream=True,
        )

        for chunk in response:
            try:
                text_chunk = chunk.choices[0].delta.content
                if text_chunk is not None:
                    yield text_chunk
            except:
                yield ""

    user_info = get_user_info(username )

    return StreamingResponse(chat_feadr(foodListText,user_info), media_type="text/plain")




class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "error"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/chat", tags=["解析配料"], summary="聊天")
def get_chat(request: ChatRequest):
    # 过滤掉error类型的消息和空内容的消息
    filtered_messages = [
        msg.model_dump() 
        for msg in request.messages 
        if msg.role != "error" and msg.content.strip()
    ]
    
    system_messages=[
        {
            "role": "system",
            "content": """
# 角色：
 - 你是一位专业的食品配料专家，负责解答用户关于食品配料的疑问
# 知识：
 - 你的知识涵盖食品添加剂、成分、加工助剂、来源、功能、安全性和法规标准
# 原则：
 - 基于科学事实和权威来源回答，提供详细解释，使用通俗易懂的语言
 - 严格遵守中国的食品安全法律法规，特别是关于食品添加剂和配料使用的规定
            """
        }
    ]

    messages = system_messages + filtered_messages
    def chat_feadr(messages):
        response = AI.chat(
            messages=messages,
            stream=True,
            isJson=False,
        )

        for chunk in response:
            try:
                text_chunk = chunk.choices[0].delta.content
                if text_chunk is not None:
                    yield text_chunk
            except:
                yield ""

    return StreamingResponse(chat_feadr(messages), media_type="text/plain")