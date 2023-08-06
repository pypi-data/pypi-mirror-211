import datetime
import typing

import kubernetes.client

class PolicyV1beta1AllowedCSIDriver:
    name: str
    
    def __init__(self, *, name: str) -> None:
        ...
    def to_dict(self) -> PolicyV1beta1AllowedCSIDriverDict:
        ...
class PolicyV1beta1AllowedCSIDriverDict(typing.TypedDict, total=False):
    name: str
