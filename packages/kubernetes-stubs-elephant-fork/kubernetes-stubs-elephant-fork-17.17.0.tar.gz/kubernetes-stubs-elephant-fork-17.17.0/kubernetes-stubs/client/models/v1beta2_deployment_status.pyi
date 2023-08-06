import datetime
import typing

import kubernetes.client

class V1beta2DeploymentStatus:
    available_replicas: typing.Optional[int]
    collision_count: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.V1beta2DeploymentCondition]]
    observed_generation: typing.Optional[int]
    ready_replicas: typing.Optional[int]
    replicas: typing.Optional[int]
    unavailable_replicas: typing.Optional[int]
    updated_replicas: typing.Optional[int]
    
    def __init__(self, *, available_replicas: typing.Optional[int] = ..., collision_count: typing.Optional[int] = ..., conditions: typing.Optional[list[kubernetes.client.V1beta2DeploymentCondition]] = ..., observed_generation: typing.Optional[int] = ..., ready_replicas: typing.Optional[int] = ..., replicas: typing.Optional[int] = ..., unavailable_replicas: typing.Optional[int] = ..., updated_replicas: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeploymentStatusDict:
        ...
class V1beta2DeploymentStatusDict(typing.TypedDict, total=False):
    availableReplicas: typing.Optional[int]
    collisionCount: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.V1beta2DeploymentConditionDict]]
    observedGeneration: typing.Optional[int]
    readyReplicas: typing.Optional[int]
    replicas: typing.Optional[int]
    unavailableReplicas: typing.Optional[int]
    updatedReplicas: typing.Optional[int]
