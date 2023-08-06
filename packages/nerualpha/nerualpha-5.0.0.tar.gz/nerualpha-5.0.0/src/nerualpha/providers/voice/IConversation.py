from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IFilter import IFilter
from nerualpha.session.requestInterface import RequestInterface
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.contracts.acceptInboundCallPayload import AcceptInboundCallPayload
from nerualpha.providers.voice.contracts.addUserPayload import AddUserPayload
from nerualpha.providers.voice.contracts.deleteMemberPayload import DeleteMemberPayload
from nerualpha.providers.voice.contracts.earmuffPayload import EarmuffPayload
from nerualpha.providers.voice.contracts.IAcceptInboundCallEvent import IAcceptInboundCallEvent
from nerualpha.providers.voice.contracts.IChannel import IChannel
from nerualpha.providers.voice.contracts.inviteMemberPayload import InviteMemberPayload
from nerualpha.providers.voice.contracts.IPlayStreamBody import IPlayStreamBody
from nerualpha.providers.voice.contracts.ISayTextBody import ISayTextBody
from nerualpha.providers.voice.contracts.mutePayload import MutePayload
from nerualpha.providers.voice.contracts.playStopPayload import PlayStopPayload
from nerualpha.providers.voice.contracts.playStreamPayload import PlayStreamPayload
from nerualpha.providers.voice.contracts.sayStopPayload import SayStopPayload
from nerualpha.providers.voice.contracts.sayTextPayload import SayTextPayload
from nerualpha.providers.voice.contracts.transferMemberPayload import TransferMemberPayload
from nerualpha.providers.voice.contracts.memberResponse import MemberResponse
from nerualpha.providers.voice.contracts.addUserResponse import AddUserResponse
from nerualpha.providers.voice.contracts.eventResponse import EventResponse
from nerualpha.providers.voice.contracts.audioSayResponseBody import AudioSayResponseBody
from nerualpha.providers.voice.contracts.audioSayStopResponseBody import AudioSayStopResponseBody
from nerualpha.providers.voice.contracts.playStreamResponseBody import PlayStreamResponseBody
from nerualpha.providers.voice.contracts.playStreamStopResponseBody import PlayStreamStopResponseBody
from nerualpha.providers.voice.contracts.earmuffResponseBody import EarmuffResponseBody
from nerualpha.providers.voice.contracts.muteResponseBody import MuteResponseBody


#interface
class IConversation(ABC):
    @abstractmethod
    def acceptInboundCall(self,event: IAcceptInboundCallEvent):
        pass
    @abstractmethod
    def inviteMember(self,name: str,channel: IChannel):
        pass
    @abstractmethod
    def onConversationCreated(self,callback: str):
        pass
    @abstractmethod
    def addUser(self,name: str):
        pass
    @abstractmethod
    def transferMember(self,userId: str,legId: str):
        pass
    @abstractmethod
    def deleteMember(self,memberId: str):
        pass
    @abstractmethod
    def sayText(self,body: ISayTextBody,to: str = None):
        pass
    @abstractmethod
    def sayStop(self,sayId: str,to: str = None):
        pass
    @abstractmethod
    def playStream(self,body: IPlayStreamBody,to: str = None):
        pass
    @abstractmethod
    def playStop(self,playId: str,to: str = None):
        pass
    @abstractmethod
    def earmuffOn(self,to: str,from_: str = None):
        pass
    @abstractmethod
    def earmuffOff(self,to: str,from_: str = None):
        pass
    @abstractmethod
    def muteOn(self,to: str,from_: str = None):
        pass
    @abstractmethod
    def muteOff(self,to: str,from_: str = None):
        pass
    @abstractmethod
    def listenForEvents(self,callback: str,filters: List[IFilter]):
        pass
    @abstractmethod
    def onSay(self,callback: str):
        pass
    @abstractmethod
    def onPlay(self,callback: str):
        pass
    @abstractmethod
    def onSayStop(self,callback: str):
        pass
    @abstractmethod
    def onPlayStop(self,callback: str):
        pass
    @abstractmethod
    def onSayDone(self,callback: str):
        pass
    @abstractmethod
    def onPlayDone(self,callback: str):
        pass
    @abstractmethod
    def onLegStatusUpdate(self,callback: str):
        pass
    @abstractmethod
    def onMemberJoined(self,callback: str,memberName: str = None):
        pass
    @abstractmethod
    def onMemberInvited(self,callback: str,memberName: str = None):
        pass
    @abstractmethod
    def onMemberLeft(self,callback: str,memberName: str = None):
        pass
    @abstractmethod
    def onDTMF(self,callback: str):
        pass
