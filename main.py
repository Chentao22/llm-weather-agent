import gradio as gr
from models.zhipu_model import chatglm_tools
from models.qwen_model import qwen_tools
def chatbot_interface(model_platform,query,model_name,temperature,max_tokens):
    response=''
    if model_platform =="ZhipuAI":
        response=chatglm_tools(query,model_name,temperature,max_tokens)
    elif model_platform =="Bailian":
        response = qwen_tools(query, model_name, temperature, max_tokens)
    return response
#构建前端页面
def update_dropdown(model_platform):
    if model_platform == "ZhipuAI":
        return gr.update(choices=["glm-4","glm-4-flash","glm-4-plus"],value="glm-4")
    elif model_platform == "Bailian":
        return gr.update(choices=["qwen2.5-72b-instruct","qwen2.5-32b-instruct","qwen2.5-14b-instruct"],value="qwen2.5-72b-instruct")

with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("#实战：天气查询助手(Function Calling)")
    with gr.Row():
        with gr.Column(scale=2):
            query = gr.Textbox(label="请输入：",lines=8)
            submit = gr.Button("提交")
        with gr.Column(scale=1):
            model_platform = gr.Radio(["ZhipuAI", "Bailian"], label="大模型平台",value="ZhipuAI")
            model_name = gr.Dropdown(["glm-4"], label="模型名称",value="glm-4")
            temperature = gr.Slider(minimum=0, maximum=1, label="temperature", value=0.8)
            max_tokens = gr.Slider(minimum=0, maximum=2048, label="max_tokens", value=512)
            model_platform.change(fn=update_dropdown,inputs=model_platform,outputs=model_name)
    with gr.Row():
        output = gr.Textbox(label="模型回复")
    with gr.Row():
        gr.Examples(["今天信阳天气怎么样？","今天信阳空气质量如何？","未来几天信阳天气怎么样？"],[query])
    submit.click(fn=chatbot_interface,inputs=[model_platform,query,model_name,temperature,max_tokens],outputs=output)
demo.launch()