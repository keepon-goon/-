import requests
import urllib3
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

# 配置信息
API_PASSWORD = "SzBawvfnyoiWpTrtDaYq:JfGdQyYBtAtcvdUullJh"
API_URL = "https://spark-api-open.xf-yun.com/v2/chat/completions"
REQUEST_TIMEOUT = 60  # 超时时间（秒）
MAX_PROMPT_LENGTH = 1000  # 最大输入长度
REQUEST_INTERVAL = 5  # 最小请求间隔（秒）
LAST_REQUEST_TIME = 0

# 敏感词过滤（示例，需根据实际情况配置）
SENSITIVE_WORDS = ["非法", "敏感"]

def check_network():
    """测试网络连通性"""
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', 'https://www.baidu.com', timeout=5)
        if response.status == 200:
            print("✅ 网络连通性正常")
            return True
        else:
            print(f"❌ 网络请求返回状态码: {response.status}")
            return False
    except Exception as e:
        print(f"❌ 网络测试失败: {e}")
        return False

def truncate_prompt(prompt: str) -> str:
    """截断过长的输入"""
    if len(prompt) > MAX_PROMPT_LENGTH:
        print(f"⚠️ 输入内容过长，已截断为前{MAX_PROMPT_LENGTH}字")
        return prompt[:MAX_PROMPT_LENGTH] + "..."
    return prompt

def filter_sensitive_words(prompt: str) -> str:
    """敏感词过滤"""
    for word in SENSITIVE_WORDS:
        if word in prompt:
            raise ValueError(f"❌ 输入包含敏感词: {word}")
    return prompt

def check_request_frequency():
    """控制请求频率"""
    global LAST_REQUEST_TIME
    now = time.time()
    if now - LAST_REQUEST_TIME < REQUEST_INTERVAL:
        wait_time = REQUEST_INTERVAL - (now - LAST_REQUEST_TIME)
        print(f"⏱️ 等待{wait_time:.1f}秒以满足请求频率限制")
        time.sleep(wait_time)
    LAST_REQUEST_TIME = now

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.HTTPError)),
    reraise=True
)
def send_request(prompt: str, history: List[Dict[str, str]] = None) -> str:
    """带重试机制的请求函数"""
    check_request_frequency()
    prompt = truncate_prompt(prompt)
    filter_sensitive_words(prompt)

    headers = {
        "Authorization": f"Bearer {API_PASSWORD}",
        "Content-Type": "application/json",
        "User-Agent": "Spark-X1-Python-Client/1.1"
    }
    payload = {
        "model": "x1",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "max_tokens": 4096,
        "timeout": REQUEST_TIMEOUT  # 传递超时参数给API
    }

    if history:
        payload["messages"] = history + payload["messages"]

    print("\n--- 开始处理请求 ---")
    print(f"用户输入: {prompt}")
    if history:
        print(f"历史对话数量: {len(history)}条")

    try:
        print("正在连接星火大模型...")
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        print("已收到响应，正在解析内容...")
        result = response.json()
        content = result["choices"][0]["message"].get("content", "")

        if not content:
            raise ValueError("响应内容为空")

        print(f"✅ 请求成功 | 消耗Token: {result.get('usage', {}).get('total_tokens', '未知')}")
        return content

    except requests.exceptions.Timeout:
        print("❌ 读取响应超时，正在重试...")
        raise
    except requests.exceptions.HTTPError as e:
        error_msg = f"❌ HTTP错误 {response.status_code}: {response.text}"
        print(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        print(f"❌ 处理请求失败: {str(e)}")
        raise

if __name__ == "__main__":
    if not check_network():
        exit(1)

    user_prompt = "1+1等于几"
    try:
        print(time)
        print(send_request(user_prompt))
        print(time)
    except Exception as e:
        print(f"最终错误: {e}")