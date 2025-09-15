# plan_and_execute 框架
import langchain
from langchain.agents import AgentType,initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.chains import LLMMathChain
from langchain.schema import SystemMessage
from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute,load_chat_planner,load_agent_executor
from langchain_core.tools import Tool
from dotenv import load_dotenv
import os
load_dotenv()
llm = ChatOpenAI(temperature=0.3,model='deepseek-chat',base_url='https://api.deepseek.com/v1', api_key=os.getenv('DEEPSEEK_API_KEY'))
search = SerpAPIWrapper()
llm_math_chain=LLMMathChain.from_llm(llm=llm,verbose=True)

tools=[Tool(name='search',func=search.run,description='用于回答问题'),Tool(name='Caculator',func=llm_math_chain.run,
    description='用于计算解决问题')]
print(tools)
memory = ConversationBufferMemory(memory_key='chat-history',return_messages=True)
# planner=load_chat_planner(llm)
# executor=load_agent_executor(llm,tools,verbose=True)
# agent1=PlanAndExecute(planner=planner,executor=executor,verbose=True)
agent_chain=initialize_agent(tools,llm,agent=AgentType.OPENAI_FUNCTIONS,memory=memory,verbose=True)
question='在北京，100元能买几朵茉莉花?如果搜索出多个价格，用最低价，请用中文回答'
question1='我们刚刚说的很好，对吗'
result=agent_chain.invoke({'input':question})
# result1=agent_chain.invoke({'input':question1})
# print(result['output'])


