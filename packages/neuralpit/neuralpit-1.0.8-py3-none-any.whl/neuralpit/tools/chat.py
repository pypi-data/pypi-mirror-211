import openai
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from neuralpit.context import Context
from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from typing import List, Tuple, Any, Union
from langchain.schema import AgentAction, AgentFinish

class ChatAgent(BaseSingleActionAgent):
    """Chat Custom Agent."""
    
    @property
    def input_keys(self):
        return ["input"]
    
    def plan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        return AgentAction(tool="QA", tool_input=kwargs["input"], log="")

    async def aplan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        return AgentAction(tool="QA", tool_input=kwargs["input"], log="")
    
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
        agent = ChatAgent()
        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
        return agent_executor