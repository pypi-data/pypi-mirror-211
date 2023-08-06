import datetime
import typing

import kubernetes.client

class V1alpha1RuntimeClassSpec:
    runtime_handler: str
    
    def __init__(self, *, runtime_handler: str) -> None:
        ...
    def to_dict(self) -> V1alpha1RuntimeClassSpecDict:
        ...
class V1alpha1RuntimeClassSpecDict(typing.TypedDict, total=False):
    runtimeHandler: str
