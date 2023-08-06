import datetime
import typing

import kubernetes.client

class V1beta1CustomResourceDefinitionVersion:
    name: str
    served: bool
    storage: bool
    
    def __init__(self, *, name: str, served: bool, storage: bool) -> None:
        ...
    def to_dict(self) -> V1beta1CustomResourceDefinitionVersionDict:
        ...
class V1beta1CustomResourceDefinitionVersionDict(typing.TypedDict, total=False):
    name: str
    served: bool
    storage: bool
