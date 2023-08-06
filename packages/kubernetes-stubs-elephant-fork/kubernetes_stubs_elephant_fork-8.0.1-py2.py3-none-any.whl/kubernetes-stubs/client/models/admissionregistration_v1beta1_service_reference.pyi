import datetime
import typing

import kubernetes.client

class AdmissionregistrationV1beta1ServiceReference:
    name: str
    namespace: str
    path: typing.Optional[str]
    
    def __init__(self, *, name: str, namespace: str, path: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> AdmissionregistrationV1beta1ServiceReferenceDict:
        ...
class AdmissionregistrationV1beta1ServiceReferenceDict(typing.TypedDict, total=False):
    name: str
    namespace: str
    path: typing.Optional[str]
