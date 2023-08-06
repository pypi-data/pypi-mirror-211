from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.messages.contracts.IBaseMessage import IBaseMessage
from nerualpha.providers.messages.contracts.IMessageContact import IMessageContact
from nerualpha.providers.messages.contracts.ISendImageContent import ISendImageContent
from nerualpha.providers.messages.contracts.sendImagePayload import SendImagePayload
from nerualpha.providers.messages.contracts.sendTextPayload import SendTextPayload
from nerualpha.providers.messages.contracts.unsubscribeEventsPayload import UnsubscribeEventsPayload
from nerualpha.providers.messages.contracts.sendResponse import SendResponse


#interface
class IMessages(ABC):
    @abstractmethod
    def send(self,message: IBaseMessage):
        pass
    @abstractmethod
    def sendText(self,from_: IMessageContact,to: IMessageContact,message: str):
        pass
    @abstractmethod
    def sendImage(self,from_: IMessageContact,to: IMessageContact,imageContent: ISendImageContent):
        pass
    @abstractmethod
    def listenMessages(self,from_: IMessageContact,to: IMessageContact,callback: str):
        pass
    @abstractmethod
    def listenEvents(self,from_: IMessageContact,to: IMessageContact,callback: str):
        pass
    @abstractmethod
    def onMessage(self,callback: str,from_: IMessageContact,to: IMessageContact):
        pass
    @abstractmethod
    def onMessageEvents(self,callback: str,from_: IMessageContact,to: IMessageContact):
        pass
    @abstractmethod
    def unsubscribeEvents(self,id: str):
        pass
