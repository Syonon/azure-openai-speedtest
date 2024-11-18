import csv
import os
from time import sleep

import requests


# 入力プロンプト配列
prompts_list = [
    "",
    "",
]


def send_request_to_azure_openai(api_key: str, endpoint: str, payload: dict)-> requests.Response:
    """
    Azure OpenAIにリクエストを送信し、レスポンスを返す。
    :param api_key: APIキー
    :param endpoint: エンドポイントURL
    :param payload: リクエストペイロード
    :return: requests.Responseオブジェクト
    """
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")
        return None  # エラーが発生した場合はNoneを返す

    return response


if __name__ == "__main__":

    API_KEYS = {
        "4jp": os.getenv("AOAI_API_KEY"),
        "4ojp": os.getenv("AOAI_API_KEY"),
        "4ous": os.getenv("AOAI_API_KEY"),
    }

    ENDPOINTS = {
        "4jp": os.getenv("AOAI_ENDPOINT"),
        "4ojp": os.getenv("AOAI_ENDPOINT"),
        "4ous": os.getenv("AOAI_ENDPOINT"),
    }

    # 出力先CSVのヘッダー
    with open(file="output.csv", mode="a", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["gpt-4-jp", "gpt-4o-jp", "gpt-4o-us"])

    for i, prompt in enumerate(prompts_list):
        response_time_4jp = -1.0  # responseがNoneの場合応答時間は-1を返す
        response_time_4ojp = -1.0
        response_time_4ous = -1.0

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "情報を見つけるのに役立つ AI アシスタントです。",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 2000,
        }

        # for key in ["4jp", "4ojp", "4ous"]:
        for key in ["4ojp"]:
            response = send_request_to_azure_openai(
                API_KEYS[key], ENDPOINTS[key], payload
            )
            if response:
                elapsed_time = response.elapsed.total_seconds()
                if key == "4jp":
                    response_time_4jp = elapsed_time
                elif key == "4ojp":
                    response_time_4ojp = elapsed_time
                else:
                    response_time_4ous = elapsed_time

                with open(
                    file="output.csv", mode="a", encoding="utf-8", newline=""
                ) as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(
                        [response_time_4jp, response_time_4ojp, response_time_4ous]
                    )
