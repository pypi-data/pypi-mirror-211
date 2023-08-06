import datetime
import typing

import kubernetes.client

class ExtensionsV1beta1AllowedCSIDriver:
    name: str
    
    def __init__(self, *, name: str) -> None:
        ...
    def to_dict(self) -> ExtensionsV1beta1AllowedCSIDriverDict:
        ...
class ExtensionsV1beta1AllowedCSIDriverDict(typing.TypedDict, total=False):
    name: str
