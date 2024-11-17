""" Azure OpenAI GPT-4とGPT-4oの応答速度比較 """

import requests
import time

# Azure OpenAIの設定
endpoint = "https://<your-endpoint>.openai.azure.com/"
api_key = "<your-api-key>"
deployment_ids = ["gpt-4", "gpt-3.5-turbo"]  # 比較したいモデルのデプロイ名
api_version = "2023-05-15"  # 適切なAPIバージョンを指定

# テストに使用するプロンプト
test_prompt = "Explain the difference between supervised and unsupervised learning."

def measure_response_time(deployment_id, prompt):
    url = f"{endpoint}/openai/deployments/{deployment_id}/chat/completions?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        elapsed_time = response.elapsed.total_seconds()
        return elapsed_time, response.json()
    else:
        return None, response.text
