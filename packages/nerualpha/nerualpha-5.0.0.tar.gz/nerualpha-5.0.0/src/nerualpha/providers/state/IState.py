from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.state.expireOptions import ExpireOptions
T = TypeVar('T')

#interface
class IState(ABC):
    @abstractmethod
    def set(self,key: str,value: T):
        pass
    @abstractmethod
    def get(self,key: str):
        pass
    @abstractmethod
    def delete(self,key: str):
        pass
    @abstractmethod
    def hdel(self,htable: str,keys: List[str]):
        pass
    @abstractmethod
    def hexists(self,htable: str,key: str):
        pass
    @abstractmethod
    def hgetall(self,htable: str):
        pass
    @abstractmethod
    def hmget(self,htable: str,keys: List[str]):
        pass
    @abstractmethod
    def hvals(self,htable: str):
        pass
    @abstractmethod
    def hget(self,htable: str,key: str):
        pass
    @abstractmethod
    def hincrby(self,htable: str,key: str,value: int):
        pass
    @abstractmethod
    def hlen(self,htable: str):
        pass
    @abstractmethod
    def hset(self,htable: str,keyValuePairs: Dict[str,str]):
        pass
    @abstractmethod
    def rpush(self,list: str,value: T):
        pass
    @abstractmethod
    def lpush(self,list: str,value: T):
        pass
    @abstractmethod
    def rpop(self,list: str,count: int):
        pass
    @abstractmethod
    def lpop(self,list: str,count: int):
        pass
    @abstractmethod
    def lrem(self,list: str,value: T,count: int):
        pass
    @abstractmethod
    def ltrim(self,list: str,startPos: int,endPos: int):
        pass
    @abstractmethod
    def linsert(self,list: str,before: bool,pivot: T,value: T):
        pass
    @abstractmethod
    def lindex(self,list: str,position: int):
        pass
    @abstractmethod
    def lset(self,list: str,position: int,value: T):
        pass
    @abstractmethod
    def incrby(self,key: str,value: int):
        pass
    @abstractmethod
    def decrby(self,key: str,value: int):
        pass
    @abstractmethod
    def expire(self,key: str,seconds: int,option: ExpireOptions = None):
        pass
    @abstractmethod
    def llen(self,list: str):
        pass
    @abstractmethod
    def lrange(self,list: str,startPos: int,endPos: int):
        pass
