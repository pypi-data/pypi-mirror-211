from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.services.config.IConfig import IConfig
from nerualpha.session.ISession import ISession
from nerualpha.providers.queue.contracts.ICreateQueueOptions import ICreateQueueOptions
from nerualpha.session.requestInterfaceWithParams import RequestInterfaceWithParams
from nerualpha.providers.queue.contracts.ICreateQueuePayload import ICreateQueuePayload
from nerualpha.providers.queue.contracts.queueDetailsResponse import QueueDetailsResponse
from nerualpha.providers.queue.contracts.IUpdateQueueOptions import IUpdateQueueOptions
from nerualpha.providers.queue.contracts.IUpdateQueuePayload import IUpdateQueuePayload
T = TypeVar('T')

#interface
class IQueue(ABC):
    config:IConfig
    provider:str
    session:ISession
    bridge:IBridge
    @abstractmethod
    def createQueue(self,queueName: str,callback: str,options: ICreateQueueOptions):
        pass
    @abstractmethod
    def updateQueue(self,queueName: str,options: IUpdateQueueOptions):
        pass
    @abstractmethod
    def list(self):
        pass
    @abstractmethod
    def getQueueDetails(self,name: str):
        pass
    @abstractmethod
    def deleteQueue(self,name: str):
        pass
    @abstractmethod
    def pauseQueue(self,name: str):
        pass
    @abstractmethod
    def resumeQueue(self,name: str):
        pass
    @abstractmethod
    def enqueue(self,name: str,data: List[T]):
        pass
    @abstractmethod
    def enqueueSingle(self,name: str,data: T):
        pass
    @abstractmethod
    def deadLetterList(self,name: str):
        pass
    @abstractmethod
    def deadLetterDequeue(self,name: str,count: int):
        pass
