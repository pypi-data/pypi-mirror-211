from neuralpit.tools.chat import ChatAgentBuilder
from neuralpit.utils.loader import MemFileLoader
import os

def main():
   fileName = 'manual.pdf'
   with open(fileName, mode='rb') as file: # b is important -> binary
      file_content = file.read()
      loader = MemFileLoader(file_content)
      agentExecutor = ChatAgentBuilder.fromLoader(loader)
      question ='How to change battery'
      ans = agentExecutor.run(question)
      print(ans)

if __name__ == "__main__":
    main()
