import json
import requests

def test_login():
    headers = {
        'Content-Type': 'application/json'
    }
    API_GW = "https://aaw5kr39wf.execute-api.cn-north-1.amazonaws.com.cn/api/"
    account_info = {
        "username": "yaru",
        "password": "intelpass"
    }  
    payload = json.dumps(account_info)
    print(f"payload {payload}")
    response = requests.request("POST", f"{API_GW}/login", headers=headers, data=payload)
    print(response)
    response_body = json.loads(response.text)
    token = response_body["data"]["token"]
    print(token)
    return 1



