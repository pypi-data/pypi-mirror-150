"""
Type annotations for iotthingsgraph service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotthingsgraph.type_defs import AssociateEntityToThingRequestRequestTypeDef

    data: AssociateEntityToThingRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    DeploymentTargetType,
    EntityFilterNameType,
    EntityTypeType,
    FlowExecutionEventTypeType,
    FlowExecutionStatusType,
    NamespaceDeletionStatusType,
    SystemInstanceDeploymentStatusType,
    SystemInstanceFilterNameType,
    UploadStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateEntityToThingRequestRequestTypeDef",
    "CreateFlowTemplateRequestRequestTypeDef",
    "CreateFlowTemplateResponseTypeDef",
    "CreateSystemInstanceRequestRequestTypeDef",
    "CreateSystemInstanceResponseTypeDef",
    "CreateSystemTemplateRequestRequestTypeDef",
    "CreateSystemTemplateResponseTypeDef",
    "DefinitionDocumentTypeDef",
    "DeleteFlowTemplateRequestRequestTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteSystemInstanceRequestRequestTypeDef",
    "DeleteSystemTemplateRequestRequestTypeDef",
    "DependencyRevisionTypeDef",
    "DeploySystemInstanceRequestRequestTypeDef",
    "DeploySystemInstanceResponseTypeDef",
    "DeprecateFlowTemplateRequestRequestTypeDef",
    "DeprecateSystemTemplateRequestRequestTypeDef",
    "DescribeNamespaceRequestRequestTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "DissociateEntityFromThingRequestRequestTypeDef",
    "EntityDescriptionTypeDef",
    "EntityFilterTypeDef",
    "FlowExecutionMessageTypeDef",
    "FlowExecutionSummaryTypeDef",
    "FlowTemplateDescriptionTypeDef",
    "FlowTemplateFilterTypeDef",
    "FlowTemplateSummaryTypeDef",
    "GetEntitiesRequestRequestTypeDef",
    "GetEntitiesResponseTypeDef",
    "GetFlowTemplateRequestRequestTypeDef",
    "GetFlowTemplateResponseTypeDef",
    "GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef",
    "GetFlowTemplateRevisionsRequestRequestTypeDef",
    "GetFlowTemplateRevisionsResponseTypeDef",
    "GetNamespaceDeletionStatusResponseTypeDef",
    "GetSystemInstanceRequestRequestTypeDef",
    "GetSystemInstanceResponseTypeDef",
    "GetSystemTemplateRequestRequestTypeDef",
    "GetSystemTemplateResponseTypeDef",
    "GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef",
    "GetSystemTemplateRevisionsRequestRequestTypeDef",
    "GetSystemTemplateRevisionsResponseTypeDef",
    "GetUploadStatusRequestRequestTypeDef",
    "GetUploadStatusResponseTypeDef",
    "ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef",
    "ListFlowExecutionMessagesRequestRequestTypeDef",
    "ListFlowExecutionMessagesResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricsConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SearchEntitiesRequestRequestTypeDef",
    "SearchEntitiesRequestSearchEntitiesPaginateTypeDef",
    "SearchEntitiesResponseTypeDef",
    "SearchFlowExecutionsRequestRequestTypeDef",
    "SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef",
    "SearchFlowExecutionsResponseTypeDef",
    "SearchFlowTemplatesRequestRequestTypeDef",
    "SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef",
    "SearchFlowTemplatesResponseTypeDef",
    "SearchSystemInstancesRequestRequestTypeDef",
    "SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef",
    "SearchSystemInstancesResponseTypeDef",
    "SearchSystemTemplatesRequestRequestTypeDef",
    "SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef",
    "SearchSystemTemplatesResponseTypeDef",
    "SearchThingsRequestRequestTypeDef",
    "SearchThingsRequestSearchThingsPaginateTypeDef",
    "SearchThingsResponseTypeDef",
    "SystemInstanceDescriptionTypeDef",
    "SystemInstanceFilterTypeDef",
    "SystemInstanceSummaryTypeDef",
    "SystemTemplateDescriptionTypeDef",
    "SystemTemplateFilterTypeDef",
    "SystemTemplateSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ThingTypeDef",
    "UndeploySystemInstanceRequestRequestTypeDef",
    "UndeploySystemInstanceResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFlowTemplateRequestRequestTypeDef",
    "UpdateFlowTemplateResponseTypeDef",
    "UpdateSystemTemplateRequestRequestTypeDef",
    "UpdateSystemTemplateResponseTypeDef",
    "UploadEntityDefinitionsRequestRequestTypeDef",
    "UploadEntityDefinitionsResponseTypeDef",
)

_RequiredAssociateEntityToThingRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateEntityToThingRequestRequestTypeDef",
    {
        "thingName": str,
        "entityId": str,
    },
)
_OptionalAssociateEntityToThingRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateEntityToThingRequestRequestTypeDef",
    {
        "namespaceVersion": int,
    },
    total=False,
)


class AssociateEntityToThingRequestRequestTypeDef(
    _RequiredAssociateEntityToThingRequestRequestTypeDef,
    _OptionalAssociateEntityToThingRequestRequestTypeDef,
):
    pass


_RequiredCreateFlowTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFlowTemplateRequestRequestTypeDef",
    {
        "definition": "DefinitionDocumentTypeDef",
    },
)
_OptionalCreateFlowTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFlowTemplateRequestRequestTypeDef",
    {
        "compatibleNamespaceVersion": int,
    },
    total=False,
)


class CreateFlowTemplateRequestRequestTypeDef(
    _RequiredCreateFlowTemplateRequestRequestTypeDef,
    _OptionalCreateFlowTemplateRequestRequestTypeDef,
):
    pass


CreateFlowTemplateResponseTypeDef = TypedDict(
    "CreateFlowTemplateResponseTypeDef",
    {
        "summary": "FlowTemplateSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateSystemInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSystemInstanceRequestRequestTypeDef",
    {
        "definition": "DefinitionDocumentTypeDef",
        "target": DeploymentTargetType,
    },
)
_OptionalCreateSystemInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSystemInstanceRequestRequestTypeDef",
    {
        "tags": Sequence["TagTypeDef"],
        "greengrassGroupName": str,
        "s3BucketName": str,
        "metricsConfiguration": "MetricsConfigurationTypeDef",
        "flowActionsRoleArn": str,
    },
    total=False,
)


class CreateSystemInstanceRequestRequestTypeDef(
    _RequiredCreateSystemInstanceRequestRequestTypeDef,
    _OptionalCreateSystemInstanceRequestRequestTypeDef,
):
    pass


CreateSystemInstanceResponseTypeDef = TypedDict(
    "CreateSystemInstanceResponseTypeDef",
    {
        "summary": "SystemInstanceSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateSystemTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSystemTemplateRequestRequestTypeDef",
    {
        "definition": "DefinitionDocumentTypeDef",
    },
)
_OptionalCreateSystemTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSystemTemplateRequestRequestTypeDef",
    {
        "compatibleNamespaceVersion": int,
    },
    total=False,
)


class CreateSystemTemplateRequestRequestTypeDef(
    _RequiredCreateSystemTemplateRequestRequestTypeDef,
    _OptionalCreateSystemTemplateRequestRequestTypeDef,
):
    pass


CreateSystemTemplateResponseTypeDef = TypedDict(
    "CreateSystemTemplateResponseTypeDef",
    {
        "summary": "SystemTemplateSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DefinitionDocumentTypeDef = TypedDict(
    "DefinitionDocumentTypeDef",
    {
        "language": Literal["GRAPHQL"],
        "text": str,
    },
)

DeleteFlowTemplateRequestRequestTypeDef = TypedDict(
    "DeleteFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteNamespaceResponseTypeDef = TypedDict(
    "DeleteNamespaceResponseTypeDef",
    {
        "namespaceArn": str,
        "namespaceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteSystemInstanceRequestRequestTypeDef = TypedDict(
    "DeleteSystemInstanceRequestRequestTypeDef",
    {
        "id": str,
    },
    total=False,
)

DeleteSystemTemplateRequestRequestTypeDef = TypedDict(
    "DeleteSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

DependencyRevisionTypeDef = TypedDict(
    "DependencyRevisionTypeDef",
    {
        "id": str,
        "revisionNumber": int,
    },
    total=False,
)

DeploySystemInstanceRequestRequestTypeDef = TypedDict(
    "DeploySystemInstanceRequestRequestTypeDef",
    {
        "id": str,
    },
    total=False,
)

DeploySystemInstanceResponseTypeDef = TypedDict(
    "DeploySystemInstanceResponseTypeDef",
    {
        "summary": "SystemInstanceSummaryTypeDef",
        "greengrassDeploymentId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeprecateFlowTemplateRequestRequestTypeDef = TypedDict(
    "DeprecateFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeprecateSystemTemplateRequestRequestTypeDef = TypedDict(
    "DeprecateSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

DescribeNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeNamespaceRequestRequestTypeDef",
    {
        "namespaceName": str,
    },
    total=False,
)

DescribeNamespaceResponseTypeDef = TypedDict(
    "DescribeNamespaceResponseTypeDef",
    {
        "namespaceArn": str,
        "namespaceName": str,
        "trackingNamespaceName": str,
        "trackingNamespaceVersion": int,
        "namespaceVersion": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DissociateEntityFromThingRequestRequestTypeDef = TypedDict(
    "DissociateEntityFromThingRequestRequestTypeDef",
    {
        "thingName": str,
        "entityType": EntityTypeType,
    },
)

EntityDescriptionTypeDef = TypedDict(
    "EntityDescriptionTypeDef",
    {
        "id": str,
        "arn": str,
        "type": EntityTypeType,
        "createdAt": datetime,
        "definition": "DefinitionDocumentTypeDef",
    },
    total=False,
)

EntityFilterTypeDef = TypedDict(
    "EntityFilterTypeDef",
    {
        "name": EntityFilterNameType,
        "value": Sequence[str],
    },
    total=False,
)

FlowExecutionMessageTypeDef = TypedDict(
    "FlowExecutionMessageTypeDef",
    {
        "messageId": str,
        "eventType": FlowExecutionEventTypeType,
        "timestamp": datetime,
        "payload": str,
    },
    total=False,
)

FlowExecutionSummaryTypeDef = TypedDict(
    "FlowExecutionSummaryTypeDef",
    {
        "flowExecutionId": str,
        "status": FlowExecutionStatusType,
        "systemInstanceId": str,
        "flowTemplateId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
    },
    total=False,
)

FlowTemplateDescriptionTypeDef = TypedDict(
    "FlowTemplateDescriptionTypeDef",
    {
        "summary": "FlowTemplateSummaryTypeDef",
        "definition": "DefinitionDocumentTypeDef",
        "validatedNamespaceVersion": int,
    },
    total=False,
)

FlowTemplateFilterTypeDef = TypedDict(
    "FlowTemplateFilterTypeDef",
    {
        "name": Literal["DEVICE_MODEL_ID"],
        "value": Sequence[str],
    },
)

FlowTemplateSummaryTypeDef = TypedDict(
    "FlowTemplateSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "revisionNumber": int,
        "createdAt": datetime,
    },
    total=False,
)

_RequiredGetEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredGetEntitiesRequestRequestTypeDef",
    {
        "ids": Sequence[str],
    },
)
_OptionalGetEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalGetEntitiesRequestRequestTypeDef",
    {
        "namespaceVersion": int,
    },
    total=False,
)


class GetEntitiesRequestRequestTypeDef(
    _RequiredGetEntitiesRequestRequestTypeDef, _OptionalGetEntitiesRequestRequestTypeDef
):
    pass


GetEntitiesResponseTypeDef = TypedDict(
    "GetEntitiesResponseTypeDef",
    {
        "descriptions": List["EntityDescriptionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetFlowTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetFlowTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetFlowTemplateRequestRequestTypeDef",
    {
        "revisionNumber": int,
    },
    total=False,
)


class GetFlowTemplateRequestRequestTypeDef(
    _RequiredGetFlowTemplateRequestRequestTypeDef, _OptionalGetFlowTemplateRequestRequestTypeDef
):
    pass


GetFlowTemplateResponseTypeDef = TypedDict(
    "GetFlowTemplateResponseTypeDef",
    {
        "description": "FlowTemplateDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef = TypedDict(
    "_RequiredGetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef",
    {
        "id": str,
    },
)
_OptionalGetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef = TypedDict(
    "_OptionalGetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef(
    _RequiredGetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef,
    _OptionalGetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef,
):
    pass


_RequiredGetFlowTemplateRevisionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetFlowTemplateRevisionsRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetFlowTemplateRevisionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetFlowTemplateRevisionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetFlowTemplateRevisionsRequestRequestTypeDef(
    _RequiredGetFlowTemplateRevisionsRequestRequestTypeDef,
    _OptionalGetFlowTemplateRevisionsRequestRequestTypeDef,
):
    pass


GetFlowTemplateRevisionsResponseTypeDef = TypedDict(
    "GetFlowTemplateRevisionsResponseTypeDef",
    {
        "summaries": List["FlowTemplateSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetNamespaceDeletionStatusResponseTypeDef = TypedDict(
    "GetNamespaceDeletionStatusResponseTypeDef",
    {
        "namespaceArn": str,
        "namespaceName": str,
        "status": NamespaceDeletionStatusType,
        "errorCode": Literal["VALIDATION_FAILED"],
        "errorMessage": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSystemInstanceRequestRequestTypeDef = TypedDict(
    "GetSystemInstanceRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetSystemInstanceResponseTypeDef = TypedDict(
    "GetSystemInstanceResponseTypeDef",
    {
        "description": "SystemInstanceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetSystemTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetSystemTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetSystemTemplateRequestRequestTypeDef",
    {
        "revisionNumber": int,
    },
    total=False,
)


class GetSystemTemplateRequestRequestTypeDef(
    _RequiredGetSystemTemplateRequestRequestTypeDef, _OptionalGetSystemTemplateRequestRequestTypeDef
):
    pass


GetSystemTemplateResponseTypeDef = TypedDict(
    "GetSystemTemplateResponseTypeDef",
    {
        "description": "SystemTemplateDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef = TypedDict(
    "_RequiredGetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef",
    {
        "id": str,
    },
)
_OptionalGetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef = TypedDict(
    "_OptionalGetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef(
    _RequiredGetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef,
    _OptionalGetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef,
):
    pass


_RequiredGetSystemTemplateRevisionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSystemTemplateRevisionsRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetSystemTemplateRevisionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSystemTemplateRevisionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetSystemTemplateRevisionsRequestRequestTypeDef(
    _RequiredGetSystemTemplateRevisionsRequestRequestTypeDef,
    _OptionalGetSystemTemplateRevisionsRequestRequestTypeDef,
):
    pass


GetSystemTemplateRevisionsResponseTypeDef = TypedDict(
    "GetSystemTemplateRevisionsResponseTypeDef",
    {
        "summaries": List["SystemTemplateSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetUploadStatusRequestRequestTypeDef = TypedDict(
    "GetUploadStatusRequestRequestTypeDef",
    {
        "uploadId": str,
    },
)

GetUploadStatusResponseTypeDef = TypedDict(
    "GetUploadStatusResponseTypeDef",
    {
        "uploadId": str,
        "uploadStatus": UploadStatusType,
        "namespaceArn": str,
        "namespaceName": str,
        "namespaceVersion": int,
        "failureReason": List[str],
        "createdDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef = TypedDict(
    "_RequiredListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef",
    {
        "flowExecutionId": str,
    },
)
_OptionalListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef = TypedDict(
    "_OptionalListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef(
    _RequiredListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef,
    _OptionalListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef,
):
    pass


_RequiredListFlowExecutionMessagesRequestRequestTypeDef = TypedDict(
    "_RequiredListFlowExecutionMessagesRequestRequestTypeDef",
    {
        "flowExecutionId": str,
    },
)
_OptionalListFlowExecutionMessagesRequestRequestTypeDef = TypedDict(
    "_OptionalListFlowExecutionMessagesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListFlowExecutionMessagesRequestRequestTypeDef(
    _RequiredListFlowExecutionMessagesRequestRequestTypeDef,
    _OptionalListFlowExecutionMessagesRequestRequestTypeDef,
):
    pass


ListFlowExecutionMessagesResponseTypeDef = TypedDict(
    "ListFlowExecutionMessagesResponseTypeDef",
    {
        "messages": List["FlowExecutionMessageTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List["TagTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MetricsConfigurationTypeDef = TypedDict(
    "MetricsConfigurationTypeDef",
    {
        "cloudMetricEnabled": bool,
        "metricRuleRoleArn": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredSearchEntitiesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchEntitiesRequestRequestTypeDef",
    {
        "entityTypes": Sequence[EntityTypeType],
    },
)
_OptionalSearchEntitiesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchEntitiesRequestRequestTypeDef",
    {
        "filters": Sequence["EntityFilterTypeDef"],
        "nextToken": str,
        "maxResults": int,
        "namespaceVersion": int,
    },
    total=False,
)


class SearchEntitiesRequestRequestTypeDef(
    _RequiredSearchEntitiesRequestRequestTypeDef, _OptionalSearchEntitiesRequestRequestTypeDef
):
    pass


_RequiredSearchEntitiesRequestSearchEntitiesPaginateTypeDef = TypedDict(
    "_RequiredSearchEntitiesRequestSearchEntitiesPaginateTypeDef",
    {
        "entityTypes": Sequence[EntityTypeType],
    },
)
_OptionalSearchEntitiesRequestSearchEntitiesPaginateTypeDef = TypedDict(
    "_OptionalSearchEntitiesRequestSearchEntitiesPaginateTypeDef",
    {
        "filters": Sequence["EntityFilterTypeDef"],
        "namespaceVersion": int,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchEntitiesRequestSearchEntitiesPaginateTypeDef(
    _RequiredSearchEntitiesRequestSearchEntitiesPaginateTypeDef,
    _OptionalSearchEntitiesRequestSearchEntitiesPaginateTypeDef,
):
    pass


SearchEntitiesResponseTypeDef = TypedDict(
    "SearchEntitiesResponseTypeDef",
    {
        "descriptions": List["EntityDescriptionTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSearchFlowExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFlowExecutionsRequestRequestTypeDef",
    {
        "systemInstanceId": str,
    },
)
_OptionalSearchFlowExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFlowExecutionsRequestRequestTypeDef",
    {
        "flowExecutionId": str,
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class SearchFlowExecutionsRequestRequestTypeDef(
    _RequiredSearchFlowExecutionsRequestRequestTypeDef,
    _OptionalSearchFlowExecutionsRequestRequestTypeDef,
):
    pass


_RequiredSearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef = TypedDict(
    "_RequiredSearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef",
    {
        "systemInstanceId": str,
    },
)
_OptionalSearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef = TypedDict(
    "_OptionalSearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef",
    {
        "flowExecutionId": str,
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef(
    _RequiredSearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef,
    _OptionalSearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef,
):
    pass


SearchFlowExecutionsResponseTypeDef = TypedDict(
    "SearchFlowExecutionsResponseTypeDef",
    {
        "summaries": List["FlowExecutionSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchFlowTemplatesRequestRequestTypeDef = TypedDict(
    "SearchFlowTemplatesRequestRequestTypeDef",
    {
        "filters": Sequence["FlowTemplateFilterTypeDef"],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef = TypedDict(
    "SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef",
    {
        "filters": Sequence["FlowTemplateFilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

SearchFlowTemplatesResponseTypeDef = TypedDict(
    "SearchFlowTemplatesResponseTypeDef",
    {
        "summaries": List["FlowTemplateSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchSystemInstancesRequestRequestTypeDef = TypedDict(
    "SearchSystemInstancesRequestRequestTypeDef",
    {
        "filters": Sequence["SystemInstanceFilterTypeDef"],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef = TypedDict(
    "SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef",
    {
        "filters": Sequence["SystemInstanceFilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

SearchSystemInstancesResponseTypeDef = TypedDict(
    "SearchSystemInstancesResponseTypeDef",
    {
        "summaries": List["SystemInstanceSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchSystemTemplatesRequestRequestTypeDef = TypedDict(
    "SearchSystemTemplatesRequestRequestTypeDef",
    {
        "filters": Sequence["SystemTemplateFilterTypeDef"],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef = TypedDict(
    "SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef",
    {
        "filters": Sequence["SystemTemplateFilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

SearchSystemTemplatesResponseTypeDef = TypedDict(
    "SearchSystemTemplatesResponseTypeDef",
    {
        "summaries": List["SystemTemplateSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSearchThingsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchThingsRequestRequestTypeDef",
    {
        "entityId": str,
    },
)
_OptionalSearchThingsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchThingsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "namespaceVersion": int,
    },
    total=False,
)


class SearchThingsRequestRequestTypeDef(
    _RequiredSearchThingsRequestRequestTypeDef, _OptionalSearchThingsRequestRequestTypeDef
):
    pass


_RequiredSearchThingsRequestSearchThingsPaginateTypeDef = TypedDict(
    "_RequiredSearchThingsRequestSearchThingsPaginateTypeDef",
    {
        "entityId": str,
    },
)
_OptionalSearchThingsRequestSearchThingsPaginateTypeDef = TypedDict(
    "_OptionalSearchThingsRequestSearchThingsPaginateTypeDef",
    {
        "namespaceVersion": int,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchThingsRequestSearchThingsPaginateTypeDef(
    _RequiredSearchThingsRequestSearchThingsPaginateTypeDef,
    _OptionalSearchThingsRequestSearchThingsPaginateTypeDef,
):
    pass


SearchThingsResponseTypeDef = TypedDict(
    "SearchThingsResponseTypeDef",
    {
        "things": List["ThingTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SystemInstanceDescriptionTypeDef = TypedDict(
    "SystemInstanceDescriptionTypeDef",
    {
        "summary": "SystemInstanceSummaryTypeDef",
        "definition": "DefinitionDocumentTypeDef",
        "s3BucketName": str,
        "metricsConfiguration": "MetricsConfigurationTypeDef",
        "validatedNamespaceVersion": int,
        "validatedDependencyRevisions": List["DependencyRevisionTypeDef"],
        "flowActionsRoleArn": str,
    },
    total=False,
)

SystemInstanceFilterTypeDef = TypedDict(
    "SystemInstanceFilterTypeDef",
    {
        "name": SystemInstanceFilterNameType,
        "value": Sequence[str],
    },
    total=False,
)

SystemInstanceSummaryTypeDef = TypedDict(
    "SystemInstanceSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "status": SystemInstanceDeploymentStatusType,
        "target": DeploymentTargetType,
        "greengrassGroupName": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "greengrassGroupId": str,
        "greengrassGroupVersionId": str,
    },
    total=False,
)

SystemTemplateDescriptionTypeDef = TypedDict(
    "SystemTemplateDescriptionTypeDef",
    {
        "summary": "SystemTemplateSummaryTypeDef",
        "definition": "DefinitionDocumentTypeDef",
        "validatedNamespaceVersion": int,
    },
    total=False,
)

SystemTemplateFilterTypeDef = TypedDict(
    "SystemTemplateFilterTypeDef",
    {
        "name": Literal["FLOW_TEMPLATE_ID"],
        "value": Sequence[str],
    },
)

SystemTemplateSummaryTypeDef = TypedDict(
    "SystemTemplateSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "revisionNumber": int,
        "createdAt": datetime,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence["TagTypeDef"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

ThingTypeDef = TypedDict(
    "ThingTypeDef",
    {
        "thingArn": str,
        "thingName": str,
    },
    total=False,
)

UndeploySystemInstanceRequestRequestTypeDef = TypedDict(
    "UndeploySystemInstanceRequestRequestTypeDef",
    {
        "id": str,
    },
    total=False,
)

UndeploySystemInstanceResponseTypeDef = TypedDict(
    "UndeploySystemInstanceResponseTypeDef",
    {
        "summary": "SystemInstanceSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateFlowTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowTemplateRequestRequestTypeDef",
    {
        "id": str,
        "definition": "DefinitionDocumentTypeDef",
    },
)
_OptionalUpdateFlowTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowTemplateRequestRequestTypeDef",
    {
        "compatibleNamespaceVersion": int,
    },
    total=False,
)


class UpdateFlowTemplateRequestRequestTypeDef(
    _RequiredUpdateFlowTemplateRequestRequestTypeDef,
    _OptionalUpdateFlowTemplateRequestRequestTypeDef,
):
    pass


UpdateFlowTemplateResponseTypeDef = TypedDict(
    "UpdateFlowTemplateResponseTypeDef",
    {
        "summary": "FlowTemplateSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateSystemTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSystemTemplateRequestRequestTypeDef",
    {
        "id": str,
        "definition": "DefinitionDocumentTypeDef",
    },
)
_OptionalUpdateSystemTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSystemTemplateRequestRequestTypeDef",
    {
        "compatibleNamespaceVersion": int,
    },
    total=False,
)


class UpdateSystemTemplateRequestRequestTypeDef(
    _RequiredUpdateSystemTemplateRequestRequestTypeDef,
    _OptionalUpdateSystemTemplateRequestRequestTypeDef,
):
    pass


UpdateSystemTemplateResponseTypeDef = TypedDict(
    "UpdateSystemTemplateResponseTypeDef",
    {
        "summary": "SystemTemplateSummaryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UploadEntityDefinitionsRequestRequestTypeDef = TypedDict(
    "UploadEntityDefinitionsRequestRequestTypeDef",
    {
        "document": "DefinitionDocumentTypeDef",
        "syncWithPublicNamespace": bool,
        "deprecateExistingEntities": bool,
    },
    total=False,
)

UploadEntityDefinitionsResponseTypeDef = TypedDict(
    "UploadEntityDefinitionsResponseTypeDef",
    {
        "uploadId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
