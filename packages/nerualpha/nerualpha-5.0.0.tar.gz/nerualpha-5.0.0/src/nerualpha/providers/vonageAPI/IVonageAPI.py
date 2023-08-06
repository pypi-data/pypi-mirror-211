from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
T = TypeVar('T')
K = TypeVar('K')

#interface
class IVonageAPI(ABC):
    @abstractmethod
    def invoke(self,url: str,method: str,body: T):
        pass
