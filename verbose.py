import os

from langchain_openai import ChatOpenAI
#create_tool_calling_agent deepseek无法使用此代理
from langchain.agents import create_tool_calling_agent,AgentExecutor
from langchain_tavily import TavilySearch
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from load_dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(model='deepseek-chat',base_url='https://api.deepseek.com/v1',api_key=os.getenv('DEEPSEEK_API_KEY'))
tools = [TavilySearch(max_result=1)]
prompt = ChatPromptTemplate.from_messages(
    [
        ('system','你是一个得力的助手',),
        # ('placeholder','{chat_history}'),
        ('human','{input}'),
        ('placeholder','{agent_scratchpad}')
    ]
)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
response = agent_executor.invoke({'input':'电视剧《伪装者》的主演都有谁？他们都是哪个国籍的人？'})
print(response['output'])