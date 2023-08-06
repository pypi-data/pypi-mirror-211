from typing import Any, Dict, List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from neuralpit.services.converterFactory import ConverterFactory
from neuralpit.context import Context

def textToDocs(text: str) -> List[Document]:
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
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks


class BinaryLoader():

    def __init__(self, binary):
        self.binary = binary
    
    def loadSingleFileFromDisck(self, binary):
        if not self._converter:
            context = Context.instance()
            self._converter = ConverterFactory.buildConverter(context.getConverterInfo())
        pages = self._converter.convertFileToString(binary)
        self._docs =  self.textToDocs(pages)
    
    def list(self)->List[Document]:
        context = Context.instance()
        converter = ConverterFactory.buildConverter(context.getConverterInfo())
        pages = converter.convertFileToString(self.binary)
        return textToDocs(pages)
    


