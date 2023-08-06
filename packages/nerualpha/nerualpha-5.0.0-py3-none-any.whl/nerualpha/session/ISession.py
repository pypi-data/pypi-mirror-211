from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.providers.logger.ILogContext import ILogContext
from nerualpha.services.commandService.ICommandService import ICommandService
from nerualpha.services.config.IConfig import IConfig
from nerualpha.services.jwt.IJwt import IJWT
from nerualpha.session.IActionPayload import IActionPayload
from nerualpha.session.IFilter import IFilter
from nerualpha.session.wrappedCallback import WrappedCallback
T = TypeVar('T')
K = TypeVar('K')

#interface
class ISession(ABC):
    id:str
    commandService:ICommandService
    bridge:IBridge
    config:IConfig
    jwt:IJWT
    @abstractmethod
    def createUUID(self):
        pass
    @abstractmethod
    def getToken(self):
        pass
    @abstractmethod
    def log(self,level: str,message: str,context: ILogContext):
        pass
    @abstractmethod
    def wrapCallback(self,route: str,filters: List[IFilter]):
        pass
    @abstractmethod
    def constructCommandHeaders(self):
        pass
    @abstractmethod
    def constructRequestHeaders(self):
        pass
    @abstractmethod
    def executeAction(self,actionPayload: IActionPayload[T],method: str):
        pass
