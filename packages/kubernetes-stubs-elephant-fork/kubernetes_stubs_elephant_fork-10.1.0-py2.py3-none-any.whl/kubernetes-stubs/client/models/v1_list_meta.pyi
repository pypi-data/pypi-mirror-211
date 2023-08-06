import datetime
import typing

import kubernetes.client

class V1ListMeta:
    _continue: typing.Optional[str]
    resource_version: typing.Optional[str]
    self_link: typing.Optional[str]
    
    def __init__(self, *, _continue: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., self_link: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1ListMetaDict:
        ...
class V1ListMetaDict(typing.TypedDict, total=False):
    _continue: typing.Optional[str]
    resourceVersion: typing.Optional[str]
    selfLink: typing.Optional[str]
