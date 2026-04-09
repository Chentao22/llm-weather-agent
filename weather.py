import requests
from dotenv import load_dotenv
import os
load_dotenv()
def get_current_weather(city):
    # 接口请求入参配置
    requestParams = {
        'key': os.getenv('API_KEY'),
        'city': city
    }
    # 发起接口网络请求
    response = requests.get(os.getenv('API_URL'), params=requestParams)
    # 解析响应结果
    if response.status_code == 200:
        responseResult = response.json()
        if responseResult.get("error_code") != 0:
            return {
                "city": city,
                "error": responseResult.get("reason", "接口请求失败，次数可能已用完")
            }
        weather_info={
            "temperature":responseResult["result"]['realtime']["temperature"],
            "humidity":responseResult["result"]['realtime']["humidity"],
            "description":responseResult["result"]['realtime']["direct"]+responseResult["result"]['realtime']["info"],
            "aqi":responseResult["result"]['realtime']["aqi"],
            "city":responseResult["result"]["city"]
        }
        return weather_info
    else:
        return {"city": city, "error": "获取天气失败"}
def get_future_weather(city):
    # 接口请求入参配置
    requestParams = {
        'key': os.getenv('API_KEY'),
        'city': city,
    }
    response = requests.get(os.getenv('API_URL'), params=requestParams)
    # 解析响应结果
    if response.status_code == 200:
        responseResult = response.json()
        if responseResult.get("error_code") != 0:
            return {
                "city": city,
                "error": responseResult.get("reason", "接口请求失败，次数可能已用完")
            }
        weather_info={
             "city": city,
             "future_weather": responseResult["result"]["future"]
        }
        return weather_info
    else:
        print('请求异常')
        return {"city": city, "error": "获取天气失败"}