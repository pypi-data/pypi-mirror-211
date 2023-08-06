import datetime
import typing

import kubernetes.client

class AppsV1beta1ScaleSpec:
    replicas: typing.Optional[int]
    
    def __init__(self, *, replicas: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1ScaleSpecDict:
        ...
class AppsV1beta1ScaleSpecDict(typing.TypedDict, total=False):
    replicas: typing.Optional[int]
