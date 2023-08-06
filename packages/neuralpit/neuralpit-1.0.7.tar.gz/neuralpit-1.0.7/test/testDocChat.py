from neuralpit.tools.chat import DocumentChatAgent
from neuralpit.utils.loader import DocumentLoader
import os

def main():
   doc_loader = DocumentLoader()
   chat = DocumentChatAgent()
   fileName = 'manual.pdf'
   with open(fileName, mode='rb') as file: # b is important -> binary
      file_content = file.read()
      doc_loader.loadSingleFileFromDisck(file_content)
      chat.buildAgentExecutor(doc_loader)
      question ='How to change battery'
      ans = chat.response(question)
      print(ans)

if __name__ == "__main__":
    main()
