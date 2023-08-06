import datetime
import typing

import kubernetes.client

class ApiregistrationV1beta1ServiceReference:
    name: typing.Optional[str]
    namespace: typing.Optional[str]
    
    def __init__(self, *, name: typing.Optional[str] = ..., namespace: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> ApiregistrationV1beta1ServiceReferenceDict:
        ...
class ApiregistrationV1beta1ServiceReferenceDict(typing.TypedDict, total=False):
    name: typing.Optional[str]
    namespace: typing.Optional[str]
