"""
Type annotations for route53resolver service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53resolver/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53resolver.type_defs import AssociateFirewallRuleGroupRequestRequestTypeDef

    data: AssociateFirewallRuleGroupRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import (
    ActionType,
    AutodefinedReverseFlagType,
    BlockResponseType,
    FirewallDomainListStatusType,
    FirewallDomainUpdateOperationType,
    FirewallFailOpenStatusType,
    FirewallRuleGroupAssociationStatusType,
    FirewallRuleGroupStatusType,
    IpAddressStatusType,
    MutationProtectionStatusType,
    ResolverAutodefinedReverseStatusType,
    ResolverDNSSECValidationStatusType,
    ResolverEndpointDirectionType,
    ResolverEndpointStatusType,
    ResolverQueryLogConfigAssociationErrorType,
    ResolverQueryLogConfigAssociationStatusType,
    ResolverQueryLogConfigStatusType,
    ResolverRuleAssociationStatusType,
    ResolverRuleStatusType,
    RuleTypeOptionType,
    ShareStatusType,
    SortOrderType,
    ValidationType,
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
    "AssociateFirewallRuleGroupRequestRequestTypeDef",
    "AssociateFirewallRuleGroupResponseTypeDef",
    "AssociateResolverEndpointIpAddressRequestRequestTypeDef",
    "AssociateResolverEndpointIpAddressResponseTypeDef",
    "AssociateResolverQueryLogConfigRequestRequestTypeDef",
    "AssociateResolverQueryLogConfigResponseTypeDef",
    "AssociateResolverRuleRequestRequestTypeDef",
    "AssociateResolverRuleResponseTypeDef",
    "CreateFirewallDomainListRequestRequestTypeDef",
    "CreateFirewallDomainListResponseTypeDef",
    "CreateFirewallRuleGroupRequestRequestTypeDef",
    "CreateFirewallRuleGroupResponseTypeDef",
    "CreateFirewallRuleRequestRequestTypeDef",
    "CreateFirewallRuleResponseTypeDef",
    "CreateResolverEndpointRequestRequestTypeDef",
    "CreateResolverEndpointResponseTypeDef",
    "CreateResolverQueryLogConfigRequestRequestTypeDef",
    "CreateResolverQueryLogConfigResponseTypeDef",
    "CreateResolverRuleRequestRequestTypeDef",
    "CreateResolverRuleResponseTypeDef",
    "DeleteFirewallDomainListRequestRequestTypeDef",
    "DeleteFirewallDomainListResponseTypeDef",
    "DeleteFirewallRuleGroupRequestRequestTypeDef",
    "DeleteFirewallRuleGroupResponseTypeDef",
    "DeleteFirewallRuleRequestRequestTypeDef",
    "DeleteFirewallRuleResponseTypeDef",
    "DeleteResolverEndpointRequestRequestTypeDef",
    "DeleteResolverEndpointResponseTypeDef",
    "DeleteResolverQueryLogConfigRequestRequestTypeDef",
    "DeleteResolverQueryLogConfigResponseTypeDef",
    "DeleteResolverRuleRequestRequestTypeDef",
    "DeleteResolverRuleResponseTypeDef",
    "DisassociateFirewallRuleGroupRequestRequestTypeDef",
    "DisassociateFirewallRuleGroupResponseTypeDef",
    "DisassociateResolverEndpointIpAddressRequestRequestTypeDef",
    "DisassociateResolverEndpointIpAddressResponseTypeDef",
    "DisassociateResolverQueryLogConfigRequestRequestTypeDef",
    "DisassociateResolverQueryLogConfigResponseTypeDef",
    "DisassociateResolverRuleRequestRequestTypeDef",
    "DisassociateResolverRuleResponseTypeDef",
    "FilterTypeDef",
    "FirewallConfigTypeDef",
    "FirewallDomainListMetadataTypeDef",
    "FirewallDomainListTypeDef",
    "FirewallRuleGroupAssociationTypeDef",
    "FirewallRuleGroupMetadataTypeDef",
    "FirewallRuleGroupTypeDef",
    "FirewallRuleTypeDef",
    "GetFirewallConfigRequestRequestTypeDef",
    "GetFirewallConfigResponseTypeDef",
    "GetFirewallDomainListRequestRequestTypeDef",
    "GetFirewallDomainListResponseTypeDef",
    "GetFirewallRuleGroupAssociationRequestRequestTypeDef",
    "GetFirewallRuleGroupAssociationResponseTypeDef",
    "GetFirewallRuleGroupPolicyRequestRequestTypeDef",
    "GetFirewallRuleGroupPolicyResponseTypeDef",
    "GetFirewallRuleGroupRequestRequestTypeDef",
    "GetFirewallRuleGroupResponseTypeDef",
    "GetResolverConfigRequestRequestTypeDef",
    "GetResolverConfigResponseTypeDef",
    "GetResolverDnssecConfigRequestRequestTypeDef",
    "GetResolverDnssecConfigResponseTypeDef",
    "GetResolverEndpointRequestRequestTypeDef",
    "GetResolverEndpointResponseTypeDef",
    "GetResolverQueryLogConfigAssociationRequestRequestTypeDef",
    "GetResolverQueryLogConfigAssociationResponseTypeDef",
    "GetResolverQueryLogConfigPolicyRequestRequestTypeDef",
    "GetResolverQueryLogConfigPolicyResponseTypeDef",
    "GetResolverQueryLogConfigRequestRequestTypeDef",
    "GetResolverQueryLogConfigResponseTypeDef",
    "GetResolverRuleAssociationRequestRequestTypeDef",
    "GetResolverRuleAssociationResponseTypeDef",
    "GetResolverRulePolicyRequestRequestTypeDef",
    "GetResolverRulePolicyResponseTypeDef",
    "GetResolverRuleRequestRequestTypeDef",
    "GetResolverRuleResponseTypeDef",
    "ImportFirewallDomainsRequestRequestTypeDef",
    "ImportFirewallDomainsResponseTypeDef",
    "IpAddressRequestTypeDef",
    "IpAddressResponseTypeDef",
    "IpAddressUpdateTypeDef",
    "ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef",
    "ListFirewallConfigsRequestRequestTypeDef",
    "ListFirewallConfigsResponseTypeDef",
    "ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef",
    "ListFirewallDomainListsRequestRequestTypeDef",
    "ListFirewallDomainListsResponseTypeDef",
    "ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    "ListFirewallDomainsRequestRequestTypeDef",
    "ListFirewallDomainsResponseTypeDef",
    "ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef",
    "ListFirewallRuleGroupAssociationsRequestRequestTypeDef",
    "ListFirewallRuleGroupAssociationsResponseTypeDef",
    "ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef",
    "ListFirewallRuleGroupsRequestRequestTypeDef",
    "ListFirewallRuleGroupsResponseTypeDef",
    "ListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    "ListFirewallRulesRequestRequestTypeDef",
    "ListFirewallRulesResponseTypeDef",
    "ListResolverConfigsRequestListResolverConfigsPaginateTypeDef",
    "ListResolverConfigsRequestRequestTypeDef",
    "ListResolverConfigsResponseTypeDef",
    "ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef",
    "ListResolverDnssecConfigsRequestRequestTypeDef",
    "ListResolverDnssecConfigsResponseTypeDef",
    "ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    "ListResolverEndpointIpAddressesRequestRequestTypeDef",
    "ListResolverEndpointIpAddressesResponseTypeDef",
    "ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef",
    "ListResolverEndpointsRequestRequestTypeDef",
    "ListResolverEndpointsResponseTypeDef",
    "ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef",
    "ListResolverQueryLogConfigAssociationsRequestRequestTypeDef",
    "ListResolverQueryLogConfigAssociationsResponseTypeDef",
    "ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef",
    "ListResolverQueryLogConfigsRequestRequestTypeDef",
    "ListResolverQueryLogConfigsResponseTypeDef",
    "ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef",
    "ListResolverRuleAssociationsRequestRequestTypeDef",
    "ListResolverRuleAssociationsResponseTypeDef",
    "ListResolverRulesRequestListResolverRulesPaginateTypeDef",
    "ListResolverRulesRequestRequestTypeDef",
    "ListResolverRulesResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutFirewallRuleGroupPolicyRequestRequestTypeDef",
    "PutFirewallRuleGroupPolicyResponseTypeDef",
    "PutResolverQueryLogConfigPolicyRequestRequestTypeDef",
    "PutResolverQueryLogConfigPolicyResponseTypeDef",
    "PutResolverRulePolicyRequestRequestTypeDef",
    "PutResolverRulePolicyResponseTypeDef",
    "ResolverConfigTypeDef",
    "ResolverDnssecConfigTypeDef",
    "ResolverEndpointTypeDef",
    "ResolverQueryLogConfigAssociationTypeDef",
    "ResolverQueryLogConfigTypeDef",
    "ResolverRuleAssociationTypeDef",
    "ResolverRuleConfigTypeDef",
    "ResolverRuleTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetAddressTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFirewallConfigRequestRequestTypeDef",
    "UpdateFirewallConfigResponseTypeDef",
    "UpdateFirewallDomainsRequestRequestTypeDef",
    "UpdateFirewallDomainsResponseTypeDef",
    "UpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    "UpdateFirewallRuleGroupAssociationResponseTypeDef",
    "UpdateFirewallRuleRequestRequestTypeDef",
    "UpdateFirewallRuleResponseTypeDef",
    "UpdateResolverConfigRequestRequestTypeDef",
    "UpdateResolverConfigResponseTypeDef",
    "UpdateResolverDnssecConfigRequestRequestTypeDef",
    "UpdateResolverDnssecConfigResponseTypeDef",
    "UpdateResolverEndpointRequestRequestTypeDef",
    "UpdateResolverEndpointResponseTypeDef",
    "UpdateResolverRuleRequestRequestTypeDef",
    "UpdateResolverRuleResponseTypeDef",
)

_RequiredAssociateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateFirewallRuleGroupRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "FirewallRuleGroupId": str,
        "VpcId": str,
        "Priority": int,
        "Name": str,
    },
)
_OptionalAssociateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateFirewallRuleGroupRequestRequestTypeDef",
    {
        "MutationProtection": MutationProtectionStatusType,
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)

class AssociateFirewallRuleGroupRequestRequestTypeDef(
    _RequiredAssociateFirewallRuleGroupRequestRequestTypeDef,
    _OptionalAssociateFirewallRuleGroupRequestRequestTypeDef,
):
    pass

AssociateFirewallRuleGroupResponseTypeDef = TypedDict(
    "AssociateFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": "FirewallRuleGroupAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociateResolverEndpointIpAddressRequestRequestTypeDef = TypedDict(
    "AssociateResolverEndpointIpAddressRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
        "IpAddress": "IpAddressUpdateTypeDef",
    },
)

AssociateResolverEndpointIpAddressResponseTypeDef = TypedDict(
    "AssociateResolverEndpointIpAddressResponseTypeDef",
    {
        "ResolverEndpoint": "ResolverEndpointTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "AssociateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
        "ResourceId": str,
    },
)

AssociateResolverQueryLogConfigResponseTypeDef = TypedDict(
    "AssociateResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfigAssociation": "ResolverQueryLogConfigAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAssociateResolverRuleRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
        "VPCId": str,
    },
)
_OptionalAssociateResolverRuleRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateResolverRuleRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)

class AssociateResolverRuleRequestRequestTypeDef(
    _RequiredAssociateResolverRuleRequestRequestTypeDef,
    _OptionalAssociateResolverRuleRequestRequestTypeDef,
):
    pass

AssociateResolverRuleResponseTypeDef = TypedDict(
    "AssociateResolverRuleResponseTypeDef",
    {
        "ResolverRuleAssociation": "ResolverRuleAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFirewallDomainListRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallDomainListRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Name": str,
    },
)
_OptionalCreateFirewallDomainListRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallDomainListRequestRequestTypeDef",
    {
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)

class CreateFirewallDomainListRequestRequestTypeDef(
    _RequiredCreateFirewallDomainListRequestRequestTypeDef,
    _OptionalCreateFirewallDomainListRequestRequestTypeDef,
):
    pass

CreateFirewallDomainListResponseTypeDef = TypedDict(
    "CreateFirewallDomainListResponseTypeDef",
    {
        "FirewallDomainList": "FirewallDomainListTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallRuleGroupRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "Name": str,
    },
)
_OptionalCreateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallRuleGroupRequestRequestTypeDef",
    {
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)

class CreateFirewallRuleGroupRequestRequestTypeDef(
    _RequiredCreateFirewallRuleGroupRequestRequestTypeDef,
    _OptionalCreateFirewallRuleGroupRequestRequestTypeDef,
):
    pass

CreateFirewallRuleGroupResponseTypeDef = TypedDict(
    "CreateFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroup": "FirewallRuleGroupTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallRuleRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
        "Priority": int,
        "Action": ActionType,
        "Name": str,
    },
)
_OptionalCreateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallRuleRequestRequestTypeDef",
    {
        "BlockResponse": BlockResponseType,
        "BlockOverrideDomain": str,
        "BlockOverrideDnsType": Literal["CNAME"],
        "BlockOverrideTtl": int,
    },
    total=False,
)

class CreateFirewallRuleRequestRequestTypeDef(
    _RequiredCreateFirewallRuleRequestRequestTypeDef,
    _OptionalCreateFirewallRuleRequestRequestTypeDef,
):
    pass

CreateFirewallRuleResponseTypeDef = TypedDict(
    "CreateFirewallRuleResponseTypeDef",
    {
        "FirewallRule": "FirewallRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResolverEndpointRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "SecurityGroupIds": Sequence[str],
        "Direction": ResolverEndpointDirectionType,
        "IpAddresses": Sequence["IpAddressRequestTypeDef"],
    },
)
_OptionalCreateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResolverEndpointRequestRequestTypeDef",
    {
        "Name": str,
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)

class CreateResolverEndpointRequestRequestTypeDef(
    _RequiredCreateResolverEndpointRequestRequestTypeDef,
    _OptionalCreateResolverEndpointRequestRequestTypeDef,
):
    pass

CreateResolverEndpointResponseTypeDef = TypedDict(
    "CreateResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": "ResolverEndpointTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "Name": str,
        "DestinationArn": str,
        "CreatorRequestId": str,
    },
)
_OptionalCreateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)

class CreateResolverQueryLogConfigRequestRequestTypeDef(
    _RequiredCreateResolverQueryLogConfigRequestRequestTypeDef,
    _OptionalCreateResolverQueryLogConfigRequestRequestTypeDef,
):
    pass

CreateResolverQueryLogConfigResponseTypeDef = TypedDict(
    "CreateResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfig": "ResolverQueryLogConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateResolverRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResolverRuleRequestRequestTypeDef",
    {
        "CreatorRequestId": str,
        "RuleType": RuleTypeOptionType,
        "DomainName": str,
    },
)
_OptionalCreateResolverRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResolverRuleRequestRequestTypeDef",
    {
        "Name": str,
        "TargetIps": Sequence["TargetAddressTypeDef"],
        "ResolverEndpointId": str,
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)

class CreateResolverRuleRequestRequestTypeDef(
    _RequiredCreateResolverRuleRequestRequestTypeDef,
    _OptionalCreateResolverRuleRequestRequestTypeDef,
):
    pass

CreateResolverRuleResponseTypeDef = TypedDict(
    "CreateResolverRuleResponseTypeDef",
    {
        "ResolverRule": "ResolverRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteFirewallDomainListRequestRequestTypeDef = TypedDict(
    "DeleteFirewallDomainListRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
    },
)

DeleteFirewallDomainListResponseTypeDef = TypedDict(
    "DeleteFirewallDomainListResponseTypeDef",
    {
        "FirewallDomainList": "FirewallDomainListTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteFirewallRuleGroupRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)

DeleteFirewallRuleGroupResponseTypeDef = TypedDict(
    "DeleteFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroup": "FirewallRuleGroupTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteFirewallRuleRequestRequestTypeDef = TypedDict(
    "DeleteFirewallRuleRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
    },
)

DeleteFirewallRuleResponseTypeDef = TypedDict(
    "DeleteFirewallRuleResponseTypeDef",
    {
        "FirewallRule": "FirewallRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteResolverEndpointRequestRequestTypeDef = TypedDict(
    "DeleteResolverEndpointRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)

DeleteResolverEndpointResponseTypeDef = TypedDict(
    "DeleteResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": "ResolverEndpointTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "DeleteResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
    },
)

DeleteResolverQueryLogConfigResponseTypeDef = TypedDict(
    "DeleteResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfig": "ResolverQueryLogConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteResolverRuleRequestRequestTypeDef = TypedDict(
    "DeleteResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
    },
)

DeleteResolverRuleResponseTypeDef = TypedDict(
    "DeleteResolverRuleResponseTypeDef",
    {
        "ResolverRule": "ResolverRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "DisassociateFirewallRuleGroupRequestRequestTypeDef",
    {
        "FirewallRuleGroupAssociationId": str,
    },
)

DisassociateFirewallRuleGroupResponseTypeDef = TypedDict(
    "DisassociateFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": "FirewallRuleGroupAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateResolverEndpointIpAddressRequestRequestTypeDef = TypedDict(
    "DisassociateResolverEndpointIpAddressRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
        "IpAddress": "IpAddressUpdateTypeDef",
    },
)

DisassociateResolverEndpointIpAddressResponseTypeDef = TypedDict(
    "DisassociateResolverEndpointIpAddressResponseTypeDef",
    {
        "ResolverEndpoint": "ResolverEndpointTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "DisassociateResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
        "ResourceId": str,
    },
)

DisassociateResolverQueryLogConfigResponseTypeDef = TypedDict(
    "DisassociateResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfigAssociation": "ResolverQueryLogConfigAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateResolverRuleRequestRequestTypeDef = TypedDict(
    "DisassociateResolverRuleRequestRequestTypeDef",
    {
        "VPCId": str,
        "ResolverRuleId": str,
    },
)

DisassociateResolverRuleResponseTypeDef = TypedDict(
    "DisassociateResolverRuleResponseTypeDef",
    {
        "ResolverRuleAssociation": "ResolverRuleAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
    total=False,
)

FirewallConfigTypeDef = TypedDict(
    "FirewallConfigTypeDef",
    {
        "Id": str,
        "ResourceId": str,
        "OwnerId": str,
        "FirewallFailOpen": FirewallFailOpenStatusType,
    },
    total=False,
)

FirewallDomainListMetadataTypeDef = TypedDict(
    "FirewallDomainListMetadataTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "CreatorRequestId": str,
        "ManagedOwnerName": str,
    },
    total=False,
)

FirewallDomainListTypeDef = TypedDict(
    "FirewallDomainListTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "DomainCount": int,
        "Status": FirewallDomainListStatusType,
        "StatusMessage": str,
        "ManagedOwnerName": str,
        "CreatorRequestId": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

FirewallRuleGroupAssociationTypeDef = TypedDict(
    "FirewallRuleGroupAssociationTypeDef",
    {
        "Id": str,
        "Arn": str,
        "FirewallRuleGroupId": str,
        "VpcId": str,
        "Name": str,
        "Priority": int,
        "MutationProtection": MutationProtectionStatusType,
        "ManagedOwnerName": str,
        "Status": FirewallRuleGroupAssociationStatusType,
        "StatusMessage": str,
        "CreatorRequestId": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

FirewallRuleGroupMetadataTypeDef = TypedDict(
    "FirewallRuleGroupMetadataTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "OwnerId": str,
        "CreatorRequestId": str,
        "ShareStatus": ShareStatusType,
    },
    total=False,
)

FirewallRuleGroupTypeDef = TypedDict(
    "FirewallRuleGroupTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "RuleCount": int,
        "Status": FirewallRuleGroupStatusType,
        "StatusMessage": str,
        "OwnerId": str,
        "CreatorRequestId": str,
        "ShareStatus": ShareStatusType,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

FirewallRuleTypeDef = TypedDict(
    "FirewallRuleTypeDef",
    {
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
        "Name": str,
        "Priority": int,
        "Action": ActionType,
        "BlockResponse": BlockResponseType,
        "BlockOverrideDomain": str,
        "BlockOverrideDnsType": Literal["CNAME"],
        "BlockOverrideTtl": int,
        "CreatorRequestId": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

GetFirewallConfigRequestRequestTypeDef = TypedDict(
    "GetFirewallConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

GetFirewallConfigResponseTypeDef = TypedDict(
    "GetFirewallConfigResponseTypeDef",
    {
        "FirewallConfig": "FirewallConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFirewallDomainListRequestRequestTypeDef = TypedDict(
    "GetFirewallDomainListRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
    },
)

GetFirewallDomainListResponseTypeDef = TypedDict(
    "GetFirewallDomainListResponseTypeDef",
    {
        "FirewallDomainList": "FirewallDomainListTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFirewallRuleGroupAssociationRequestRequestTypeDef = TypedDict(
    "GetFirewallRuleGroupAssociationRequestRequestTypeDef",
    {
        "FirewallRuleGroupAssociationId": str,
    },
)

GetFirewallRuleGroupAssociationResponseTypeDef = TypedDict(
    "GetFirewallRuleGroupAssociationResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": "FirewallRuleGroupAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFirewallRuleGroupPolicyRequestRequestTypeDef = TypedDict(
    "GetFirewallRuleGroupPolicyRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetFirewallRuleGroupPolicyResponseTypeDef = TypedDict(
    "GetFirewallRuleGroupPolicyResponseTypeDef",
    {
        "FirewallRuleGroupPolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFirewallRuleGroupRequestRequestTypeDef = TypedDict(
    "GetFirewallRuleGroupRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)

GetFirewallRuleGroupResponseTypeDef = TypedDict(
    "GetFirewallRuleGroupResponseTypeDef",
    {
        "FirewallRuleGroup": "FirewallRuleGroupTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverConfigRequestRequestTypeDef = TypedDict(
    "GetResolverConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

GetResolverConfigResponseTypeDef = TypedDict(
    "GetResolverConfigResponseTypeDef",
    {
        "ResolverConfig": "ResolverConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverDnssecConfigRequestRequestTypeDef = TypedDict(
    "GetResolverDnssecConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)

GetResolverDnssecConfigResponseTypeDef = TypedDict(
    "GetResolverDnssecConfigResponseTypeDef",
    {
        "ResolverDNSSECConfig": "ResolverDnssecConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverEndpointRequestRequestTypeDef = TypedDict(
    "GetResolverEndpointRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)

GetResolverEndpointResponseTypeDef = TypedDict(
    "GetResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": "ResolverEndpointTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverQueryLogConfigAssociationRequestRequestTypeDef = TypedDict(
    "GetResolverQueryLogConfigAssociationRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigAssociationId": str,
    },
)

GetResolverQueryLogConfigAssociationResponseTypeDef = TypedDict(
    "GetResolverQueryLogConfigAssociationResponseTypeDef",
    {
        "ResolverQueryLogConfigAssociation": "ResolverQueryLogConfigAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverQueryLogConfigPolicyRequestRequestTypeDef = TypedDict(
    "GetResolverQueryLogConfigPolicyRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetResolverQueryLogConfigPolicyResponseTypeDef = TypedDict(
    "GetResolverQueryLogConfigPolicyResponseTypeDef",
    {
        "ResolverQueryLogConfigPolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverQueryLogConfigRequestRequestTypeDef = TypedDict(
    "GetResolverQueryLogConfigRequestRequestTypeDef",
    {
        "ResolverQueryLogConfigId": str,
    },
)

GetResolverQueryLogConfigResponseTypeDef = TypedDict(
    "GetResolverQueryLogConfigResponseTypeDef",
    {
        "ResolverQueryLogConfig": "ResolverQueryLogConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverRuleAssociationRequestRequestTypeDef = TypedDict(
    "GetResolverRuleAssociationRequestRequestTypeDef",
    {
        "ResolverRuleAssociationId": str,
    },
)

GetResolverRuleAssociationResponseTypeDef = TypedDict(
    "GetResolverRuleAssociationResponseTypeDef",
    {
        "ResolverRuleAssociation": "ResolverRuleAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverRulePolicyRequestRequestTypeDef = TypedDict(
    "GetResolverRulePolicyRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetResolverRulePolicyResponseTypeDef = TypedDict(
    "GetResolverRulePolicyResponseTypeDef",
    {
        "ResolverRulePolicy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResolverRuleRequestRequestTypeDef = TypedDict(
    "GetResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
    },
)

GetResolverRuleResponseTypeDef = TypedDict(
    "GetResolverRuleResponseTypeDef",
    {
        "ResolverRule": "ResolverRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportFirewallDomainsRequestRequestTypeDef = TypedDict(
    "ImportFirewallDomainsRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
        "Operation": Literal["REPLACE"],
        "DomainFileUrl": str,
    },
)

ImportFirewallDomainsResponseTypeDef = TypedDict(
    "ImportFirewallDomainsResponseTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": FirewallDomainListStatusType,
        "StatusMessage": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredIpAddressRequestTypeDef = TypedDict(
    "_RequiredIpAddressRequestTypeDef",
    {
        "SubnetId": str,
    },
)
_OptionalIpAddressRequestTypeDef = TypedDict(
    "_OptionalIpAddressRequestTypeDef",
    {
        "Ip": str,
    },
    total=False,
)

class IpAddressRequestTypeDef(_RequiredIpAddressRequestTypeDef, _OptionalIpAddressRequestTypeDef):
    pass

IpAddressResponseTypeDef = TypedDict(
    "IpAddressResponseTypeDef",
    {
        "IpId": str,
        "SubnetId": str,
        "Ip": str,
        "Status": IpAddressStatusType,
        "StatusMessage": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

IpAddressUpdateTypeDef = TypedDict(
    "IpAddressUpdateTypeDef",
    {
        "IpId": str,
        "SubnetId": str,
        "Ip": str,
    },
    total=False,
)

ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef = TypedDict(
    "ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFirewallConfigsRequestRequestTypeDef = TypedDict(
    "ListFirewallConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFirewallConfigsResponseTypeDef = TypedDict(
    "ListFirewallConfigsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallConfigs": List["FirewallConfigTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef = TypedDict(
    "ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFirewallDomainListsRequestRequestTypeDef = TypedDict(
    "ListFirewallDomainListsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFirewallDomainListsResponseTypeDef = TypedDict(
    "ListFirewallDomainListsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallDomainLists": List["FirewallDomainListMetadataTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef = TypedDict(
    "_RequiredListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    {
        "FirewallDomainListId": str,
    },
)
_OptionalListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef = TypedDict(
    "_OptionalListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef(
    _RequiredListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef,
    _OptionalListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef,
):
    pass

_RequiredListFirewallDomainsRequestRequestTypeDef = TypedDict(
    "_RequiredListFirewallDomainsRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
    },
)
_OptionalListFirewallDomainsRequestRequestTypeDef = TypedDict(
    "_OptionalListFirewallDomainsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListFirewallDomainsRequestRequestTypeDef(
    _RequiredListFirewallDomainsRequestRequestTypeDef,
    _OptionalListFirewallDomainsRequestRequestTypeDef,
):
    pass

ListFirewallDomainsResponseTypeDef = TypedDict(
    "ListFirewallDomainsResponseTypeDef",
    {
        "NextToken": str,
        "Domains": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef = (
    TypedDict(
        "ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef",
        {
            "FirewallRuleGroupId": str,
            "VpcId": str,
            "Priority": int,
            "Status": FirewallRuleGroupAssociationStatusType,
            "PaginationConfig": "PaginatorConfigTypeDef",
        },
        total=False,
    )
)

ListFirewallRuleGroupAssociationsRequestRequestTypeDef = TypedDict(
    "ListFirewallRuleGroupAssociationsRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
        "VpcId": str,
        "Priority": int,
        "Status": FirewallRuleGroupAssociationStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFirewallRuleGroupAssociationsResponseTypeDef = TypedDict(
    "ListFirewallRuleGroupAssociationsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallRuleGroupAssociations": List["FirewallRuleGroupAssociationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef = TypedDict(
    "ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFirewallRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListFirewallRuleGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListFirewallRuleGroupsResponseTypeDef = TypedDict(
    "ListFirewallRuleGroupsResponseTypeDef",
    {
        "NextToken": str,
        "FirewallRuleGroups": List["FirewallRuleGroupMetadataTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListFirewallRulesRequestListFirewallRulesPaginateTypeDef = TypedDict(
    "_RequiredListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)
_OptionalListFirewallRulesRequestListFirewallRulesPaginateTypeDef = TypedDict(
    "_OptionalListFirewallRulesRequestListFirewallRulesPaginateTypeDef",
    {
        "Priority": int,
        "Action": ActionType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListFirewallRulesRequestListFirewallRulesPaginateTypeDef(
    _RequiredListFirewallRulesRequestListFirewallRulesPaginateTypeDef,
    _OptionalListFirewallRulesRequestListFirewallRulesPaginateTypeDef,
):
    pass

_RequiredListFirewallRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListFirewallRulesRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
    },
)
_OptionalListFirewallRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListFirewallRulesRequestRequestTypeDef",
    {
        "Priority": int,
        "Action": ActionType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListFirewallRulesRequestRequestTypeDef(
    _RequiredListFirewallRulesRequestRequestTypeDef, _OptionalListFirewallRulesRequestRequestTypeDef
):
    pass

ListFirewallRulesResponseTypeDef = TypedDict(
    "ListFirewallRulesResponseTypeDef",
    {
        "NextToken": str,
        "FirewallRules": List["FirewallRuleTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverConfigsRequestListResolverConfigsPaginateTypeDef = TypedDict(
    "ListResolverConfigsRequestListResolverConfigsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverConfigsRequestRequestTypeDef = TypedDict(
    "ListResolverConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListResolverConfigsResponseTypeDef = TypedDict(
    "ListResolverConfigsResponseTypeDef",
    {
        "NextToken": str,
        "ResolverConfigs": List["ResolverConfigTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef = TypedDict(
    "ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverDnssecConfigsRequestRequestTypeDef = TypedDict(
    "ListResolverDnssecConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence["FilterTypeDef"],
    },
    total=False,
)

ListResolverDnssecConfigsResponseTypeDef = TypedDict(
    "ListResolverDnssecConfigsResponseTypeDef",
    {
        "NextToken": str,
        "ResolverDnssecConfigs": List["ResolverDnssecConfigTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef = TypedDict(
    "_RequiredListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    {
        "ResolverEndpointId": str,
    },
)
_OptionalListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef = TypedDict(
    "_OptionalListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef(
    _RequiredListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef,
    _OptionalListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef,
):
    pass

_RequiredListResolverEndpointIpAddressesRequestRequestTypeDef = TypedDict(
    "_RequiredListResolverEndpointIpAddressesRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)
_OptionalListResolverEndpointIpAddressesRequestRequestTypeDef = TypedDict(
    "_OptionalListResolverEndpointIpAddressesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListResolverEndpointIpAddressesRequestRequestTypeDef(
    _RequiredListResolverEndpointIpAddressesRequestRequestTypeDef,
    _OptionalListResolverEndpointIpAddressesRequestRequestTypeDef,
):
    pass

ListResolverEndpointIpAddressesResponseTypeDef = TypedDict(
    "ListResolverEndpointIpAddressesResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "IpAddresses": List["IpAddressResponseTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef = TypedDict(
    "ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverEndpointsRequestRequestTypeDef = TypedDict(
    "ListResolverEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence["FilterTypeDef"],
    },
    total=False,
)

ListResolverEndpointsResponseTypeDef = TypedDict(
    "ListResolverEndpointsResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ResolverEndpoints": List["ResolverEndpointTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef = TypedDict(
    "ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
        "SortBy": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverQueryLogConfigAssociationsRequestRequestTypeDef = TypedDict(
    "ListResolverQueryLogConfigAssociationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence["FilterTypeDef"],
        "SortBy": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListResolverQueryLogConfigAssociationsResponseTypeDef = TypedDict(
    "ListResolverQueryLogConfigAssociationsResponseTypeDef",
    {
        "NextToken": str,
        "TotalCount": int,
        "TotalFilteredCount": int,
        "ResolverQueryLogConfigAssociations": List["ResolverQueryLogConfigAssociationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef = TypedDict(
    "ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
        "SortBy": str,
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverQueryLogConfigsRequestRequestTypeDef = TypedDict(
    "ListResolverQueryLogConfigsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence["FilterTypeDef"],
        "SortBy": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

ListResolverQueryLogConfigsResponseTypeDef = TypedDict(
    "ListResolverQueryLogConfigsResponseTypeDef",
    {
        "NextToken": str,
        "TotalCount": int,
        "TotalFilteredCount": int,
        "ResolverQueryLogConfigs": List["ResolverQueryLogConfigTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef = TypedDict(
    "ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverRuleAssociationsRequestRequestTypeDef = TypedDict(
    "ListResolverRuleAssociationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence["FilterTypeDef"],
    },
    total=False,
)

ListResolverRuleAssociationsResponseTypeDef = TypedDict(
    "ListResolverRuleAssociationsResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ResolverRuleAssociations": List["ResolverRuleAssociationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResolverRulesRequestListResolverRulesPaginateTypeDef = TypedDict(
    "ListResolverRulesRequestListResolverRulesPaginateTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListResolverRulesRequestRequestTypeDef = TypedDict(
    "ListResolverRulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence["FilterTypeDef"],
    },
    total=False,
)

ListResolverRulesResponseTypeDef = TypedDict(
    "ListResolverRulesResponseTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ResolverRules": List["ResolverRuleTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
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
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
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
        "Tags": List["TagTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
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

PutFirewallRuleGroupPolicyRequestRequestTypeDef = TypedDict(
    "PutFirewallRuleGroupPolicyRequestRequestTypeDef",
    {
        "Arn": str,
        "FirewallRuleGroupPolicy": str,
    },
)

PutFirewallRuleGroupPolicyResponseTypeDef = TypedDict(
    "PutFirewallRuleGroupPolicyResponseTypeDef",
    {
        "ReturnValue": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutResolverQueryLogConfigPolicyRequestRequestTypeDef = TypedDict(
    "PutResolverQueryLogConfigPolicyRequestRequestTypeDef",
    {
        "Arn": str,
        "ResolverQueryLogConfigPolicy": str,
    },
)

PutResolverQueryLogConfigPolicyResponseTypeDef = TypedDict(
    "PutResolverQueryLogConfigPolicyResponseTypeDef",
    {
        "ReturnValue": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutResolverRulePolicyRequestRequestTypeDef = TypedDict(
    "PutResolverRulePolicyRequestRequestTypeDef",
    {
        "Arn": str,
        "ResolverRulePolicy": str,
    },
)

PutResolverRulePolicyResponseTypeDef = TypedDict(
    "PutResolverRulePolicyResponseTypeDef",
    {
        "ReturnValue": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResolverConfigTypeDef = TypedDict(
    "ResolverConfigTypeDef",
    {
        "Id": str,
        "ResourceId": str,
        "OwnerId": str,
        "AutodefinedReverse": ResolverAutodefinedReverseStatusType,
    },
    total=False,
)

ResolverDnssecConfigTypeDef = TypedDict(
    "ResolverDnssecConfigTypeDef",
    {
        "Id": str,
        "OwnerId": str,
        "ResourceId": str,
        "ValidationStatus": ResolverDNSSECValidationStatusType,
    },
    total=False,
)

ResolverEndpointTypeDef = TypedDict(
    "ResolverEndpointTypeDef",
    {
        "Id": str,
        "CreatorRequestId": str,
        "Arn": str,
        "Name": str,
        "SecurityGroupIds": List[str],
        "Direction": ResolverEndpointDirectionType,
        "IpAddressCount": int,
        "HostVPCId": str,
        "Status": ResolverEndpointStatusType,
        "StatusMessage": str,
        "CreationTime": str,
        "ModificationTime": str,
    },
    total=False,
)

ResolverQueryLogConfigAssociationTypeDef = TypedDict(
    "ResolverQueryLogConfigAssociationTypeDef",
    {
        "Id": str,
        "ResolverQueryLogConfigId": str,
        "ResourceId": str,
        "Status": ResolverQueryLogConfigAssociationStatusType,
        "Error": ResolverQueryLogConfigAssociationErrorType,
        "ErrorMessage": str,
        "CreationTime": str,
    },
    total=False,
)

ResolverQueryLogConfigTypeDef = TypedDict(
    "ResolverQueryLogConfigTypeDef",
    {
        "Id": str,
        "OwnerId": str,
        "Status": ResolverQueryLogConfigStatusType,
        "ShareStatus": ShareStatusType,
        "AssociationCount": int,
        "Arn": str,
        "Name": str,
        "DestinationArn": str,
        "CreatorRequestId": str,
        "CreationTime": str,
    },
    total=False,
)

ResolverRuleAssociationTypeDef = TypedDict(
    "ResolverRuleAssociationTypeDef",
    {
        "Id": str,
        "ResolverRuleId": str,
        "Name": str,
        "VPCId": str,
        "Status": ResolverRuleAssociationStatusType,
        "StatusMessage": str,
    },
    total=False,
)

ResolverRuleConfigTypeDef = TypedDict(
    "ResolverRuleConfigTypeDef",
    {
        "Name": str,
        "TargetIps": Sequence["TargetAddressTypeDef"],
        "ResolverEndpointId": str,
    },
    total=False,
)

ResolverRuleTypeDef = TypedDict(
    "ResolverRuleTypeDef",
    {
        "Id": str,
        "CreatorRequestId": str,
        "Arn": str,
        "DomainName": str,
        "Status": ResolverRuleStatusType,
        "StatusMessage": str,
        "RuleType": RuleTypeOptionType,
        "Name": str,
        "TargetIps": List["TargetAddressTypeDef"],
        "ResolverEndpointId": str,
        "OwnerId": str,
        "ShareStatus": ShareStatusType,
        "CreationTime": str,
        "ModificationTime": str,
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

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence["TagTypeDef"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredTargetAddressTypeDef = TypedDict(
    "_RequiredTargetAddressTypeDef",
    {
        "Ip": str,
    },
)
_OptionalTargetAddressTypeDef = TypedDict(
    "_OptionalTargetAddressTypeDef",
    {
        "Port": int,
    },
    total=False,
)

class TargetAddressTypeDef(_RequiredTargetAddressTypeDef, _OptionalTargetAddressTypeDef):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateFirewallConfigRequestRequestTypeDef = TypedDict(
    "UpdateFirewallConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
        "FirewallFailOpen": FirewallFailOpenStatusType,
    },
)

UpdateFirewallConfigResponseTypeDef = TypedDict(
    "UpdateFirewallConfigResponseTypeDef",
    {
        "FirewallConfig": "FirewallConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFirewallDomainsRequestRequestTypeDef = TypedDict(
    "UpdateFirewallDomainsRequestRequestTypeDef",
    {
        "FirewallDomainListId": str,
        "Operation": FirewallDomainUpdateOperationType,
        "Domains": Sequence[str],
    },
)

UpdateFirewallDomainsResponseTypeDef = TypedDict(
    "UpdateFirewallDomainsResponseTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": FirewallDomainListStatusType,
        "StatusMessage": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateFirewallRuleGroupAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    {
        "FirewallRuleGroupAssociationId": str,
    },
)
_OptionalUpdateFirewallRuleGroupAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallRuleGroupAssociationRequestRequestTypeDef",
    {
        "Priority": int,
        "MutationProtection": MutationProtectionStatusType,
        "Name": str,
    },
    total=False,
)

class UpdateFirewallRuleGroupAssociationRequestRequestTypeDef(
    _RequiredUpdateFirewallRuleGroupAssociationRequestRequestTypeDef,
    _OptionalUpdateFirewallRuleGroupAssociationRequestRequestTypeDef,
):
    pass

UpdateFirewallRuleGroupAssociationResponseTypeDef = TypedDict(
    "UpdateFirewallRuleGroupAssociationResponseTypeDef",
    {
        "FirewallRuleGroupAssociation": "FirewallRuleGroupAssociationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallRuleRequestRequestTypeDef",
    {
        "FirewallRuleGroupId": str,
        "FirewallDomainListId": str,
    },
)
_OptionalUpdateFirewallRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallRuleRequestRequestTypeDef",
    {
        "Priority": int,
        "Action": ActionType,
        "BlockResponse": BlockResponseType,
        "BlockOverrideDomain": str,
        "BlockOverrideDnsType": Literal["CNAME"],
        "BlockOverrideTtl": int,
        "Name": str,
    },
    total=False,
)

class UpdateFirewallRuleRequestRequestTypeDef(
    _RequiredUpdateFirewallRuleRequestRequestTypeDef,
    _OptionalUpdateFirewallRuleRequestRequestTypeDef,
):
    pass

UpdateFirewallRuleResponseTypeDef = TypedDict(
    "UpdateFirewallRuleResponseTypeDef",
    {
        "FirewallRule": "FirewallRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateResolverConfigRequestRequestTypeDef = TypedDict(
    "UpdateResolverConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
        "AutodefinedReverseFlag": AutodefinedReverseFlagType,
    },
)

UpdateResolverConfigResponseTypeDef = TypedDict(
    "UpdateResolverConfigResponseTypeDef",
    {
        "ResolverConfig": "ResolverConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateResolverDnssecConfigRequestRequestTypeDef = TypedDict(
    "UpdateResolverDnssecConfigRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Validation": ValidationType,
    },
)

UpdateResolverDnssecConfigResponseTypeDef = TypedDict(
    "UpdateResolverDnssecConfigResponseTypeDef",
    {
        "ResolverDNSSECConfig": "ResolverDnssecConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResolverEndpointRequestRequestTypeDef",
    {
        "ResolverEndpointId": str,
    },
)
_OptionalUpdateResolverEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResolverEndpointRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)

class UpdateResolverEndpointRequestRequestTypeDef(
    _RequiredUpdateResolverEndpointRequestRequestTypeDef,
    _OptionalUpdateResolverEndpointRequestRequestTypeDef,
):
    pass

UpdateResolverEndpointResponseTypeDef = TypedDict(
    "UpdateResolverEndpointResponseTypeDef",
    {
        "ResolverEndpoint": "ResolverEndpointTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateResolverRuleRequestRequestTypeDef = TypedDict(
    "UpdateResolverRuleRequestRequestTypeDef",
    {
        "ResolverRuleId": str,
        "Config": "ResolverRuleConfigTypeDef",
    },
)

UpdateResolverRuleResponseTypeDef = TypedDict(
    "UpdateResolverRuleResponseTypeDef",
    {
        "ResolverRule": "ResolverRuleTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
