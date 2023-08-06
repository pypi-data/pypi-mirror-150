"""
Type annotations for organizations service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_organizations/type_defs/)

Usage::

    ```python
    from mypy_boto3_organizations.type_defs import AcceptHandshakeRequestRequestTypeDef

    data: AcceptHandshakeRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    AccountJoinedMethodType,
    AccountStatusType,
    ActionTypeType,
    ChildTypeType,
    CreateAccountFailureReasonType,
    CreateAccountStateType,
    EffectivePolicyTypeType,
    HandshakePartyTypeType,
    HandshakeResourceTypeType,
    HandshakeStateType,
    IAMUserAccessToBillingType,
    OrganizationFeatureSetType,
    ParentTypeType,
    PolicyTypeStatusType,
    PolicyTypeType,
    TargetTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptHandshakeRequestRequestTypeDef",
    "AcceptHandshakeResponseTypeDef",
    "AccountTypeDef",
    "AttachPolicyRequestRequestTypeDef",
    "CancelHandshakeRequestRequestTypeDef",
    "CancelHandshakeResponseTypeDef",
    "ChildTypeDef",
    "CloseAccountRequestRequestTypeDef",
    "CreateAccountRequestRequestTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateAccountStatusTypeDef",
    "CreateGovCloudAccountRequestRequestTypeDef",
    "CreateGovCloudAccountResponseTypeDef",
    "CreateOrganizationRequestRequestTypeDef",
    "CreateOrganizationResponseTypeDef",
    "CreateOrganizationalUnitRequestRequestTypeDef",
    "CreateOrganizationalUnitResponseTypeDef",
    "CreatePolicyRequestRequestTypeDef",
    "CreatePolicyResponseTypeDef",
    "DeclineHandshakeRequestRequestTypeDef",
    "DeclineHandshakeResponseTypeDef",
    "DelegatedAdministratorTypeDef",
    "DelegatedServiceTypeDef",
    "DeleteOrganizationalUnitRequestRequestTypeDef",
    "DeletePolicyRequestRequestTypeDef",
    "DeregisterDelegatedAdministratorRequestRequestTypeDef",
    "DescribeAccountRequestRequestTypeDef",
    "DescribeAccountResponseTypeDef",
    "DescribeCreateAccountStatusRequestRequestTypeDef",
    "DescribeCreateAccountStatusResponseTypeDef",
    "DescribeEffectivePolicyRequestRequestTypeDef",
    "DescribeEffectivePolicyResponseTypeDef",
    "DescribeHandshakeRequestRequestTypeDef",
    "DescribeHandshakeResponseTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DescribeOrganizationalUnitRequestRequestTypeDef",
    "DescribeOrganizationalUnitResponseTypeDef",
    "DescribePolicyRequestRequestTypeDef",
    "DescribePolicyResponseTypeDef",
    "DetachPolicyRequestRequestTypeDef",
    "DisableAWSServiceAccessRequestRequestTypeDef",
    "DisablePolicyTypeRequestRequestTypeDef",
    "DisablePolicyTypeResponseTypeDef",
    "EffectivePolicyTypeDef",
    "EnableAWSServiceAccessRequestRequestTypeDef",
    "EnableAllFeaturesResponseTypeDef",
    "EnablePolicyTypeRequestRequestTypeDef",
    "EnablePolicyTypeResponseTypeDef",
    "EnabledServicePrincipalTypeDef",
    "HandshakeFilterTypeDef",
    "HandshakePartyTypeDef",
    "HandshakeResourceTypeDef",
    "HandshakeTypeDef",
    "InviteAccountToOrganizationRequestRequestTypeDef",
    "InviteAccountToOrganizationResponseTypeDef",
    "ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef",
    "ListAWSServiceAccessForOrganizationRequestRequestTypeDef",
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    "ListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    "ListAccountsForParentRequestRequestTypeDef",
    "ListAccountsForParentResponseTypeDef",
    "ListAccountsRequestListAccountsPaginateTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "ListAccountsResponseTypeDef",
    "ListChildrenRequestListChildrenPaginateTypeDef",
    "ListChildrenRequestRequestTypeDef",
    "ListChildrenResponseTypeDef",
    "ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef",
    "ListCreateAccountStatusRequestRequestTypeDef",
    "ListCreateAccountStatusResponseTypeDef",
    "ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef",
    "ListDelegatedAdministratorsRequestRequestTypeDef",
    "ListDelegatedAdministratorsResponseTypeDef",
    "ListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    "ListDelegatedServicesForAccountRequestRequestTypeDef",
    "ListDelegatedServicesForAccountResponseTypeDef",
    "ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef",
    "ListHandshakesForAccountRequestRequestTypeDef",
    "ListHandshakesForAccountResponseTypeDef",
    "ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef",
    "ListHandshakesForOrganizationRequestRequestTypeDef",
    "ListHandshakesForOrganizationResponseTypeDef",
    "ListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    "ListOrganizationalUnitsForParentRequestRequestTypeDef",
    "ListOrganizationalUnitsForParentResponseTypeDef",
    "ListParentsRequestListParentsPaginateTypeDef",
    "ListParentsRequestRequestTypeDef",
    "ListParentsResponseTypeDef",
    "ListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    "ListPoliciesForTargetRequestRequestTypeDef",
    "ListPoliciesForTargetResponseTypeDef",
    "ListPoliciesRequestListPoliciesPaginateTypeDef",
    "ListPoliciesRequestRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListRootsRequestListRootsPaginateTypeDef",
    "ListRootsRequestRequestTypeDef",
    "ListRootsResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    "ListTargetsForPolicyRequestRequestTypeDef",
    "ListTargetsForPolicyResponseTypeDef",
    "MoveAccountRequestRequestTypeDef",
    "OrganizationTypeDef",
    "OrganizationalUnitTypeDef",
    "PaginatorConfigTypeDef",
    "ParentTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTargetSummaryTypeDef",
    "PolicyTypeDef",
    "PolicyTypeSummaryTypeDef",
    "RegisterDelegatedAdministratorRequestRequestTypeDef",
    "RemoveAccountFromOrganizationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RootTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateOrganizationalUnitRequestRequestTypeDef",
    "UpdateOrganizationalUnitResponseTypeDef",
    "UpdatePolicyRequestRequestTypeDef",
    "UpdatePolicyResponseTypeDef",
)

AcceptHandshakeRequestRequestTypeDef = TypedDict(
    "AcceptHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

AcceptHandshakeResponseTypeDef = TypedDict(
    "AcceptHandshakeResponseTypeDef",
    {
        "Handshake": "HandshakeTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Email": str,
        "Name": str,
        "Status": AccountStatusType,
        "JoinedMethod": AccountJoinedMethodType,
        "JoinedTimestamp": datetime,
    },
    total=False,
)

AttachPolicyRequestRequestTypeDef = TypedDict(
    "AttachPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
        "TargetId": str,
    },
)

CancelHandshakeRequestRequestTypeDef = TypedDict(
    "CancelHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

CancelHandshakeResponseTypeDef = TypedDict(
    "CancelHandshakeResponseTypeDef",
    {
        "Handshake": "HandshakeTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ChildTypeDef = TypedDict(
    "ChildTypeDef",
    {
        "Id": str,
        "Type": ChildTypeType,
    },
    total=False,
)

CloseAccountRequestRequestTypeDef = TypedDict(
    "CloseAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

_RequiredCreateAccountRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccountRequestRequestTypeDef",
    {
        "Email": str,
        "AccountName": str,
    },
)
_OptionalCreateAccountRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccountRequestRequestTypeDef",
    {
        "RoleName": str,
        "IamUserAccessToBilling": IAMUserAccessToBillingType,
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateAccountRequestRequestTypeDef(
    _RequiredCreateAccountRequestRequestTypeDef, _OptionalCreateAccountRequestRequestTypeDef
):
    pass


CreateAccountResponseTypeDef = TypedDict(
    "CreateAccountResponseTypeDef",
    {
        "CreateAccountStatus": "CreateAccountStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAccountStatusTypeDef = TypedDict(
    "CreateAccountStatusTypeDef",
    {
        "Id": str,
        "AccountName": str,
        "State": CreateAccountStateType,
        "RequestedTimestamp": datetime,
        "CompletedTimestamp": datetime,
        "AccountId": str,
        "GovCloudAccountId": str,
        "FailureReason": CreateAccountFailureReasonType,
    },
    total=False,
)

_RequiredCreateGovCloudAccountRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGovCloudAccountRequestRequestTypeDef",
    {
        "Email": str,
        "AccountName": str,
    },
)
_OptionalCreateGovCloudAccountRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGovCloudAccountRequestRequestTypeDef",
    {
        "RoleName": str,
        "IamUserAccessToBilling": IAMUserAccessToBillingType,
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateGovCloudAccountRequestRequestTypeDef(
    _RequiredCreateGovCloudAccountRequestRequestTypeDef,
    _OptionalCreateGovCloudAccountRequestRequestTypeDef,
):
    pass


CreateGovCloudAccountResponseTypeDef = TypedDict(
    "CreateGovCloudAccountResponseTypeDef",
    {
        "CreateAccountStatus": "CreateAccountStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateOrganizationRequestRequestTypeDef = TypedDict(
    "CreateOrganizationRequestRequestTypeDef",
    {
        "FeatureSet": OrganizationFeatureSetType,
    },
    total=False,
)

CreateOrganizationResponseTypeDef = TypedDict(
    "CreateOrganizationResponseTypeDef",
    {
        "Organization": "OrganizationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOrganizationalUnitRequestRequestTypeDef",
    {
        "ParentId": str,
        "Name": str,
    },
)
_OptionalCreateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOrganizationalUnitRequestRequestTypeDef",
    {
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateOrganizationalUnitRequestRequestTypeDef(
    _RequiredCreateOrganizationalUnitRequestRequestTypeDef,
    _OptionalCreateOrganizationalUnitRequestRequestTypeDef,
):
    pass


CreateOrganizationalUnitResponseTypeDef = TypedDict(
    "CreateOrganizationalUnitResponseTypeDef",
    {
        "OrganizationalUnit": "OrganizationalUnitTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyRequestRequestTypeDef",
    {
        "Content": str,
        "Description": str,
        "Name": str,
        "Type": PolicyTypeType,
    },
)
_OptionalCreatePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyRequestRequestTypeDef",
    {
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreatePolicyRequestRequestTypeDef(
    _RequiredCreatePolicyRequestRequestTypeDef, _OptionalCreatePolicyRequestRequestTypeDef
):
    pass


CreatePolicyResponseTypeDef = TypedDict(
    "CreatePolicyResponseTypeDef",
    {
        "Policy": "PolicyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeclineHandshakeRequestRequestTypeDef = TypedDict(
    "DeclineHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

DeclineHandshakeResponseTypeDef = TypedDict(
    "DeclineHandshakeResponseTypeDef",
    {
        "Handshake": "HandshakeTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DelegatedAdministratorTypeDef = TypedDict(
    "DelegatedAdministratorTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Email": str,
        "Name": str,
        "Status": AccountStatusType,
        "JoinedMethod": AccountJoinedMethodType,
        "JoinedTimestamp": datetime,
        "DelegationEnabledDate": datetime,
    },
    total=False,
)

DelegatedServiceTypeDef = TypedDict(
    "DelegatedServiceTypeDef",
    {
        "ServicePrincipal": str,
        "DelegationEnabledDate": datetime,
    },
    total=False,
)

DeleteOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "DeleteOrganizationalUnitRequestRequestTypeDef",
    {
        "OrganizationalUnitId": str,
    },
)

DeletePolicyRequestRequestTypeDef = TypedDict(
    "DeletePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

DeregisterDelegatedAdministratorRequestRequestTypeDef = TypedDict(
    "DeregisterDelegatedAdministratorRequestRequestTypeDef",
    {
        "AccountId": str,
        "ServicePrincipal": str,
    },
)

DescribeAccountRequestRequestTypeDef = TypedDict(
    "DescribeAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

DescribeAccountResponseTypeDef = TypedDict(
    "DescribeAccountResponseTypeDef",
    {
        "Account": "AccountTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCreateAccountStatusRequestRequestTypeDef = TypedDict(
    "DescribeCreateAccountStatusRequestRequestTypeDef",
    {
        "CreateAccountRequestId": str,
    },
)

DescribeCreateAccountStatusResponseTypeDef = TypedDict(
    "DescribeCreateAccountStatusResponseTypeDef",
    {
        "CreateAccountStatus": "CreateAccountStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeEffectivePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEffectivePolicyRequestRequestTypeDef",
    {
        "PolicyType": EffectivePolicyTypeType,
    },
)
_OptionalDescribeEffectivePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEffectivePolicyRequestRequestTypeDef",
    {
        "TargetId": str,
    },
    total=False,
)


class DescribeEffectivePolicyRequestRequestTypeDef(
    _RequiredDescribeEffectivePolicyRequestRequestTypeDef,
    _OptionalDescribeEffectivePolicyRequestRequestTypeDef,
):
    pass


DescribeEffectivePolicyResponseTypeDef = TypedDict(
    "DescribeEffectivePolicyResponseTypeDef",
    {
        "EffectivePolicy": "EffectivePolicyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeHandshakeRequestRequestTypeDef = TypedDict(
    "DescribeHandshakeRequestRequestTypeDef",
    {
        "HandshakeId": str,
    },
)

DescribeHandshakeResponseTypeDef = TypedDict(
    "DescribeHandshakeResponseTypeDef",
    {
        "Handshake": "HandshakeTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOrganizationResponseTypeDef = TypedDict(
    "DescribeOrganizationResponseTypeDef",
    {
        "Organization": "OrganizationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "DescribeOrganizationalUnitRequestRequestTypeDef",
    {
        "OrganizationalUnitId": str,
    },
)

DescribeOrganizationalUnitResponseTypeDef = TypedDict(
    "DescribeOrganizationalUnitResponseTypeDef",
    {
        "OrganizationalUnit": "OrganizationalUnitTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePolicyRequestRequestTypeDef = TypedDict(
    "DescribePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)

DescribePolicyResponseTypeDef = TypedDict(
    "DescribePolicyResponseTypeDef",
    {
        "Policy": "PolicyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetachPolicyRequestRequestTypeDef = TypedDict(
    "DetachPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
        "TargetId": str,
    },
)

DisableAWSServiceAccessRequestRequestTypeDef = TypedDict(
    "DisableAWSServiceAccessRequestRequestTypeDef",
    {
        "ServicePrincipal": str,
    },
)

DisablePolicyTypeRequestRequestTypeDef = TypedDict(
    "DisablePolicyTypeRequestRequestTypeDef",
    {
        "RootId": str,
        "PolicyType": PolicyTypeType,
    },
)

DisablePolicyTypeResponseTypeDef = TypedDict(
    "DisablePolicyTypeResponseTypeDef",
    {
        "Root": "RootTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EffectivePolicyTypeDef = TypedDict(
    "EffectivePolicyTypeDef",
    {
        "PolicyContent": str,
        "LastUpdatedTimestamp": datetime,
        "TargetId": str,
        "PolicyType": EffectivePolicyTypeType,
    },
    total=False,
)

EnableAWSServiceAccessRequestRequestTypeDef = TypedDict(
    "EnableAWSServiceAccessRequestRequestTypeDef",
    {
        "ServicePrincipal": str,
    },
)

EnableAllFeaturesResponseTypeDef = TypedDict(
    "EnableAllFeaturesResponseTypeDef",
    {
        "Handshake": "HandshakeTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnablePolicyTypeRequestRequestTypeDef = TypedDict(
    "EnablePolicyTypeRequestRequestTypeDef",
    {
        "RootId": str,
        "PolicyType": PolicyTypeType,
    },
)

EnablePolicyTypeResponseTypeDef = TypedDict(
    "EnablePolicyTypeResponseTypeDef",
    {
        "Root": "RootTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnabledServicePrincipalTypeDef = TypedDict(
    "EnabledServicePrincipalTypeDef",
    {
        "ServicePrincipal": str,
        "DateEnabled": datetime,
    },
    total=False,
)

HandshakeFilterTypeDef = TypedDict(
    "HandshakeFilterTypeDef",
    {
        "ActionType": ActionTypeType,
        "ParentHandshakeId": str,
    },
    total=False,
)

HandshakePartyTypeDef = TypedDict(
    "HandshakePartyTypeDef",
    {
        "Id": str,
        "Type": HandshakePartyTypeType,
    },
)

HandshakeResourceTypeDef = TypedDict(
    "HandshakeResourceTypeDef",
    {
        "Value": str,
        "Type": HandshakeResourceTypeType,
        "Resources": List[Dict[str, Any]],
    },
    total=False,
)

HandshakeTypeDef = TypedDict(
    "HandshakeTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Parties": List["HandshakePartyTypeDef"],
        "State": HandshakeStateType,
        "RequestedTimestamp": datetime,
        "ExpirationTimestamp": datetime,
        "Action": ActionTypeType,
        "Resources": List["HandshakeResourceTypeDef"],
    },
    total=False,
)

_RequiredInviteAccountToOrganizationRequestRequestTypeDef = TypedDict(
    "_RequiredInviteAccountToOrganizationRequestRequestTypeDef",
    {
        "Target": "HandshakePartyTypeDef",
    },
)
_OptionalInviteAccountToOrganizationRequestRequestTypeDef = TypedDict(
    "_OptionalInviteAccountToOrganizationRequestRequestTypeDef",
    {
        "Notes": str,
        "Tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class InviteAccountToOrganizationRequestRequestTypeDef(
    _RequiredInviteAccountToOrganizationRequestRequestTypeDef,
    _OptionalInviteAccountToOrganizationRequestRequestTypeDef,
):
    pass


InviteAccountToOrganizationResponseTypeDef = TypedDict(
    "InviteAccountToOrganizationResponseTypeDef",
    {
        "Handshake": "HandshakeTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationRequestListAWSServiceAccessForOrganizationPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAWSServiceAccessForOrganizationRequestRequestTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListAWSServiceAccessForOrganizationResponseTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    {
        "EnabledServicePrincipals": List["EnabledServicePrincipalTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListAccountsForParentRequestListAccountsForParentPaginateTypeDef = TypedDict(
    "_RequiredListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListAccountsForParentRequestListAccountsForParentPaginateTypeDef = TypedDict(
    "_OptionalListAccountsForParentRequestListAccountsForParentPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListAccountsForParentRequestListAccountsForParentPaginateTypeDef(
    _RequiredListAccountsForParentRequestListAccountsForParentPaginateTypeDef,
    _OptionalListAccountsForParentRequestListAccountsForParentPaginateTypeDef,
):
    pass


_RequiredListAccountsForParentRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountsForParentRequestRequestTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListAccountsForParentRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountsForParentRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAccountsForParentRequestRequestTypeDef(
    _RequiredListAccountsForParentRequestRequestTypeDef,
    _OptionalListAccountsForParentRequestRequestTypeDef,
):
    pass


ListAccountsForParentResponseTypeDef = TypedDict(
    "ListAccountsForParentResponseTypeDef",
    {
        "Accounts": List["AccountTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAccountsRequestListAccountsPaginateTypeDef = TypedDict(
    "ListAccountsRequestListAccountsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAccountsRequestRequestTypeDef = TypedDict(
    "ListAccountsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef",
    {
        "Accounts": List["AccountTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListChildrenRequestListChildrenPaginateTypeDef = TypedDict(
    "_RequiredListChildrenRequestListChildrenPaginateTypeDef",
    {
        "ParentId": str,
        "ChildType": ChildTypeType,
    },
)
_OptionalListChildrenRequestListChildrenPaginateTypeDef = TypedDict(
    "_OptionalListChildrenRequestListChildrenPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListChildrenRequestListChildrenPaginateTypeDef(
    _RequiredListChildrenRequestListChildrenPaginateTypeDef,
    _OptionalListChildrenRequestListChildrenPaginateTypeDef,
):
    pass


_RequiredListChildrenRequestRequestTypeDef = TypedDict(
    "_RequiredListChildrenRequestRequestTypeDef",
    {
        "ParentId": str,
        "ChildType": ChildTypeType,
    },
)
_OptionalListChildrenRequestRequestTypeDef = TypedDict(
    "_OptionalListChildrenRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListChildrenRequestRequestTypeDef(
    _RequiredListChildrenRequestRequestTypeDef, _OptionalListChildrenRequestRequestTypeDef
):
    pass


ListChildrenResponseTypeDef = TypedDict(
    "ListChildrenResponseTypeDef",
    {
        "Children": List["ChildTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef = TypedDict(
    "ListCreateAccountStatusRequestListCreateAccountStatusPaginateTypeDef",
    {
        "States": Sequence[CreateAccountStateType],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCreateAccountStatusRequestRequestTypeDef = TypedDict(
    "ListCreateAccountStatusRequestRequestTypeDef",
    {
        "States": Sequence[CreateAccountStateType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListCreateAccountStatusResponseTypeDef = TypedDict(
    "ListCreateAccountStatusResponseTypeDef",
    {
        "CreateAccountStatuses": List["CreateAccountStatusTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef = TypedDict(
    "ListDelegatedAdministratorsRequestListDelegatedAdministratorsPaginateTypeDef",
    {
        "ServicePrincipal": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDelegatedAdministratorsRequestRequestTypeDef = TypedDict(
    "ListDelegatedAdministratorsRequestRequestTypeDef",
    {
        "ServicePrincipal": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDelegatedAdministratorsResponseTypeDef = TypedDict(
    "ListDelegatedAdministratorsResponseTypeDef",
    {
        "DelegatedAdministrators": List["DelegatedAdministratorTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef = TypedDict(
    "_RequiredListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef = TypedDict(
    "_OptionalListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef(
    _RequiredListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef,
    _OptionalListDelegatedServicesForAccountRequestListDelegatedServicesForAccountPaginateTypeDef,
):
    pass


_RequiredListDelegatedServicesForAccountRequestRequestTypeDef = TypedDict(
    "_RequiredListDelegatedServicesForAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListDelegatedServicesForAccountRequestRequestTypeDef = TypedDict(
    "_OptionalListDelegatedServicesForAccountRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDelegatedServicesForAccountRequestRequestTypeDef(
    _RequiredListDelegatedServicesForAccountRequestRequestTypeDef,
    _OptionalListDelegatedServicesForAccountRequestRequestTypeDef,
):
    pass


ListDelegatedServicesForAccountResponseTypeDef = TypedDict(
    "ListDelegatedServicesForAccountResponseTypeDef",
    {
        "DelegatedServices": List["DelegatedServiceTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef = TypedDict(
    "ListHandshakesForAccountRequestListHandshakesForAccountPaginateTypeDef",
    {
        "Filter": "HandshakeFilterTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListHandshakesForAccountRequestRequestTypeDef = TypedDict(
    "ListHandshakesForAccountRequestRequestTypeDef",
    {
        "Filter": "HandshakeFilterTypeDef",
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListHandshakesForAccountResponseTypeDef = TypedDict(
    "ListHandshakesForAccountResponseTypeDef",
    {
        "Handshakes": List["HandshakeTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef = TypedDict(
    "ListHandshakesForOrganizationRequestListHandshakesForOrganizationPaginateTypeDef",
    {
        "Filter": "HandshakeFilterTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListHandshakesForOrganizationRequestRequestTypeDef = TypedDict(
    "ListHandshakesForOrganizationRequestRequestTypeDef",
    {
        "Filter": "HandshakeFilterTypeDef",
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListHandshakesForOrganizationResponseTypeDef = TypedDict(
    "ListHandshakesForOrganizationResponseTypeDef",
    {
        "Handshakes": List["HandshakeTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef = TypedDict(
    "_RequiredListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef = TypedDict(
    "_OptionalListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef(
    _RequiredListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef,
    _OptionalListOrganizationalUnitsForParentRequestListOrganizationalUnitsForParentPaginateTypeDef,
):
    pass


_RequiredListOrganizationalUnitsForParentRequestRequestTypeDef = TypedDict(
    "_RequiredListOrganizationalUnitsForParentRequestRequestTypeDef",
    {
        "ParentId": str,
    },
)
_OptionalListOrganizationalUnitsForParentRequestRequestTypeDef = TypedDict(
    "_OptionalListOrganizationalUnitsForParentRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListOrganizationalUnitsForParentRequestRequestTypeDef(
    _RequiredListOrganizationalUnitsForParentRequestRequestTypeDef,
    _OptionalListOrganizationalUnitsForParentRequestRequestTypeDef,
):
    pass


ListOrganizationalUnitsForParentResponseTypeDef = TypedDict(
    "ListOrganizationalUnitsForParentResponseTypeDef",
    {
        "OrganizationalUnits": List["OrganizationalUnitTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListParentsRequestListParentsPaginateTypeDef = TypedDict(
    "_RequiredListParentsRequestListParentsPaginateTypeDef",
    {
        "ChildId": str,
    },
)
_OptionalListParentsRequestListParentsPaginateTypeDef = TypedDict(
    "_OptionalListParentsRequestListParentsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListParentsRequestListParentsPaginateTypeDef(
    _RequiredListParentsRequestListParentsPaginateTypeDef,
    _OptionalListParentsRequestListParentsPaginateTypeDef,
):
    pass


_RequiredListParentsRequestRequestTypeDef = TypedDict(
    "_RequiredListParentsRequestRequestTypeDef",
    {
        "ChildId": str,
    },
)
_OptionalListParentsRequestRequestTypeDef = TypedDict(
    "_OptionalListParentsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListParentsRequestRequestTypeDef(
    _RequiredListParentsRequestRequestTypeDef, _OptionalListParentsRequestRequestTypeDef
):
    pass


ListParentsResponseTypeDef = TypedDict(
    "ListParentsResponseTypeDef",
    {
        "Parents": List["ParentTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef = TypedDict(
    "_RequiredListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    {
        "TargetId": str,
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef = TypedDict(
    "_OptionalListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef(
    _RequiredListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef,
    _OptionalListPoliciesForTargetRequestListPoliciesForTargetPaginateTypeDef,
):
    pass


_RequiredListPoliciesForTargetRequestRequestTypeDef = TypedDict(
    "_RequiredListPoliciesForTargetRequestRequestTypeDef",
    {
        "TargetId": str,
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesForTargetRequestRequestTypeDef = TypedDict(
    "_OptionalListPoliciesForTargetRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPoliciesForTargetRequestRequestTypeDef(
    _RequiredListPoliciesForTargetRequestRequestTypeDef,
    _OptionalListPoliciesForTargetRequestRequestTypeDef,
):
    pass


ListPoliciesForTargetResponseTypeDef = TypedDict(
    "ListPoliciesForTargetResponseTypeDef",
    {
        "Policies": List["PolicySummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListPoliciesRequestListPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListPoliciesRequestListPoliciesPaginateTypeDef",
    {
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesRequestListPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListPoliciesRequestListPoliciesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListPoliciesRequestListPoliciesPaginateTypeDef(
    _RequiredListPoliciesRequestListPoliciesPaginateTypeDef,
    _OptionalListPoliciesRequestListPoliciesPaginateTypeDef,
):
    pass


_RequiredListPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListPoliciesRequestRequestTypeDef",
    {
        "Filter": PolicyTypeType,
    },
)
_OptionalListPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListPoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPoliciesRequestRequestTypeDef(
    _RequiredListPoliciesRequestRequestTypeDef, _OptionalListPoliciesRequestRequestTypeDef
):
    pass


ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {
        "Policies": List["PolicySummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRootsRequestListRootsPaginateTypeDef = TypedDict(
    "ListRootsRequestListRootsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRootsRequestRequestTypeDef = TypedDict(
    "ListRootsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListRootsResponseTypeDef = TypedDict(
    "ListRootsResponseTypeDef",
    {
        "Roots": List["RootTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceId": str,
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
        "ResourceId": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
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

_RequiredListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef = TypedDict(
    "_RequiredListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef = TypedDict(
    "_OptionalListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef(
    _RequiredListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef,
    _OptionalListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef,
):
    pass


_RequiredListTargetsForPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredListTargetsForPolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalListTargetsForPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalListTargetsForPolicyRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTargetsForPolicyRequestRequestTypeDef(
    _RequiredListTargetsForPolicyRequestRequestTypeDef,
    _OptionalListTargetsForPolicyRequestRequestTypeDef,
):
    pass


ListTargetsForPolicyResponseTypeDef = TypedDict(
    "ListTargetsForPolicyResponseTypeDef",
    {
        "Targets": List["PolicyTargetSummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MoveAccountRequestRequestTypeDef = TypedDict(
    "MoveAccountRequestRequestTypeDef",
    {
        "AccountId": str,
        "SourceParentId": str,
        "DestinationParentId": str,
    },
)

OrganizationTypeDef = TypedDict(
    "OrganizationTypeDef",
    {
        "Id": str,
        "Arn": str,
        "FeatureSet": OrganizationFeatureSetType,
        "MasterAccountArn": str,
        "MasterAccountId": str,
        "MasterAccountEmail": str,
        "AvailablePolicyTypes": List["PolicyTypeSummaryTypeDef"],
    },
    total=False,
)

OrganizationalUnitTypeDef = TypedDict(
    "OrganizationalUnitTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
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

ParentTypeDef = TypedDict(
    "ParentTypeDef",
    {
        "Id": str,
        "Type": ParentTypeType,
    },
    total=False,
)

PolicySummaryTypeDef = TypedDict(
    "PolicySummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "Type": PolicyTypeType,
        "AwsManaged": bool,
    },
    total=False,
)

PolicyTargetSummaryTypeDef = TypedDict(
    "PolicyTargetSummaryTypeDef",
    {
        "TargetId": str,
        "Arn": str,
        "Name": str,
        "Type": TargetTypeType,
    },
    total=False,
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "PolicySummary": "PolicySummaryTypeDef",
        "Content": str,
    },
    total=False,
)

PolicyTypeSummaryTypeDef = TypedDict(
    "PolicyTypeSummaryTypeDef",
    {
        "Type": PolicyTypeType,
        "Status": PolicyTypeStatusType,
    },
    total=False,
)

RegisterDelegatedAdministratorRequestRequestTypeDef = TypedDict(
    "RegisterDelegatedAdministratorRequestRequestTypeDef",
    {
        "AccountId": str,
        "ServicePrincipal": str,
    },
)

RemoveAccountFromOrganizationRequestRequestTypeDef = TypedDict(
    "RemoveAccountFromOrganizationRequestRequestTypeDef",
    {
        "AccountId": str,
    },
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

RootTypeDef = TypedDict(
    "RootTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "PolicyTypes": List["PolicyTypeSummaryTypeDef"],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
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

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceId": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOrganizationalUnitRequestRequestTypeDef",
    {
        "OrganizationalUnitId": str,
    },
)
_OptionalUpdateOrganizationalUnitRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOrganizationalUnitRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateOrganizationalUnitRequestRequestTypeDef(
    _RequiredUpdateOrganizationalUnitRequestRequestTypeDef,
    _OptionalUpdateOrganizationalUnitRequestRequestTypeDef,
):
    pass


UpdateOrganizationalUnitResponseTypeDef = TypedDict(
    "UpdateOrganizationalUnitResponseTypeDef",
    {
        "OrganizationalUnit": "OrganizationalUnitTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdatePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePolicyRequestRequestTypeDef",
    {
        "PolicyId": str,
    },
)
_OptionalUpdatePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePolicyRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Content": str,
    },
    total=False,
)


class UpdatePolicyRequestRequestTypeDef(
    _RequiredUpdatePolicyRequestRequestTypeDef, _OptionalUpdatePolicyRequestRequestTypeDef
):
    pass


UpdatePolicyResponseTypeDef = TypedDict(
    "UpdatePolicyResponseTypeDef",
    {
        "Policy": "PolicyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
