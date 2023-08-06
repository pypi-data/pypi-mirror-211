import datetime
import typing

import kubernetes.client

class V1beta1CustomResourceDefinitionSpec:
    additional_printer_columns: typing.Optional[list[kubernetes.client.V1beta1CustomResourceColumnDefinition]]
    group: str
    names: kubernetes.client.V1beta1CustomResourceDefinitionNames
    scope: str
    subresources: typing.Optional[kubernetes.client.V1beta1CustomResourceSubresources]
    validation: typing.Optional[kubernetes.client.V1beta1CustomResourceValidation]
    version: typing.Optional[str]
    versions: typing.Optional[list[kubernetes.client.V1beta1CustomResourceDefinitionVersion]]
    
    def __init__(self, *, additional_printer_columns: typing.Optional[list[kubernetes.client.V1beta1CustomResourceColumnDefinition]] = ..., group: str, names: kubernetes.client.V1beta1CustomResourceDefinitionNames, scope: str, subresources: typing.Optional[kubernetes.client.V1beta1CustomResourceSubresources] = ..., validation: typing.Optional[kubernetes.client.V1beta1CustomResourceValidation] = ..., version: typing.Optional[str] = ..., versions: typing.Optional[list[kubernetes.client.V1beta1CustomResourceDefinitionVersion]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CustomResourceDefinitionSpecDict:
        ...
class V1beta1CustomResourceDefinitionSpecDict(typing.TypedDict, total=False):
    additionalPrinterColumns: typing.Optional[list[kubernetes.client.V1beta1CustomResourceColumnDefinitionDict]]
    group: str
    names: kubernetes.client.V1beta1CustomResourceDefinitionNamesDict
    scope: str
    subresources: typing.Optional[kubernetes.client.V1beta1CustomResourceSubresourcesDict]
    validation: typing.Optional[kubernetes.client.V1beta1CustomResourceValidationDict]
    version: typing.Optional[str]
    versions: typing.Optional[list[kubernetes.client.V1beta1CustomResourceDefinitionVersionDict]]
