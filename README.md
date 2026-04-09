# 天气查询智能体 · Weather Agent
基于大模型 Function Calling 工具调用实现的智能问答助手

## 项目介绍
本项目实现了一个能够自主判断是否调用工具的智能体，能够根据用户问题自动选择是否查询实时天气，并调用大模型进行自然语言回答。

## 技术栈
- 大模型：智谱 AI / 百炼（通义千问）
- 工具调用：Function Calling
- 前端界面：Gradio
- 环境管理：python-dotenv

## 功能
- 自动识别是否需要查询天气
- 调用天气接口获取实时数据
- 多模型自由切换
- 简洁易用的 Web 界面

## 项目结构
```python
main.py              # 项目入口，Gradio 界面
zhipu.py             # 智谱模型调用
bailian.py           # 百炼模型调用
weather.py           # 天气查询工具
tool_config.py       # 工具定义与配置
.env                 # 密钥配置
requirements.txt     # 依赖列表
