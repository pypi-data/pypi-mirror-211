from typing import Any, Dict, List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from neuralpit.services.converterFactory import ConverterFactory
from neuralpit.context import Context

def textToDocs(text: str, file_index: int) -> List[Document]:
    """Converts a string or list of strings to a list of Documents with metadata."""
    if isinstance(text, str):
        # Take a single string as one page
        text = [text]
    page_docs = [Document(page_content=page) for page in text]

    # Add page numbers as metadata
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"fileIndex":file_index, "page": doc.metadata["page"], "chunk": i}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['fileIndex']}-{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks


class MemFileLoader():

    def __init__(self, binary):
        self._binary = binary

    
    def list(self)->List[Document]:
        context = Context.instance()
        converter = ConverterFactory.buildConverter(context.getConverterInfo())
        files = [converter.getFilePages(self._binary)]
        docs = []
        for idx, pages in enumerate(files):
            docs.extend(textToDocs(pages, idx ))
        return docs
    
class MemFilesLoader():

    def __init__(self, binary_list):
        self._binary_list = binary_list

    
    def list(self)->List[Document]:
        context = Context.instance()
        converter = ConverterFactory.buildConverter(context.getConverterInfo())
        files = [converter.getFilePages(binary) for binary in self._binary_list]
        docs = []
        for idx, pages in enumerate(files):
            docs.extend(textToDocs(pages, idx ))
        return docs

