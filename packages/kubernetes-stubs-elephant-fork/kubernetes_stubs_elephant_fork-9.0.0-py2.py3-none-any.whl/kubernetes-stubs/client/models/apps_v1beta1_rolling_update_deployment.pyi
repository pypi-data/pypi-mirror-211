import datetime
import typing

import kubernetes.client

class AppsV1beta1RollingUpdateDeployment:
    max_surge: typing.Optional[typing.Any]
    max_unavailable: typing.Optional[typing.Any]
    
    def __init__(self, *, max_surge: typing.Optional[typing.Any] = ..., max_unavailable: typing.Optional[typing.Any] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1RollingUpdateDeploymentDict:
        ...
class AppsV1beta1RollingUpdateDeploymentDict(typing.TypedDict, total=False):
    maxSurge: typing.Optional[typing.Any]
    maxUnavailable: typing.Optional[typing.Any]
