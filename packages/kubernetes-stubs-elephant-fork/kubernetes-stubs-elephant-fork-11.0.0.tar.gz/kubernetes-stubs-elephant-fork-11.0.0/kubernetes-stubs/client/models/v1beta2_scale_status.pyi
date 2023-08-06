import datetime
import typing

import kubernetes.client

class V1beta2ScaleStatus:
    replicas: int
    selector: typing.Optional[dict[str, str]]
    target_selector: typing.Optional[str]
    
    def __init__(self, *, replicas: int, selector: typing.Optional[dict[str, str]] = ..., target_selector: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2ScaleStatusDict:
        ...
class V1beta2ScaleStatusDict(typing.TypedDict, total=False):
    replicas: int
    selector: typing.Optional[dict[str, str]]
    targetSelector: typing.Optional[str]
