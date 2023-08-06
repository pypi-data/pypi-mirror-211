import datetime
import typing

import kubernetes.client

class V1beta1DaemonSetUpdateStrategy:
    rolling_update: typing.Optional[kubernetes.client.V1beta1RollingUpdateDaemonSet]
    type: typing.Optional[str]
    
    def __init__(self, *, rolling_update: typing.Optional[kubernetes.client.V1beta1RollingUpdateDaemonSet] = ..., type: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DaemonSetUpdateStrategyDict:
        ...
class V1beta1DaemonSetUpdateStrategyDict(typing.TypedDict, total=False):
    rollingUpdate: typing.Optional[kubernetes.client.V1beta1RollingUpdateDaemonSetDict]
    type: typing.Optional[str]
