from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.request.requestParams import RequestParams
from nerualpha.services.commandService.ICommandService import ICommandService
T = TypeVar('T')
K = TypeVar('K')
@dataclass
class CommandService(ICommandService):
    bridge: IBridge
    def __init__(self,bridge: IBridge):
        self.bridge = bridge
    
    async def executeCommand(self,url: str,method: str,data: T = None,headers: Dict[str,str] = None):
        requestParams = RequestParams()
        requestParams.url = url
        requestParams.method = method
        if data is not None:
            requestParams.data = data
        
        if headers is not None:
            requestParams.headers = headers
        
        return await self.bridge.request(requestParams)
    
    def reprJSON(self):
        result = {}
        dict = asdict(self)
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type"}
        for key in dict:
            val = getattr(self, key)

            if val is not None:
                if type(val) is list:
                    parsedList = []
                    for i in val:
                        if hasattr(i,'reprJSON'):
                            parsedList.append(i.reprJSON())
                        else:
                            parsedList.append(i)
                    val = parsedList

                if hasattr(val,'reprJSON'):
                    val = val.reprJSON()
                if key in keywordsMap:
                    key = keywordsMap[key]
                result.__setitem__(key.replace('_hyphen_', '-'), val)
        return result
