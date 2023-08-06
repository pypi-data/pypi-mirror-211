import datetime
import typing

import kubernetes.client

class V1alpha1Rule:
    api_groups: typing.Optional[list[str]]
    api_versions: typing.Optional[list[str]]
    resources: typing.Optional[list[str]]
    
    def __init__(self, *, api_groups: typing.Optional[list[str]] = ..., api_versions: typing.Optional[list[str]] = ..., resources: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1RuleDict:
        ...
class V1alpha1RuleDict(typing.TypedDict, total=False):
    apiGroups: typing.Optional[list[str]]
    apiVersions: typing.Optional[list[str]]
    resources: typing.Optional[list[str]]
