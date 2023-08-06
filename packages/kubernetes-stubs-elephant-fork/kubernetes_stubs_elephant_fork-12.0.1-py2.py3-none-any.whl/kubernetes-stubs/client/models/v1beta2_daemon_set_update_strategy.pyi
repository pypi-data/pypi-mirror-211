import datetime
import typing

import kubernetes.client

class V1beta2DaemonSetUpdateStrategy:
    rolling_update: typing.Optional[kubernetes.client.V1beta2RollingUpdateDaemonSet]
    type: typing.Optional[str]
    
    def __init__(self, *, rolling_update: typing.Optional[kubernetes.client.V1beta2RollingUpdateDaemonSet] = ..., type: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DaemonSetUpdateStrategyDict:
        ...
class V1beta2DaemonSetUpdateStrategyDict(typing.TypedDict, total=False):
    rollingUpdate: typing.Optional[kubernetes.client.V1beta2RollingUpdateDaemonSetDict]
    type: typing.Optional[str]
