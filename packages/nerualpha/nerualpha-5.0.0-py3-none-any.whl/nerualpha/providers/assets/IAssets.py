from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.assets.contracts.directoryPayload import DirectoryPayload
from nerualpha.providers.assets.contracts.listAssetsPayload import ListAssetsPayload
from nerualpha.providers.assets.contracts.removeAssetPayload import RemoveAssetPayload
from nerualpha.session.requestInterfaceWithParams import RequestInterfaceWithParams
from nerualpha.providers.assets.contracts.linkPayload import LinkPayload
from nerualpha.providers.assets.contracts.assetLinkResponse import AssetLinkResponse
from nerualpha.providers.assets.contracts.assetListResponse import AssetListResponse


#interface
class IAssets(ABC):
    @abstractmethod
    def createDir(self,name: str):
        pass
    @abstractmethod
    def remove(self,remoteFilePath: str,recursive: bool):
        pass
    @abstractmethod
    def getRemoteFile(self,remoteFilePath: str):
        pass
    @abstractmethod
    def generateLink(self,remoteFilePath: str,duration: str):
        pass
    @abstractmethod
    def uploadFiles(self,localFilePaths: List[str],remoteDir: str,retentionPeriod: str = None):
        pass
    @abstractmethod
    def uploadData(self,data: List[object],remoteDir: str,filenames: List[str] = None,retentionPeriod: str = None):
        pass
    @abstractmethod
    def list(self,remotePath: str,recursive: bool,limit: int):
        pass
