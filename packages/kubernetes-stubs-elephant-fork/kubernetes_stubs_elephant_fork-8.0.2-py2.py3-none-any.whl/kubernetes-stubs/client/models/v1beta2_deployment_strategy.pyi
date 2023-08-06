import datetime
import typing

import kubernetes.client

class V1beta2DeploymentStrategy:
    rolling_update: typing.Optional[kubernetes.client.V1beta2RollingUpdateDeployment]
    type: typing.Optional[str]
    
    def __init__(self, *, rolling_update: typing.Optional[kubernetes.client.V1beta2RollingUpdateDeployment] = ..., type: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeploymentStrategyDict:
        ...
class V1beta2DeploymentStrategyDict(typing.TypedDict, total=False):
    rollingUpdate: typing.Optional[kubernetes.client.V1beta2RollingUpdateDeploymentDict]
    type: typing.Optional[str]
