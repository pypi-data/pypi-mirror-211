import datetime
import typing

import kubernetes.client

class V1TokenReviewSpec:
    token: typing.Optional[str]
    
    def __init__(self, *, token: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1TokenReviewSpecDict:
        ...
class V1TokenReviewSpecDict(typing.TypedDict, total=False):
    token: typing.Optional[str]
