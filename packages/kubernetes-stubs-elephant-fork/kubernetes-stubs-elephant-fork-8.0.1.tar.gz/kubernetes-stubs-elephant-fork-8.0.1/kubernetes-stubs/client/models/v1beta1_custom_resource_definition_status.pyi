import datetime
import typing

import kubernetes.client

class V1beta1CustomResourceDefinitionStatus:
    accepted_names: kubernetes.client.V1beta1CustomResourceDefinitionNames
    conditions: list[kubernetes.client.V1beta1CustomResourceDefinitionCondition]
    stored_versions: list[str]
    
    def __init__(self, *, accepted_names: kubernetes.client.V1beta1CustomResourceDefinitionNames, conditions: list[kubernetes.client.V1beta1CustomResourceDefinitionCondition], stored_versions: list[str]) -> None:
        ...
    def to_dict(self) -> V1beta1CustomResourceDefinitionStatusDict:
        ...
class V1beta1CustomResourceDefinitionStatusDict(typing.TypedDict, total=False):
    acceptedNames: kubernetes.client.V1beta1CustomResourceDefinitionNamesDict
    conditions: list[kubernetes.client.V1beta1CustomResourceDefinitionConditionDict]
    storedVersions: list[str]
