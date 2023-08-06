import datetime
import typing

import kubernetes.client

class V1TokenReviewStatus:
    authenticated: typing.Optional[bool]
    error: typing.Optional[str]
    user: typing.Optional[kubernetes.client.V1UserInfo]
    
    def __init__(self, *, authenticated: typing.Optional[bool] = ..., error: typing.Optional[str] = ..., user: typing.Optional[kubernetes.client.V1UserInfo] = ...) -> None:
        ...
    def to_dict(self) -> V1TokenReviewStatusDict:
        ...
class V1TokenReviewStatusDict(typing.TypedDict, total=False):
    authenticated: typing.Optional[bool]
    error: typing.Optional[str]
    user: typing.Optional[kubernetes.client.V1UserInfoDict]
