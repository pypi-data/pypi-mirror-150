"""
Type annotations for discovery service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_discovery/type_defs/)

Usage::

    ```python
    from mypy_boto3_discovery.type_defs import AgentConfigurationStatusTypeDef

    data: AgentConfigurationStatusTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AgentStatusType,
    BatchDeleteImportDataErrorCodeType,
    ConfigurationItemTypeType,
    ContinuousExportStatusType,
    ExportDataFormatType,
    ExportStatusType,
    ImportStatusType,
    ImportTaskFilterNameType,
    orderStringType,
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
    "AgentConfigurationStatusTypeDef",
    "AgentInfoTypeDef",
    "AgentNetworkInfoTypeDef",
    "AssociateConfigurationItemsToApplicationRequestRequestTypeDef",
    "BatchDeleteImportDataErrorTypeDef",
    "BatchDeleteImportDataRequestRequestTypeDef",
    "BatchDeleteImportDataResponseTypeDef",
    "ConfigurationTagTypeDef",
    "ContinuousExportDescriptionTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateTagsRequestRequestTypeDef",
    "CustomerAgentInfoTypeDef",
    "CustomerConnectorInfoTypeDef",
    "DeleteApplicationsRequestRequestTypeDef",
    "DeleteTagsRequestRequestTypeDef",
    "DescribeAgentsRequestDescribeAgentsPaginateTypeDef",
    "DescribeAgentsRequestRequestTypeDef",
    "DescribeAgentsResponseTypeDef",
    "DescribeConfigurationsRequestRequestTypeDef",
    "DescribeConfigurationsResponseTypeDef",
    "DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef",
    "DescribeContinuousExportsRequestRequestTypeDef",
    "DescribeContinuousExportsResponseTypeDef",
    "DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef",
    "DescribeExportConfigurationsRequestRequestTypeDef",
    "DescribeExportConfigurationsResponseTypeDef",
    "DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef",
    "DescribeExportTasksRequestRequestTypeDef",
    "DescribeExportTasksResponseTypeDef",
    "DescribeImportTasksRequestRequestTypeDef",
    "DescribeImportTasksResponseTypeDef",
    "DescribeTagsRequestDescribeTagsPaginateTypeDef",
    "DescribeTagsRequestRequestTypeDef",
    "DescribeTagsResponseTypeDef",
    "DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef",
    "ExportConfigurationsResponseTypeDef",
    "ExportFilterTypeDef",
    "ExportInfoTypeDef",
    "FilterTypeDef",
    "GetDiscoverySummaryResponseTypeDef",
    "ImportTaskFilterTypeDef",
    "ImportTaskTypeDef",
    "ListConfigurationsRequestListConfigurationsPaginateTypeDef",
    "ListConfigurationsRequestRequestTypeDef",
    "ListConfigurationsResponseTypeDef",
    "ListServerNeighborsRequestRequestTypeDef",
    "ListServerNeighborsResponseTypeDef",
    "NeighborConnectionDetailTypeDef",
    "OrderByElementTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "StartContinuousExportResponseTypeDef",
    "StartDataCollectionByAgentIdsRequestRequestTypeDef",
    "StartDataCollectionByAgentIdsResponseTypeDef",
    "StartExportTaskRequestRequestTypeDef",
    "StartExportTaskResponseTypeDef",
    "StartImportTaskRequestRequestTypeDef",
    "StartImportTaskResponseTypeDef",
    "StopContinuousExportRequestRequestTypeDef",
    "StopContinuousExportResponseTypeDef",
    "StopDataCollectionByAgentIdsRequestRequestTypeDef",
    "StopDataCollectionByAgentIdsResponseTypeDef",
    "TagFilterTypeDef",
    "TagTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
)

AgentConfigurationStatusTypeDef = TypedDict(
    "AgentConfigurationStatusTypeDef",
    {
        "agentId": str,
        "operationSucceeded": bool,
        "description": str,
    },
    total=False,
)

AgentInfoTypeDef = TypedDict(
    "AgentInfoTypeDef",
    {
        "agentId": str,
        "hostName": str,
        "agentNetworkInfoList": List["AgentNetworkInfoTypeDef"],
        "connectorId": str,
        "version": str,
        "health": AgentStatusType,
        "lastHealthPingTime": str,
        "collectionStatus": str,
        "agentType": str,
        "registeredTime": str,
    },
    total=False,
)

AgentNetworkInfoTypeDef = TypedDict(
    "AgentNetworkInfoTypeDef",
    {
        "ipAddress": str,
        "macAddress": str,
    },
    total=False,
)

AssociateConfigurationItemsToApplicationRequestRequestTypeDef = TypedDict(
    "AssociateConfigurationItemsToApplicationRequestRequestTypeDef",
    {
        "applicationConfigurationId": str,
        "configurationIds": Sequence[str],
    },
)

BatchDeleteImportDataErrorTypeDef = TypedDict(
    "BatchDeleteImportDataErrorTypeDef",
    {
        "importTaskId": str,
        "errorCode": BatchDeleteImportDataErrorCodeType,
        "errorDescription": str,
    },
    total=False,
)

BatchDeleteImportDataRequestRequestTypeDef = TypedDict(
    "BatchDeleteImportDataRequestRequestTypeDef",
    {
        "importTaskIds": Sequence[str],
    },
)

BatchDeleteImportDataResponseTypeDef = TypedDict(
    "BatchDeleteImportDataResponseTypeDef",
    {
        "errors": List["BatchDeleteImportDataErrorTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ConfigurationTagTypeDef = TypedDict(
    "ConfigurationTagTypeDef",
    {
        "configurationType": ConfigurationItemTypeType,
        "configurationId": str,
        "key": str,
        "value": str,
        "timeOfCreation": datetime,
    },
    total=False,
)

ContinuousExportDescriptionTypeDef = TypedDict(
    "ContinuousExportDescriptionTypeDef",
    {
        "exportId": str,
        "status": ContinuousExportStatusType,
        "statusDetail": str,
        "s3Bucket": str,
        "startTime": datetime,
        "stopTime": datetime,
        "dataSource": Literal["AGENT"],
        "schemaStorageConfig": Dict[str, str],
    },
    total=False,
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "configurationId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateTagsRequestRequestTypeDef = TypedDict(
    "CreateTagsRequestRequestTypeDef",
    {
        "configurationIds": Sequence[str],
        "tags": Sequence["TagTypeDef"],
    },
)

CustomerAgentInfoTypeDef = TypedDict(
    "CustomerAgentInfoTypeDef",
    {
        "activeAgents": int,
        "healthyAgents": int,
        "blackListedAgents": int,
        "shutdownAgents": int,
        "unhealthyAgents": int,
        "totalAgents": int,
        "unknownAgents": int,
    },
)

CustomerConnectorInfoTypeDef = TypedDict(
    "CustomerConnectorInfoTypeDef",
    {
        "activeConnectors": int,
        "healthyConnectors": int,
        "blackListedConnectors": int,
        "shutdownConnectors": int,
        "unhealthyConnectors": int,
        "totalConnectors": int,
        "unknownConnectors": int,
    },
)

DeleteApplicationsRequestRequestTypeDef = TypedDict(
    "DeleteApplicationsRequestRequestTypeDef",
    {
        "configurationIds": Sequence[str],
    },
)

_RequiredDeleteTagsRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTagsRequestRequestTypeDef",
    {
        "configurationIds": Sequence[str],
    },
)
_OptionalDeleteTagsRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTagsRequestRequestTypeDef",
    {
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class DeleteTagsRequestRequestTypeDef(
    _RequiredDeleteTagsRequestRequestTypeDef, _OptionalDeleteTagsRequestRequestTypeDef
):
    pass


DescribeAgentsRequestDescribeAgentsPaginateTypeDef = TypedDict(
    "DescribeAgentsRequestDescribeAgentsPaginateTypeDef",
    {
        "agentIds": Sequence[str],
        "filters": Sequence["FilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeAgentsRequestRequestTypeDef = TypedDict(
    "DescribeAgentsRequestRequestTypeDef",
    {
        "agentIds": Sequence[str],
        "filters": Sequence["FilterTypeDef"],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeAgentsResponseTypeDef = TypedDict(
    "DescribeAgentsResponseTypeDef",
    {
        "agentsInfo": List["AgentInfoTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeConfigurationsRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationsRequestRequestTypeDef",
    {
        "configurationIds": Sequence[str],
    },
)

DescribeConfigurationsResponseTypeDef = TypedDict(
    "DescribeConfigurationsResponseTypeDef",
    {
        "configurations": List[Dict[str, str]],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef = TypedDict(
    "DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef",
    {
        "exportIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeContinuousExportsRequestRequestTypeDef = TypedDict(
    "DescribeContinuousExportsRequestRequestTypeDef",
    {
        "exportIds": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeContinuousExportsResponseTypeDef = TypedDict(
    "DescribeContinuousExportsResponseTypeDef",
    {
        "descriptions": List["ContinuousExportDescriptionTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef = TypedDict(
    "DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef",
    {
        "exportIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeExportConfigurationsRequestRequestTypeDef = TypedDict(
    "DescribeExportConfigurationsRequestRequestTypeDef",
    {
        "exportIds": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeExportConfigurationsResponseTypeDef = TypedDict(
    "DescribeExportConfigurationsResponseTypeDef",
    {
        "exportsInfo": List["ExportInfoTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef = TypedDict(
    "DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef",
    {
        "exportIds": Sequence[str],
        "filters": Sequence["ExportFilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeExportTasksRequestRequestTypeDef = TypedDict(
    "DescribeExportTasksRequestRequestTypeDef",
    {
        "exportIds": Sequence[str],
        "filters": Sequence["ExportFilterTypeDef"],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeExportTasksResponseTypeDef = TypedDict(
    "DescribeExportTasksResponseTypeDef",
    {
        "exportsInfo": List["ExportInfoTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeImportTasksRequestRequestTypeDef = TypedDict(
    "DescribeImportTasksRequestRequestTypeDef",
    {
        "filters": Sequence["ImportTaskFilterTypeDef"],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeImportTasksResponseTypeDef = TypedDict(
    "DescribeImportTasksResponseTypeDef",
    {
        "nextToken": str,
        "tasks": List["ImportTaskTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTagsRequestDescribeTagsPaginateTypeDef = TypedDict(
    "DescribeTagsRequestDescribeTagsPaginateTypeDef",
    {
        "filters": Sequence["TagFilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeTagsRequestRequestTypeDef = TypedDict(
    "DescribeTagsRequestRequestTypeDef",
    {
        "filters": Sequence["TagFilterTypeDef"],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeTagsResponseTypeDef = TypedDict(
    "DescribeTagsResponseTypeDef",
    {
        "tags": List["ConfigurationTagTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef = TypedDict(
    "DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef",
    {
        "applicationConfigurationId": str,
        "configurationIds": Sequence[str],
    },
)

ExportConfigurationsResponseTypeDef = TypedDict(
    "ExportConfigurationsResponseTypeDef",
    {
        "exportId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExportFilterTypeDef = TypedDict(
    "ExportFilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
        "condition": str,
    },
)

_RequiredExportInfoTypeDef = TypedDict(
    "_RequiredExportInfoTypeDef",
    {
        "exportId": str,
        "exportStatus": ExportStatusType,
        "statusMessage": str,
        "exportRequestTime": datetime,
    },
)
_OptionalExportInfoTypeDef = TypedDict(
    "_OptionalExportInfoTypeDef",
    {
        "configurationsDownloadUrl": str,
        "isTruncated": bool,
        "requestedStartTime": datetime,
        "requestedEndTime": datetime,
    },
    total=False,
)


class ExportInfoTypeDef(_RequiredExportInfoTypeDef, _OptionalExportInfoTypeDef):
    pass


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
        "condition": str,
    },
)

GetDiscoverySummaryResponseTypeDef = TypedDict(
    "GetDiscoverySummaryResponseTypeDef",
    {
        "servers": int,
        "applications": int,
        "serversMappedToApplications": int,
        "serversMappedtoTags": int,
        "agentSummary": "CustomerAgentInfoTypeDef",
        "connectorSummary": "CustomerConnectorInfoTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportTaskFilterTypeDef = TypedDict(
    "ImportTaskFilterTypeDef",
    {
        "name": ImportTaskFilterNameType,
        "values": Sequence[str],
    },
    total=False,
)

ImportTaskTypeDef = TypedDict(
    "ImportTaskTypeDef",
    {
        "importTaskId": str,
        "clientRequestToken": str,
        "name": str,
        "importUrl": str,
        "status": ImportStatusType,
        "importRequestTime": datetime,
        "importCompletionTime": datetime,
        "importDeletedTime": datetime,
        "serverImportSuccess": int,
        "serverImportFailure": int,
        "applicationImportSuccess": int,
        "applicationImportFailure": int,
        "errorsAndFailedEntriesZip": str,
    },
    total=False,
)

_RequiredListConfigurationsRequestListConfigurationsPaginateTypeDef = TypedDict(
    "_RequiredListConfigurationsRequestListConfigurationsPaginateTypeDef",
    {
        "configurationType": ConfigurationItemTypeType,
    },
)
_OptionalListConfigurationsRequestListConfigurationsPaginateTypeDef = TypedDict(
    "_OptionalListConfigurationsRequestListConfigurationsPaginateTypeDef",
    {
        "filters": Sequence["FilterTypeDef"],
        "orderBy": Sequence["OrderByElementTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListConfigurationsRequestListConfigurationsPaginateTypeDef(
    _RequiredListConfigurationsRequestListConfigurationsPaginateTypeDef,
    _OptionalListConfigurationsRequestListConfigurationsPaginateTypeDef,
):
    pass


_RequiredListConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListConfigurationsRequestRequestTypeDef",
    {
        "configurationType": ConfigurationItemTypeType,
    },
)
_OptionalListConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListConfigurationsRequestRequestTypeDef",
    {
        "filters": Sequence["FilterTypeDef"],
        "maxResults": int,
        "nextToken": str,
        "orderBy": Sequence["OrderByElementTypeDef"],
    },
    total=False,
)


class ListConfigurationsRequestRequestTypeDef(
    _RequiredListConfigurationsRequestRequestTypeDef,
    _OptionalListConfigurationsRequestRequestTypeDef,
):
    pass


ListConfigurationsResponseTypeDef = TypedDict(
    "ListConfigurationsResponseTypeDef",
    {
        "configurations": List[Dict[str, str]],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListServerNeighborsRequestRequestTypeDef = TypedDict(
    "_RequiredListServerNeighborsRequestRequestTypeDef",
    {
        "configurationId": str,
    },
)
_OptionalListServerNeighborsRequestRequestTypeDef = TypedDict(
    "_OptionalListServerNeighborsRequestRequestTypeDef",
    {
        "portInformationNeeded": bool,
        "neighborConfigurationIds": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListServerNeighborsRequestRequestTypeDef(
    _RequiredListServerNeighborsRequestRequestTypeDef,
    _OptionalListServerNeighborsRequestRequestTypeDef,
):
    pass


ListServerNeighborsResponseTypeDef = TypedDict(
    "ListServerNeighborsResponseTypeDef",
    {
        "neighbors": List["NeighborConnectionDetailTypeDef"],
        "nextToken": str,
        "knownDependencyCount": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredNeighborConnectionDetailTypeDef = TypedDict(
    "_RequiredNeighborConnectionDetailTypeDef",
    {
        "sourceServerId": str,
        "destinationServerId": str,
        "connectionsCount": int,
    },
)
_OptionalNeighborConnectionDetailTypeDef = TypedDict(
    "_OptionalNeighborConnectionDetailTypeDef",
    {
        "destinationPort": int,
        "transportProtocol": str,
    },
    total=False,
)


class NeighborConnectionDetailTypeDef(
    _RequiredNeighborConnectionDetailTypeDef, _OptionalNeighborConnectionDetailTypeDef
):
    pass


_RequiredOrderByElementTypeDef = TypedDict(
    "_RequiredOrderByElementTypeDef",
    {
        "fieldName": str,
    },
)
_OptionalOrderByElementTypeDef = TypedDict(
    "_OptionalOrderByElementTypeDef",
    {
        "sortOrder": orderStringType,
    },
    total=False,
)


class OrderByElementTypeDef(_RequiredOrderByElementTypeDef, _OptionalOrderByElementTypeDef):
    pass


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

StartContinuousExportResponseTypeDef = TypedDict(
    "StartContinuousExportResponseTypeDef",
    {
        "exportId": str,
        "s3Bucket": str,
        "startTime": datetime,
        "dataSource": Literal["AGENT"],
        "schemaStorageConfig": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartDataCollectionByAgentIdsRequestRequestTypeDef = TypedDict(
    "StartDataCollectionByAgentIdsRequestRequestTypeDef",
    {
        "agentIds": Sequence[str],
    },
)

StartDataCollectionByAgentIdsResponseTypeDef = TypedDict(
    "StartDataCollectionByAgentIdsResponseTypeDef",
    {
        "agentsConfigurationStatus": List["AgentConfigurationStatusTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartExportTaskRequestRequestTypeDef = TypedDict(
    "StartExportTaskRequestRequestTypeDef",
    {
        "exportDataFormat": Sequence[ExportDataFormatType],
        "filters": Sequence["ExportFilterTypeDef"],
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
    },
    total=False,
)

StartExportTaskResponseTypeDef = TypedDict(
    "StartExportTaskResponseTypeDef",
    {
        "exportId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartImportTaskRequestRequestTypeDef = TypedDict(
    "_RequiredStartImportTaskRequestRequestTypeDef",
    {
        "name": str,
        "importUrl": str,
    },
)
_OptionalStartImportTaskRequestRequestTypeDef = TypedDict(
    "_OptionalStartImportTaskRequestRequestTypeDef",
    {
        "clientRequestToken": str,
    },
    total=False,
)


class StartImportTaskRequestRequestTypeDef(
    _RequiredStartImportTaskRequestRequestTypeDef, _OptionalStartImportTaskRequestRequestTypeDef
):
    pass


StartImportTaskResponseTypeDef = TypedDict(
    "StartImportTaskResponseTypeDef",
    {
        "task": "ImportTaskTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopContinuousExportRequestRequestTypeDef = TypedDict(
    "StopContinuousExportRequestRequestTypeDef",
    {
        "exportId": str,
    },
)

StopContinuousExportResponseTypeDef = TypedDict(
    "StopContinuousExportResponseTypeDef",
    {
        "startTime": datetime,
        "stopTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopDataCollectionByAgentIdsRequestRequestTypeDef = TypedDict(
    "StopDataCollectionByAgentIdsRequestRequestTypeDef",
    {
        "agentIds": Sequence[str],
    },
)

StopDataCollectionByAgentIdsResponseTypeDef = TypedDict(
    "StopDataCollectionByAgentIdsResponseTypeDef",
    {
        "agentsConfigurationStatus": List["AgentConfigurationStatusTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "configurationId": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass
