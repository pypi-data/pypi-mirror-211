import datetime
import typing

import kubernetes.client

class V1alpha1Initializer:
    name: str
    rules: typing.Optional[list[kubernetes.client.V1alpha1Rule]]
    
    def __init__(self, *, name: str, rules: typing.Optional[list[kubernetes.client.V1alpha1Rule]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1InitializerDict:
        ...
class V1alpha1InitializerDict(typing.TypedDict, total=False):
    name: str
    rules: typing.Optional[list[kubernetes.client.V1alpha1RuleDict]]
