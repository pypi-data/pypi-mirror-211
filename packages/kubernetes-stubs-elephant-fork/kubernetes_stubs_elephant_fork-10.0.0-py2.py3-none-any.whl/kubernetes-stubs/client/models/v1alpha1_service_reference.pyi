import datetime
import typing

import kubernetes.client

class V1alpha1ServiceReference:
    name: str
    namespace: str
    path: typing.Optional[str]
    
    def __init__(self, *, name: str, namespace: str, path: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ServiceReferenceDict:
        ...
class V1alpha1ServiceReferenceDict(typing.TypedDict, total=False):
    name: str
    namespace: str
    path: typing.Optional[str]
