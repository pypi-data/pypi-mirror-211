import datetime
import typing

import kubernetes.client

class AppsV1beta1DeploymentStrategy:
    rolling_update: typing.Optional[kubernetes.client.AppsV1beta1RollingUpdateDeployment]
    type: typing.Optional[str]
    
    def __init__(self, *, rolling_update: typing.Optional[kubernetes.client.AppsV1beta1RollingUpdateDeployment] = ..., type: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1DeploymentStrategyDict:
        ...
class AppsV1beta1DeploymentStrategyDict(typing.TypedDict, total=False):
    rollingUpdate: typing.Optional[kubernetes.client.AppsV1beta1RollingUpdateDeploymentDict]
    type: typing.Optional[str]
