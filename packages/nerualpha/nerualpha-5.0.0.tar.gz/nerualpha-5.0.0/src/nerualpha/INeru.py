from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.state.state import State
from nerualpha.request.IRequest import IRequest
from nerualpha.session.neruSession import NeruSession


#interface
class INeru(ABC):
    @abstractmethod
    def createSession(self,ttl: int = None):
        pass
    @abstractmethod
    def createSessionWithId(self,id: str):
        pass
    @abstractmethod
    def getSessionById(self,id: str):
        pass
    @abstractmethod
    def getAppUrl(self):
        pass
    @abstractmethod
    def getSessionFromRequest(self,req: IRequest):
        pass
    @abstractmethod
    def getGlobalSession(self):
        pass
    @abstractmethod
    def getInstanceState(self):
        pass
    @abstractmethod
    def getAccountState(self):
        pass
