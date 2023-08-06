import datetime
import typing

import kubernetes.client

class V1beta2RollingUpdateDaemonSet:
    max_unavailable: typing.Optional[typing.Any]
    
    def __init__(self, *, max_unavailable: typing.Optional[typing.Any] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2RollingUpdateDaemonSetDict:
        ...
class V1beta2RollingUpdateDaemonSetDict(typing.TypedDict, total=False):
    maxUnavailable: typing.Optional[typing.Any]
