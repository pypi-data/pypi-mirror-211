from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')
K = TypeVar('K')

#interface
class ICommandService(ABC):
    @abstractmethod
    def executeCommand(self,url: str,method: str,data: T = None,headers: Dict[str,str] = None):
        pass
