import os

from langchain import hub
from langchain.agents import create_react_agent,AgentExecutor
from langchain.globals import set_verbose, set_debug
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from load_dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_deepseek import ChatDeepSeek
from langchain_community.agent_toolkits.load_tools import load_tools

load_dotenv()

# prompt_template = ChatPromptTemplate.from_messages([
#     ('system', '你是一个专业的翻译助手，要尽可能保留中文所要表达的含义'),
#     MessagesPlaceholder('his_msg'),
#     ('human', '请翻译以下内容，{text}')
#
# ])
# prompt = prompt_template.invoke(
#     {'text': '愿所爱皆所愿',
#     'his_msg': [HumanMessage(content='我是一个女孩'),
#                     AIMessage(content="I'm a girl!")]
#     })

# search =TavilySearch(max_results=1)
# llm = ChatOpenAI(model='deepseek-chat', base_url='https://api.deepseek.com/v1', api_key=os.getenv('DEEPSEEK_API_KEY'))
llm = ChatDeepSeek(model='deepseek-chat')
tools = [TavilySearch(max_results = 1)]
tool_names = [tools]
# tools = [TavilySearch(max_results=1)]
# tool_names = []
# prompt = ChatPromptTemplate.from_messages(
#     [('system','你是一个专业的助手，能提供专业的回答，也能提供充足的情绪价值,你可以使用以下工具'),
#
#      ('human','{input}'),
#      ('placeholder','{agent_scratchpad}')
#      ]
# )

prompt2 =ChatPromptTemplate.from_messages(
    ['system',"""
    Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer\n
Thought: you should always think about what to do\n
Action: the action to take, should be one of [{tool_names}]\n
Action Input: the input to the action\n
Observation: the result of the action\n
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer\n
Final Answer: the final answer to the original input question\n

Begin!
"""
,
     'human','{input}',
     'placeholder','{agent_scratchpad}'
]
)

prompt =PromptTemplate.from_template(
    '''
    Answer the following questions as best you can. You have access to the following tools:

{tools}

Strictly use the following format (IMPORTANT: the step name must be present in your response. Valid options for step names: Thought, Action, Action Input, Observation, Final Thought):

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation sequence can repeat N times)
Final Thought: your final thought
Final Answer: the final answer to the original input question. You must start this line with "Final Answer: ". You must not produce any further text beyond this line

Begin!

Question: {input}
Thought: {agent_scratchpad}
'''
)



# result = llm.invoke(prompt)
parser = StrOutputParser()
# print(parser.invoke(result  ))
messages = {
    'text':'愿有情人终成眷属',
    'his_msg':[HumanMessage(content='愿所爱皆所愿'),
               AIMessage(content='May all your loved ones fulfill your wishes. ')]
}
# chain = prompt_template | llm | parser
# result = chain.invoke(messages)
# print(result)
#加日志
# set_verbose(True)
set_debug(True)
agent = create_react_agent(llm,tools,prompt=prompt)
agent_executor = AgentExecutor(agent=agent,tools=tools,handle_parsing_errors=True)
response = agent_executor.invoke({'input':'解释一下，愿所爱皆所愿，然能有几人如愿否？'})
print(response['output'])