import json
from zhipuai import ZhipuAI
from tools.tool_config import weather_tools
from tools.weather import get_current_weather, get_future_weather
import os
from dotenv import load_dotenv
load_dotenv()
def chatglm_tools(query,model_name,temperature,max_tokens):
    client=ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"),)
    messages=[{"role":"user","content":query}]
    resp = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=weather_tools,
        messages=messages)
    # print(resp)
    if resp.choices[0].message.tool_calls !=None:
        args = resp.choices[0].message.tool_calls[0].function.arguments
        if resp.choices[0].message.tool_calls[0].function.name=="get_current_weather":
            city = json.loads(args)["city"]
            weather_info = get_current_weather(city)
            #第二次调用
            messages.append({"role": "tool",
                         "content":json.dumps(weather_info),
                         "tool_call_id": resp.choices[0].message.tool_calls[0].id})
            final_resp = client.chat.completions.create(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=messages)
            result = final_resp.choices[0].message.content
            return result
        elif resp.choices[0].message.tool_calls[0].function.name=="get_future_weather":
            city = json.loads(args)["city"]
            weather_info = get_future_weather(city)
            # 第二次调用
            messages.append({"role": "tool",
                             "content": json.dumps(weather_info),
                             "tool_call_id": resp.choices[0].message.tool_calls[0].id})
            final_resp = client.chat.completions.create(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=messages)
            result = final_resp.choices[0].message.content
            return result

    else:
        return resp.choices[0].message.content