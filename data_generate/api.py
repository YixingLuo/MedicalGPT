import requests
import json

API_KEY = "PTCwzCihbJqy88Vqc1x0Qf28"
SECRET_KEY = "kFWEbMgLgZsWNnOa9pnNpQwUw7B52R5v"

def get_access_token():
    """
    使用 API 密钥和密钥生成认证令牌。
    :return: 成功时返回访问令牌，错误时返回 None。
    """
    # 获取访问令牌的 URL
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",  # 授权类型
        "client_id": API_KEY,                # API 密钥
        "client_secret": SECRET_KEY          # 密钥
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("获取访问令牌时出错:", response.text)
        return None

def get_response_for_prompt(prompt, llm='wenxin-3.5-8k'):
    """
    将给定的提示发送给文心一言 API，并返回 API 的响应。
    :param prompt: 发送给 API 的提示。
    :return: API 响应的字符串形式。
    """
    access_token = get_access_token()
    if not access_token:
        return "获取访问令牌失败。"
    
    # 构建完整的 API 请求 URL，包含获取的访问令牌
    params = {}
    if llm == 'wenxin-3.5-8k':
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",         # 用户角色
                    "content": prompt       # 用户输入的提示
                },
            ],
            "top_p": 0,
            "disable_search": False,    # 是否禁用搜索
            "enable_citation": False    # 是否启用引用
        })
    elif llm == 'chatglm2-6b-32k':
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + get_access_token()
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",         # 用户角色
                    "content": prompt       # 用户输入的提示
                },
            ],
        })
    elif llm == 'codellama-7b-instrct-16k':
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/completions/codellama_7b_instruct?access_token=" + get_access_token()
        payload = json.dumps({
            "prompt": prompt,
            # "top_p": 0
        })
    
    
    
    # 构建请求负载，其中包含用户的提示
    headers = {
        'Content-Type': 'application/json'
    }
    
    # 发送 POST 请求给 API
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        try:
            return response.json()['result'].strip()
        except json.JSONDecodeError:
            return "解析响应失败。"
    else:
        return f"API 请求失败，状态码 {response.status_code}: {response.text}"

# 示例用法
prompt = "你好" 
response = get_response_for_prompt(prompt)
print(response)