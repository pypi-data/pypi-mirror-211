import datetime
import typing

import kubernetes.client

class V1beta2StatefulSetStatus:
    collision_count: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.V1beta2StatefulSetCondition]]
    current_replicas: typing.Optional[int]
    current_revision: typing.Optional[str]
    observed_generation: typing.Optional[int]
    ready_replicas: typing.Optional[int]
    replicas: int
    update_revision: typing.Optional[str]
    updated_replicas: typing.Optional[int]
    
    def __init__(self, *, collision_count: typing.Optional[int] = ..., conditions: typing.Optional[list[kubernetes.client.V1beta2StatefulSetCondition]] = ..., current_replicas: typing.Optional[int] = ..., current_revision: typing.Optional[str] = ..., observed_generation: typing.Optional[int] = ..., ready_replicas: typing.Optional[int] = ..., replicas: int, update_revision: typing.Optional[str] = ..., updated_replicas: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2StatefulSetStatusDict:
        ...
class V1beta2StatefulSetStatusDict(typing.TypedDict, total=False):
    collisionCount: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.V1beta2StatefulSetConditionDict]]
    currentReplicas: typing.Optional[int]
    currentRevision: typing.Optional[str]
    observedGeneration: typing.Optional[int]
    readyReplicas: typing.Optional[int]
    replicas: int
    updateRevision: typing.Optional[str]
    updatedReplicas: typing.Optional[int]
