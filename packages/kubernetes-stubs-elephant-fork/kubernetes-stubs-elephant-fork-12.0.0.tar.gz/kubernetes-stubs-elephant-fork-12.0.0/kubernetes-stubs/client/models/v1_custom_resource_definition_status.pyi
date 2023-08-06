import datetime
import typing

import kubernetes.client

class V1CustomResourceDefinitionStatus:
    accepted_names: kubernetes.client.V1CustomResourceDefinitionNames
    conditions: typing.Optional[list[kubernetes.client.V1CustomResourceDefinitionCondition]]
    stored_versions: list[str]
    
    def __init__(self, *, accepted_names: kubernetes.client.V1CustomResourceDefinitionNames, conditions: typing.Optional[list[kubernetes.client.V1CustomResourceDefinitionCondition]] = ..., stored_versions: list[str]) -> None:
        ...
    def to_dict(self) -> V1CustomResourceDefinitionStatusDict:
        ...
class V1CustomResourceDefinitionStatusDict(typing.TypedDict, total=False):
    acceptedNames: kubernetes.client.V1CustomResourceDefinitionNamesDict
    conditions: typing.Optional[list[kubernetes.client.V1CustomResourceDefinitionConditionDict]]
    storedVersions: list[str]
