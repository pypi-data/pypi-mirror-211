import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1DeploymentStatus:
    available_replicas: typing.Optional[int]
    collision_count: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.ExtensionsV1beta1DeploymentCondition]]
    observed_generation: typing.Optional[int]
    ready_replicas: typing.Optional[int]
    replicas: typing.Optional[int]
    unavailable_replicas: typing.Optional[int]
    updated_replicas: typing.Optional[int]
    
    def __init__(self, *, available_replicas: typing.Optional[int] = ..., collision_count: typing.Optional[int] = ..., conditions: typing.Optional[list[kubernetes.client.ExtensionsV1beta1DeploymentCondition]] = ..., observed_generation: typing.Optional[int] = ..., ready_replicas: typing.Optional[int] = ..., replicas: typing.Optional[int] = ..., unavailable_replicas: typing.Optional[int] = ..., updated_replicas: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1DeploymentStatusDict:
        ...
class ExtensionsV1beta1DeploymentStatusDict(typing.TypedDict, total=False):
    availableReplicas: typing.Optional[int]
    collisionCount: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.ExtensionsV1beta1DeploymentConditionDict]]
    observedGeneration: typing.Optional[int]
    readyReplicas: typing.Optional[int]
    replicas: typing.Optional[int]
    unavailableReplicas: typing.Optional[int]
    updatedReplicas: typing.Optional[int]
