import asyncio
import os

from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from load_dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model='deepseek-chat',base_url='https://api.deepseek.com/v1',api_key=os.getenv('DEEPSEEK_API_KEY'))

# 同步流调用
# chunks = []
# for chunk in model.stream('天空是什么颜色?'):
#     chunks.append(chunk)
#     print(chunk.content ,end='|',flush=True)

#异步流调用 必须要用async 定义一个方法
# async def async_stream():
#     chunks = []
#     async for chunk in model.astream('天空是什么颜色?'):
#         chunks.append(chunk)
#         print(chunk.content ,end='|',flush=True)
# #运行异步流处理
# asyncio.run(async_stream())

#链式异步调用
# prompt = ChatPromptTemplate.from_template('给我讲一个关于{topic}的故事')
# parser = StrOutputParser()
# chain = prompt | model | parser
# async def async_stream():
#     chunks = []
#     async for chunk in chain.astream({'topic':'鸵鸟'}):
#         chunks.append(chunk)
#         print(chunk,end='|',flush=True)
# asyncio.run(async_stream())

#JSON格式输出
# parser = JsonOutputParser()
# chain = model | parser
# async def async_stream():
#     async for text in chain.astream(
#         "使用JSON输出法国、西班牙国家的人口数"
#         "使用一个带有'countries'外部键的字典，其中包含国家列表"
#         "每个国家都应该有键'name'和'population'"
# ):
#         print(text,flush=True )
# asyncio.run(async_stream())

#监听聊天模型产生的事件
# async def async_event():
#     events = []
#     async for event in model.astream_events('hello',version='v2'):
#                 events.append(event)
#     print(events)
# asyncio.run(async_event())

# 三种日志打印  verbose详细日志打印，debug调试日志打印，langsmith链路调用跟踪