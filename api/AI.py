import os
from openai import OpenAI
import re
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def remove_markdown(text: str) -> str:
    remove_chars = ["#", "**","\n\n","```json","```","\n","\t"," "]
    for char in remove_chars:
        text = text.replace(char, "")

    return text


#bot-20250308105606-5kz7f
def chat(messages:list, stream=False, temperature=0.01, isJson=False):
    base_url="https://api.deepseek.com"
    model="deepseek-chat"
    client = OpenAI(
        base_url=base_url,
        api_key="sk-89d9324fdcda4bbbab5f3bac856e1a07",
    )

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
        temperature=temperature,
        response_format={"type": "json_object" if isJson else "text"}
    )
    if stream:
        return completion
    result=completion.choices[0].message.content
    if isJson:
        result=remove_markdown(result)
        result=result.replace("```json","").replace("```","")
    return result

# ocr
def ocr(url:str):
    client = OpenAI(
        api_key="sk-ecf2758fcf594a08bce088b5ec2bf96a",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-ocr",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": url,
                        "min_pixels": 28 * 28 * 4,
                        "max_pixels": 28 * 28 * 1280
                    },
                    # 为保证识别效果，目前模型内部会统一使用"Read all the text in the image."进行识别，用户输入的文本不会生效。
                    {"type": "text", "text": "Read all the text in the image."},
                ]
            }
        ])

    return completion.choices[0].message.content
