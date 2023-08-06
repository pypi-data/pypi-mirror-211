import datetime
import typing

import kubernetes.client

class ApiextensionsV1beta1ServiceReference:
    name: str
    namespace: str
    path: typing.Optional[str]
    
    def __init__(self, *, name: str, namespace: str, path: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> ApiextensionsV1beta1ServiceReferenceDict:
        ...
class ApiextensionsV1beta1ServiceReferenceDict(typing.TypedDict, total=False):
    name: str
    namespace: str
    path: typing.Optional[str]
