import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1AllowedHostPath:
    path_prefix: typing.Optional[str]
    read_only: typing.Optional[bool]
    
    def __init__(self, *, path_prefix: typing.Optional[str] = ..., read_only: typing.Optional[bool] = ...) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1AllowedHostPathDict:
        ...
class ExtensionsV1beta1AllowedHostPathDict(typing.TypedDict, total=False):
    pathPrefix: typing.Optional[str]
    readOnly: typing.Optional[bool]
