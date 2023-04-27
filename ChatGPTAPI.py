
from revChatGPT.V1 import Chatbot
import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep



class ChatGPT(LLM):
    
    history_data: Optional[List] = []
    token : Optional[str]
    chatbot : Optional[Chatbot] = None
    call : int = 0
    
    #### WARNING : for each api call this library will create a new chat on chat.openai.com
    
    
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        #token is a must check
        if self.token is None:
            raise ValueError("Need a token , check https://chat.openai.com/api/auth/session for get your token")
        else:
            self.chatbot = Chatbot(config={"access_token": self.token})
            
        response = ""
        # OpenAI: 50 requests / hour for each account
        if self.call >= 49:
            raise ValueError("You have reached the maximum number of requests per hour ! Help me to Improve")
        else:
            sleep(2)
            for data in self.chatbot.ask( prompt ):
                response = data["message"]
            
            self.call += 1
        
        #add to history
        self.history_data.append({"prompt":prompt,"response":response})    
        
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "CHatGPT", "token": self.token}


#llm = ChatGPT(token = "YOUR_TOKEN")

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("how have i question in before?"))