import os
from neuralpit.services.api import NeuralPitAPIService

class Context():

    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._instance.api_client =  NeuralPitAPIService()
            cls._instance._service_profile = None
            cls._instance._user_profile = None
        return cls._instance


    def getUserProfile(self)->str:
        if not self._user_profile:
            self._user_profile = self.api_client.getUserProfile()
        return self._user_profile
    
    def getServiceProfile(self)->str:
        if not self._service_profile:
            self._service_profile = self.api_client.getServiceProfile('DOC_CHAT')
        return self._service_profile
    
    def getOpenAIKey(self)-> str:
        user_profile = self.getUserProfile()
        return user_profile['openai_key']
    
    def getConverterInfo(self)-> str:
        service_profile = self.getServiceProfile()
        return service_profile['converter']
    