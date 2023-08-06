import openai
from langchain.chains import RetrievalQAWithSourcesChain, LLMChain
from langchain import OpenAI
from neuralpit.context import Context
from neuralpit.agent.passthrough import PassThroughAgent
from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent, ZeroShotAgent
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from typing import List, Tuple, Any, Union
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory

class ChatAgentBuilder():

    @staticmethod
    def fromLoader(loader):
        context = Context.instance()
        embeddings = OpenAIEmbeddings(openai_api_key=context.getOpenAIKey())
        docs = loader.list()
        index = FAISS.from_documents(docs, embeddings)
        llm = OpenAI(openai_api_key=context.getOpenAIKey())
        qqa_chain = RetrievalQAWithSourcesChain.from_chain_type(
                llm=llm,
                chain_type = "map_reduce",
                retriever=index.as_retriever(),
            )
        tools = [
            Tool(
                name = "QA",
                func=qqa_chain,
                description="useful for when you need to answer questions about current events",
                return_direct=True
            )
        ]
        agent = PassThroughAgent()
        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
        return agent_executor