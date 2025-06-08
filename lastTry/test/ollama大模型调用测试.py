import json

import requests


def generate_with_api(model_name, prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False  # 获取完整响应
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # 处理 x-ndjson 格式（最后一行包含完整结果）
        lines = response.text.strip().split('\n')
        for line in lines:
            if line.strip():
                data = json.loads(line)
                if data.get("done", False):
                    return data.get("response", "")
        return "No response found"

    except requests.exceptions.RequestException as e:
        print(f"API 请求错误: {e}")
        print(f"响应内容: {response.text}")
        return None


model = "qwen2.5:7b"
prompt = "你好，请介绍一下自己"
print(1)
response_text = generate_with_api(model, prompt)


if response_text:
    print(f"模型回复:\n{response_text}")