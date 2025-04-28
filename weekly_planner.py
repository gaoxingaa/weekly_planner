# 文件名：weekly_planner.py

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# --------- 加载环境变量，读取 OPENAI_API_KEY ---------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --------- 初始化 OpenAI 客户端 ---------
client = OpenAI(api_key=api_key)


# --------- 页面标题 ---------
st.title("🗓️ AI自动生成周计划助手")

# --------- 用户输入部分 ---------
user_tasks = st.text_area(
    "请输入你的本周目标或任务（每行一个任务）：",
    height=200,
    placeholder="例如：\n- 完成AI小项目\n- 读完一本书\n- 运动三次"
)

# --------- 生成按钮 ---------
if st.button("生成周计划"):

    if not user_tasks.strip():
        st.warning("请输入至少一个任务！")
    else:
        with st.spinner("AI正在规划中，请稍等..."):

            # --------- 构建Prompt ---------
            prompt = f"""
你是一个专业的时间管理顾问。
请根据下面列出的任务，帮我制定一个详细的一周计划。
要求：
- 每天安排2-4个任务
- 每天工作时间控制在4-6小时
- 用表格形式展示（日期｜任务｜预计时间｜优先级）
- 计划从周一开始，到周日结束
任务列表：
{user_tasks}
"""

            try:
                # --------- 调用OpenAI Chat Completions ---------
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一个擅长时间管理的专业助手。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=800
                )

                # 提取返回内容
                plan_text = response.choices[0].message.content
                st.success("生成完成！🎉")
                st.markdown(plan_text)

                # --------- 下载按钮 ---------
                st.download_button(
                    label="📄 下载周计划为TXT文件",
                    data=plan_text,
                    file_name="weekly_plan.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"出错了！请检查API Key或者网络连接。\n\n错误详情：{str(e)}")
