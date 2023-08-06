import datetime
import typing

import kubernetes.client

class V1beta1ReplicaSetStatus:
    available_replicas: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.V1beta1ReplicaSetCondition]]
    fully_labeled_replicas: typing.Optional[int]
    observed_generation: typing.Optional[int]
    ready_replicas: typing.Optional[int]
    replicas: int
    
    def __init__(self, *, available_replicas: typing.Optional[int] = ..., conditions: typing.Optional[list[kubernetes.client.V1beta1ReplicaSetCondition]] = ..., fully_labeled_replicas: typing.Optional[int] = ..., observed_generation: typing.Optional[int] = ..., ready_replicas: typing.Optional[int] = ..., replicas: int) -> None:
        ...
    def to_dict(self) -> V1beta1ReplicaSetStatusDict:
        ...
class V1beta1ReplicaSetStatusDict(typing.TypedDict, total=False):
    availableReplicas: typing.Optional[int]
    conditions: typing.Optional[list[kubernetes.client.V1beta1ReplicaSetConditionDict]]
    fullyLabeledReplicas: typing.Optional[int]
    observedGeneration: typing.Optional[int]
    readyReplicas: typing.Optional[int]
    replicas: int
