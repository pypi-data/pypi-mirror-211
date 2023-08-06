import datetime
import typing

import kubernetes.client

class AppsV1beta1RollbackConfig:
    revision: typing.Optional[int]
    
    def __init__(self, *, revision: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> AppsV1beta1RollbackConfigDict:
        ...
class AppsV1beta1RollbackConfigDict(typing.TypedDict, total=False):
    revision: typing.Optional[int]
