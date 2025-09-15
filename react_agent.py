# 第一个 agent  v0.3版本
from langchain.agents import AgentType,initialize_agent,create_react_agent,AgentExecutor
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os



load_dotenv()


# 定义llm
llm = ChatOpenAI(
    temperature=0,
    model='deepseek-chat',
    base_url='https://api.deepseek.com/v1',
    # 淘宝购买api 下面为中转网址
    # base_url='https://www.chataiapi.com/v1',
    # model='gpt-3.5-turbo'
    api_key=os.getenv('deepseek_api_key')
    )


# serpapi是谷歌搜索引擎，后面是llm自带数学计算
tools = load_tools(tool_names=['serpapi', 'llm-math'], llm=llm)
tool_names=[tool.name for tool in tools]

# 设置提示模板 不要加f，会立即计算变量值
template=('''请用中文回答以下问题。如果能力不足，你可以使用以下工具：
{tools}
请严格按照以下格式进行回应：
Question: {input}
Thought: 你的思考过程
Action: 需要采取的行动，必须是 [{tool_names}] 中的一个"
Action Input: 行动的输入参数，如果需要计算，则提炼出纯数字进行计算，不要带有逻辑判断。
Observation: 行动的结果

...(这个循环可以重复N次，直到获得最终答案，然后停止)

当你获得上述信息后，停止循环，进入以下流程，给出简介明了的答案：
Action: 在这里输入你知道的答案
Thought: 我已经知道答案，现在停止检索，停止循环，并输出答案。
Action Input: 对原始问题的最终回答，回答之后就结束循环，不要一直重复同样的流程。


{agent_scratchpad} ''')
prompt = PromptTemplate.from_template(template)

# agent = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,  # 是否打印日志
#     handle_parsing_errors=True
#     )

#初始化Agent
agent=create_react_agent(llm,tools,prompt)
#构建AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools,handle_parsing_errors=True,verbose=True)

question = '我国现任主席是哪位？他目前多少岁了？计算到今年25年8月份'
try:
    result = agent_executor.invoke({'input': question})
    print(result['output'])
except Exception as e:
    print(f'执行出错:{e}')