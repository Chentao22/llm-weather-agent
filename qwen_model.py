from dashscope import Generation
from tools.tool_config import weather_tools
from tools.weather import get_current_weather, get_future_weather
import json
import os
from dotenv import load_dotenv
load_dotenv()
def qwen_tools(query, model_name, temperature, max_tokens):
    messages = [{"role": "user", "content": query}]
    # 第一次请求
    resp = Generation.call(
        model=model_name,
        api_key=os.getenv('BAILIAN_API_KEY'),
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=weather_tools,
        result_format="message"
    )

    if not resp or not resp.output:
        return "模型调用失败"

    message = resp.output.choices[0].message

    if 'tool_calls' in message:
        tool_call = message.tool_calls[0]
        tool_call_id = tool_call["id"]
        name = tool_call['function']['name']
        args = json.loads(tool_call['function']['arguments'])
        city = args.get("city", "")

        # 执行工具
        if name == "get_current_weather":
            weather_info = get_current_weather(city)
        elif name == "get_future_weather":
            weather_info = get_future_weather(city)
        else:
            return "不支持的工具"

        messages.append(message)  # 把AI的tool_call加进去
        messages.append({
            "role": "tool",
            "content": json.dumps(weather_info, ensure_ascii=False),
            "tool_call_id": tool_call_id
        })

        # 第二次请求：必须带 tools！！！
        final_resp = Generation.call(
            model=model_name,
            api_key=os.getenv('BAILIAN_API_KEY'),
            messages=messages,
            temperature=0.1,
            max_tokens=1024,
            tools=weather_tools,
            result_format="message"
        )
        try:
            return final_resp.output.choices[0].message.content
        except Exception as e:
            print("【AI 解析失败】", e)
            return f"工具调用成功！天气信息：\n{json.dumps(weather_info, ensure_ascii=False, indent=2)}"
    else:
        return message.content