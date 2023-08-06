from typing import List
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from neuralpit.context import Context
from .loader import BinaryLoader

class DocumentIndexer():

    def __init__(self, doc_loader: BinaryLoader):
        context = Context.instance()
        self._embeddings = OpenAIEmbeddings(openai_api_key=context.getOpenAIKey())
        self._doc_loader = doc_loader

    def getIndex(self):
        docs = self._doc_loader.list()
        index = FAISS.from_documents(docs, self._embeddings)
        return index


