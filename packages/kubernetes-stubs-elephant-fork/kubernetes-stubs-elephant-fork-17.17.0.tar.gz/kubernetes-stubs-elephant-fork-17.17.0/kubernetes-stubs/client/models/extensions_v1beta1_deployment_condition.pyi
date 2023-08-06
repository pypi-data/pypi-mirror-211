import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1DeploymentCondition:
    last_transition_time: typing.Optional[datetime.datetime]
    last_update_time: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    reason: typing.Optional[str]
    status: str
    type: str
    
    def __init__(self, *, last_transition_time: typing.Optional[datetime.datetime] = ..., last_update_time: typing.Optional[datetime.datetime] = ..., message: typing.Optional[str] = ..., reason: typing.Optional[str] = ..., status: str, type: str) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1DeploymentConditionDict:
        ...
class ExtensionsV1beta1DeploymentConditionDict(typing.TypedDict, total=False):
    lastTransitionTime: typing.Optional[datetime.datetime]
    lastUpdateTime: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    reason: typing.Optional[str]
    status: str
    type: str
