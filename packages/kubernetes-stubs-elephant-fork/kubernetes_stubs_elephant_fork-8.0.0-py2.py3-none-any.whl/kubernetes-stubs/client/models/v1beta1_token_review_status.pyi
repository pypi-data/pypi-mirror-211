import datetime
import typing

import kubernetes.client

class V1beta1TokenReviewStatus:
    authenticated: typing.Optional[bool]
    error: typing.Optional[str]
    user: typing.Optional[kubernetes.client.V1beta1UserInfo]
    
    def __init__(self, *, authenticated: typing.Optional[bool] = ..., error: typing.Optional[str] = ..., user: typing.Optional[kubernetes.client.V1beta1UserInfo] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1TokenReviewStatusDict:
        ...
class V1beta1TokenReviewStatusDict(typing.TypedDict, total=False):
    authenticated: typing.Optional[bool]
    error: typing.Optional[str]
    user: typing.Optional[kubernetes.client.V1beta1UserInfoDict]
