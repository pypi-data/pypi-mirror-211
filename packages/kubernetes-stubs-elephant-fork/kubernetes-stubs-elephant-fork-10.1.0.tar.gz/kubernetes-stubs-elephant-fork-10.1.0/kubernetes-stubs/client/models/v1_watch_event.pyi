import datetime
import typing

import kubernetes.client

class V1WatchEvent:
    object: kubernetes.client.RuntimeRawExtension
    type: str
    
    def __init__(self, *, object: kubernetes.client.RuntimeRawExtension, type: str) -> None:
        ...
    def to_dict(self) -> V1WatchEventDict:
        ...
class V1WatchEventDict(typing.TypedDict, total=False):
    object: kubernetes.client.RuntimeRawExtensionDict
    type: str
