import datetime
import typing

import kubernetes.client

class AppsV1beta1ScaleStatus:
    replicas: int
    selector: typing.Optional[dict[str, str]]
    target_selector: typing.Optional[str]
    
    def __init__(self, *, replicas: int, selector: typing.Optional[dict[str, str]] = ..., target_selector: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1ScaleStatusDict:
        ...
class AppsV1beta1ScaleStatusDict(typing.TypedDict, total=False):
    replicas: int
    selector: typing.Optional[dict[str, str]]
    targetSelector: typing.Optional[str]
