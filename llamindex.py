import os

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from dotenv import load_dotenv
from llama_index.core.base.embeddings.base import similarity
from llama_index.core.tools import QueryEngineTool,ToolMetadata
from sqlalchemy.testing.suite.test_reflection import metadata
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
load_dotenv()





# documents = SimpleDirectoryReader('data').load_data()
# index = VectorStoreIndex.from_documents(documents)
# query_engine = index.as_query_engine()
# response =query_engine.query('财务数据变化趋势')
# print(response)

A_docs = SimpleDirectoryReader(
    input_files=['./A.pdf']
).load_data()
B_docs = SimpleDirectoryReader(
    input_files=['./B.pdf']
).load_data()

A_index = VectorStoreIndex.from_documents(A_docs)
B_index = VectorStoreIndex.from_documents(B_docs)

#持久化索引
A_index.storage_context.persist(persist_dir='./storage/A')
B_index.storage_context.persist(persist_dir='./storage/B')
#从本地读取索引
try:
    storage_context = StorageContext.from_defaults(
        persist_dir='./storage/A'
    )
    A_index = load_index_from_storage(storage_context)
    storage_context = StorageContext.from_defaults(
        persist_dir='./storage/B'
    )
    B_index = load_index_from_storage(storage_context)
    index_loaded =True
except:
    index_loaded = False

#创建查询索引
A_engine = A_index.as_query_engine(similarity_top_k=3)
B_engine = B_index.as_query_engine(similarity_top_k=3)

query_engine_tools = [
    QueryEngineTool(
        query_engine=A_engine,
        metadata = ToolMetadata(
            name='A_Finance',
            description=(
                '用于提供A公司的财务信息'
            ),
        ),
    ),

    QueryEngineTool(
        query_engine=B_engine,
        metadata=ToolMetadata(
            name='B_Finance',
            description=(
                '用于提供B公司的财务信息'
            ),
        ),
    ),
]

#配置大模型
llm = OpenAI(model='deepseek-chat',base_url='https://api.deepseek.com/v1',api_key=os.getenv('DEEPSEEK_API_KEY'),timeout=60,max_retries=3)
agent = ReActAgent.from_tools(query_engine_tools,llm=llm,verbose=True)
print(agent.chat('比较这两个文件的知识差异'))


