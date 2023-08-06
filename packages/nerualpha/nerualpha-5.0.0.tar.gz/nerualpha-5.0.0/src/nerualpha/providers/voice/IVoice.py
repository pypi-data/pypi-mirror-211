from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.contracts.vapiCreateCallPayload import VapiCreateCallPayload
from nerualpha.providers.voice.conversation import Conversation
from nerualpha.providers.voice.contracts.IVapiEventParams import IVapiEventParams
from nerualpha.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint
from nerualpha.providers.voice.contracts.vapiCreateCallResponse import VapiCreateCallResponse
from nerualpha.providers.voice.contracts.IVapiCreateCallOptions import IVapiCreateCallOptions
T = TypeVar('T')

#interface
class IVoice(ABC):
    @abstractmethod
    def onInboundCall(self,callback: str,to: IChannelPhoneEndpoint,from_: IChannelPhoneEndpoint = None):
        pass
    @abstractmethod
    def createConversation(self,name: str = None,displayName: str = None):
        pass
    @abstractmethod
    def onVapiAnswer(self,callback: str):
        pass
    @abstractmethod
    def onVapiEvent(self,params: IVapiEventParams):
        pass
    @abstractmethod
    def vapiCreateCall(self,from_: IChannelPhoneEndpoint,to: List[IChannelPhoneEndpoint],ncco: List[Dict[str,object]],options: IVapiCreateCallOptions = None):
        pass
    @abstractmethod
    def uploadNCCO(self,uuid: str,ncco: T):
        pass
    @abstractmethod
    def getConversation(self,id: str):
        pass
    @abstractmethod
    def getCallRecording(self,recordingUrl: str):
        pass
    @abstractmethod
    def uploadCallRecording(self,recordingUrl: str,assetsPath: str):
        pass
