"""
Classes representing IAM documents
"""
from pydantic import Field, validator
from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Union, Any
from enum import Enum


class Effects(Enum):
    ALLOW = "Allow"
    DENY = "Deny"


@dataclass
class Statements:
    Sid: Optional[str] = None
    Effect: Effects = Field(Effects.DENY)
    Principal: Optional[Dict[str, List[str]]] = None
    NotPrincipal: Optional[Dict[str, List[str]]] = None
    Action: Optional[Union[str, List[str]]] = None
    NotAction: Optional[Union[str, List[str]]] = None
    Resource: Optional[Union[str, List[str]]] = None
    NotResource: Optional[Union[str, List[str]]] = None
    Condition: Optional[Dict[str, Dict[str, Union[str, List[str]]]]] = None

    @validator("Principal", pre=True)
    def principal_is_list(cls, v):
        if not v:
            return v
        if isinstance(v, str):
            v = {"AWS": v}
        for key, value in v.items():
            if isinstance(value, str):
                v[key] = [value]
        return v

    @validator("NotPrincipal", pre=True)
    def notprincipal_is_list(cls, v):
        if not v:
            return v
        if isinstance(v, str):
            v = {"AWS": v}
        for key, value in v.items():
            if isinstance(value, str):
                v[key] = [value]
        return v

    @validator("NotAction", always=True)
    def at_least_action_or_not_action(cls, v, values, **kwargs):
        if not ((values.get("Action", None) is not None) ^ (v is not None)):
            raise ValueError("At least one of Action and NotAction must be specified")
        return v


@dataclass
class Document:
    Version: Optional[str] = "2008-10-17"
    Id: Optional[str] = None
    Statement: List[Statements] = Field(default_factory=list)

    @validator("Statement", pre=True)
    def make_sure_statements_is_list(cls, v):
        if not isinstance(v, list):
            return [v]
        return v


@dataclass
class Policy:
    PolicyName: str
    PolicyDocument: Document


@dataclass
class ManagedPolicy:
    PolicyName: str
    PolicyArn: str


@dataclass
class PermissionBoundary:
    PermissionsBoundaryType: str = Field(..., regex="^Policy$")
    PermissionsBoundaryArn: str = Field(...)


@dataclass
class Tag:
    Key: str
    Value: str


@dataclass
class UserDetail:
    Path: str
    UserName: str
    UserId: str
    Arn: str
    CreateDate: datetime
    UserPolicyList: List[Policy] = Field(default_factory=list)
    GroupList: List[str] = Field(default_factory=list)
    AttachedManagedPolicies: List[ManagedPolicy] = Field(default_factory=list)
    PermissionsBoundary: Optional[PermissionBoundary] = None
    Tags: List[Tag] = Field(default_factory=list)


@dataclass
class GroupDetail:
    Path: str
    GroupName: str
    GroupId: str
    Arn: str
    CreateDate: datetime
    GroupPolicyList: List[Policy]
    AttachedManagedPolicies: List[ManagedPolicy]


@dataclass
class RoleLastUse:
    LastUsedDate: Optional[datetime] = None
    Region: Optional[str] = None


@dataclass
class RoleDetail:
    Path: str
    RoleName: str
    RoleId: str
    Arn: str
    CreateDate: datetime
    AssumeRolePolicyDocument: Document
    InstanceProfileList: List[Any]  # We don't care about this yet
    RolePolicyList: List[Policy] = Field(default_factory=list)
    AttachedManagedPolicies: List[ManagedPolicy] = Field(default_factory=list)
    PermissionsBoundary: Optional[PermissionBoundary] = None
    Tags: List[Tag] = Field(default_factory=list)
    RoleLastUsed: RoleLastUse = Field(...)


@dataclass
class PolicyVersion:
    Document: Document
    VersionId: str
    IsDefaultVersion: bool
    CreateDate: datetime


@dataclass
class PolicyDetail:
    PolicyName: str
    PolicyId: str
    Arn: str
    Path: str
    DefaultVersionId: str
    AttachmentCount: int
    PermissionsBoundaryUsageCount: int
    IsAttachable: bool
    Description: str = Field("")
    CreateDate: datetime = Field(...)
    UpdateDate: datetime = Field(...)
    PolicyVersionList: List[PolicyVersion] = Field(...)


@dataclass
class AuthorizationDetails:
    UserDetailList: List[UserDetail]
    GroupDetailList: List[GroupDetail]
    RoleDetailList: List[RoleDetail]
    Policies: List[PolicyDetail]


@dataclass
class ResourcePolicy:
    Resource: str
    Policy: Document
    Account: Optional[str] = Field(None)


def extract_applicable_policies(data: AuthorizationDetails, source_arn: str) -> List[Document]:
    """
    For any given ARN, go through the GAAD, find all policies that apply to an ARN
    """
    source_type = source_arn.split(":")[5].split("/")[0]

    source: Union[RoleDetail, UserDetail]

    if source_type == "user":
        try:
            source = next(x for x in data.UserDetailList if x.Arn == source_arn)
            inline_policies = source.UserPolicyList
        except StopIteration:
            raise ValueError("Can't find Source ARN")
    elif source_type == "role":
        try:
            source = next(x for x in data.RoleDetailList if x.Arn == source_arn)
            inline_policies = source.RolePolicyList
        except StopIteration:
            raise ValueError("Can't find Source ARN")
    applicable_policies = []

    for managed_policy in source.AttachedManagedPolicies:
        policy_arn = managed_policy.PolicyArn
        try:
            policy_details = next(x for x in data.Policies if policy_arn == x.Arn)
            policy_version = next(x for x in policy_details.PolicyVersionList if x.IsDefaultVersion)
        except StopIteration:
            continue
        applicable_policies.append(policy_version.Document)

    for inline_policy in inline_policies:
        applicable_policies.append(inline_policy.PolicyDocument)

    if isinstance(source, UserDetail):
        for name in source.GroupList:
            try:
                group = next(x for x in data.GroupDetailList if x.GroupName == name)
            except StopIteration:
                continue

            for managed_policy in group.AttachedManagedPolicies:
                policy_arn = managed_policy.PolicyArn
                try:
                    policy_details = next(x for x in data.Policies if policy_arn == x.Arn)
                    policy_version = next(x for x in policy_details.PolicyVersionList if x.IsDefaultVersion)
                except StopIteration:
                    continue
                applicable_policies.append(policy_version.Document)

            for policy in group.GroupPolicyList:
                applicable_policies.append(policy.PolicyDocument)

    return applicable_policies
