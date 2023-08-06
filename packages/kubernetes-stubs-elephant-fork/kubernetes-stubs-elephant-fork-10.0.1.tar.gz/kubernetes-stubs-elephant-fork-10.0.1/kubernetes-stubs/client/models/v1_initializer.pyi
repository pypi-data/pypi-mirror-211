import datetime
import typing

import kubernetes.client

class V1Initializer:
    name: str
    
    def __init__(self, *, name: str) -> None:
        ...
    def to_dict(self) -> V1InitializerDict:
        ...
class V1InitializerDict(typing.TypedDict, total=False):
    name: str
