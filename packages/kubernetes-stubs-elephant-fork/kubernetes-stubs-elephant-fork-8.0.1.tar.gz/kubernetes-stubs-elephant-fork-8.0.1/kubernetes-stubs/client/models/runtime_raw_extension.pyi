import datetime
import typing

import kubernetes.client

class RuntimeRawExtension:
    raw: str
    
    def __init__(self, *, raw: str) -> None:
        ...
    def to_dict(self) -> RuntimeRawExtensionDict:
        ...
class RuntimeRawExtensionDict(typing.TypedDict, total=False):
    Raw: str
