import time
from curl_cffi import requests

CAPSOLVER_API_KEY = "your api key"
PAGE_URL = "https://visa.vfsglobal.com/npl/en/ltp/login"
WEBSITE_KEY = "0x4AAAAAAACYaM3U_Dz-4DN1"

def solvecf(metadata_action=None, metadata_cdata=None):
    url = "https://api.capsolver.com/createTask"
    task = {
        "type": "AntiTurnstileTaskProxyLess",
        "websiteURL": PAGE_URL,
        "websiteKey": WEBSITE_KEY,
    }
    if metadata_action or metadata_cdata:
        task["metadata"] = {}
        if metadata_action:
            task["metadata"]["action"] = metadata_action
        if metadata_cdata:
            task["metadata"]["cdata"] = metadata_cdata
    data = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": task
    }
    response_data = requests.post(url, json=data).json()
    print(response_data)
    return response_data['taskId']


def solutionGet(taskId):
    url = "https://api.capsolver.com/getTaskResult"
    status = ""
    while status != "ready":
        data = {"clientKey": CAPSOLVER_API_KEY, "taskId": taskId}
        response_data = requests.post(url, json=data).json()
        print(response_data)
        status = response_data.get('status', '')
        print(status)
        if status == "ready":
            return response_data['solution']

        time.sleep(2)


def main():
    start_time = time.time()
    
    taskId = solvecf()
    solution = solutionGet(taskId)
    if solution:
        user_agent = solution['userAgent']
        token = solution['token']

    print("User_Agent:", user_agent)
    print("Solved Turnstile Captcha, token:", token)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time to solve the captcha: {elapsed_time} seconds")

if __name__ == "__main__":
    main()
