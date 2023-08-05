import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_route53resolver as _aws_cdk_aws_route53resolver_ceddda9d
import constructs as _constructs_77d1e7e8


class AssociateSharedResolverRule(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.AssociateSharedResolverRule",
):
    '''(experimental) Associate a resolver rule that has been shared to this account.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_names: typing.Sequence[builtins.str],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain_names: (experimental) domainNames which are to be associated.
        :param vpc: (experimental) The VPC which will be assocaited with the ResolverRules.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae22f953478fe352acc7bc74c6ade1acf4f04bb9cd525fe93b2ec5451fae8a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssociateSharedResolverRuleProps(domain_names=domain_names, vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.dns.AssociateSharedResolverRuleProps",
    jsii_struct_bases=[],
    name_mapping={"domain_names": "domainNames", "vpc": "vpc"},
)
class AssociateSharedResolverRuleProps:
    def __init__(
        self,
        *,
        domain_names: typing.Sequence[builtins.str],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    ) -> None:
        '''
        :param domain_names: (experimental) domainNames which are to be associated.
        :param vpc: (experimental) The VPC which will be assocaited with the ResolverRules.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65a67c65afa6cf00ad5c87e050a21b38872e7ca1786a6e74416ee909d7bc0cc)
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_names": domain_names,
            "vpc": vpc,
        }

    @builtins.property
    def domain_names(self) -> typing.List[builtins.str]:
        '''(experimental) domainNames which are to be associated.

        :stability: experimental
        '''
        result = self._values.get("domain_names")
        assert result is not None, "Required property 'domain_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''(experimental) The VPC which will be assocaited with the ResolverRules.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssociateSharedResolverRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsManagedDNSFirewallRuleGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.AwsManagedDNSFirewallRuleGroup",
):
    '''
    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472e0270947c7ad3005640dd4cae38efa59fc59c96809ec55b6ded6e1a9016e2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="resolverRuleId")
    def resolver_rule_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "resolverRuleId"))

    @resolver_rule_id.setter
    def resolver_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d23a22d280213989c6113d9bb6c03a87dc39bf5d4df434bd159fb67b0a9869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverRuleId", value)


class CentralAccountAssnRole(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.CentralAccountAssnRole",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        org_id: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param org_id: 
        :param vpc: 
        :param role_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c7359c8886b335a2341370c4d3930bcdd2ee857d5d6d5cf52981616842950e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CentralAccountAssnRoleProps(
            org_id=org_id, vpc=vpc, role_name=role_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assnRole")
    def assn_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "assnRole"))


@jsii.data_type(
    jsii_type="raindancers-network.dns.CentralAccountAssnRoleProps",
    jsii_struct_bases=[],
    name_mapping={"org_id": "orgId", "vpc": "vpc", "role_name": "roleName"},
)
class CentralAccountAssnRoleProps:
    def __init__(
        self,
        *,
        org_id: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param org_id: 
        :param vpc: 
        :param role_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d531557c3beeb761e272f75b243ab115ec57092a105e590695247615c8e7f8)
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "org_id": org_id,
            "vpc": vpc,
        }
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def org_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CentralAccountAssnRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CentralResolverRules(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.CentralResolverRules",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domains: typing.Sequence[builtins.str],
        resolvers: "R53Resolverendpoints",
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        vpc_search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domains: 
        :param resolvers: 
        :param vpc: 
        :param vpc_search_tag: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7b0b51a00acf5ecddaae109bf17a729da42372bea37e05c30a0c26e384565e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CentralResolverRulesProps(
            domains=domains,
            resolvers=resolvers,
            vpc=vpc,
            vpc_search_tag=vpc_search_tag,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.dns.CentralResolverRulesProps",
    jsii_struct_bases=[],
    name_mapping={
        "domains": "domains",
        "resolvers": "resolvers",
        "vpc": "vpc",
        "vpc_search_tag": "vpcSearchTag",
    },
)
class CentralResolverRulesProps:
    def __init__(
        self,
        *,
        domains: typing.Sequence[builtins.str],
        resolvers: "R53Resolverendpoints",
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        vpc_search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param domains: 
        :param resolvers: 
        :param vpc: 
        :param vpc_search_tag: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11da622b6d6b59ec833c49fbc9e12cdef3e4970524dc537a6fb061717a60195)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument resolvers", value=resolvers, expected_type=type_hints["resolvers"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_search_tag", value=vpc_search_tag, expected_type=type_hints["vpc_search_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
            "resolvers": resolvers,
            "vpc": vpc,
        }
        if vpc_search_tag is not None:
            self._values["vpc_search_tag"] = vpc_search_tag

    @builtins.property
    def domains(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resolvers(self) -> "R53Resolverendpoints":
        '''
        :stability: experimental
        '''
        result = self._values.get("resolvers")
        assert result is not None, "Required property 'resolvers' is missing"
        return typing.cast("R53Resolverendpoints", result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    @builtins.property
    def vpc_search_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc_search_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CentralResolverRulesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConditionalForwarder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.ConditionalForwarder",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        forwarding_rules: typing.Sequence[typing.Union["OutboundForwardingRule", typing.Dict[builtins.str, typing.Any]]],
        inbound_resolver_targets: typing.Sequence[typing.Union[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]],
        outbound_resolver: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param forwarding_rules: 
        :param inbound_resolver_targets: 
        :param outbound_resolver: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fae23ba4a4b07a1d40b3e23f3e950dbd8e6eb6cd5af09b108bd94044ad75464)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConditionalForwarderProps(
            forwarding_rules=forwarding_rules,
            inbound_resolver_targets=inbound_resolver_targets,
            outbound_resolver=outbound_resolver,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.dns.ConditionalForwarderProps",
    jsii_struct_bases=[],
    name_mapping={
        "forwarding_rules": "forwardingRules",
        "inbound_resolver_targets": "inboundResolverTargets",
        "outbound_resolver": "outboundResolver",
        "vpc": "vpc",
    },
)
class ConditionalForwarderProps:
    def __init__(
        self,
        *,
        forwarding_rules: typing.Sequence[typing.Union["OutboundForwardingRule", typing.Dict[builtins.str, typing.Any]]],
        inbound_resolver_targets: typing.Sequence[typing.Union[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]],
        outbound_resolver: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    ) -> None:
        '''
        :param forwarding_rules: 
        :param inbound_resolver_targets: 
        :param outbound_resolver: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3b13529a40fc3c33ea7de31ce81e5d3b3862543d9f46ceb6eb17b9396749e9)
            check_type(argname="argument forwarding_rules", value=forwarding_rules, expected_type=type_hints["forwarding_rules"])
            check_type(argname="argument inbound_resolver_targets", value=inbound_resolver_targets, expected_type=type_hints["inbound_resolver_targets"])
            check_type(argname="argument outbound_resolver", value=outbound_resolver, expected_type=type_hints["outbound_resolver"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "forwarding_rules": forwarding_rules,
            "inbound_resolver_targets": inbound_resolver_targets,
            "outbound_resolver": outbound_resolver,
            "vpc": vpc,
        }

    @builtins.property
    def forwarding_rules(self) -> typing.List["OutboundForwardingRule"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("forwarding_rules")
        assert result is not None, "Required property 'forwarding_rules' is missing"
        return typing.cast(typing.List["OutboundForwardingRule"], result)

    @builtins.property
    def inbound_resolver_targets(
        self,
    ) -> typing.List[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty]:
        '''
        :stability: experimental
        '''
        result = self._values.get("inbound_resolver_targets")
        assert result is not None, "Required property 'inbound_resolver_targets' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty], result)

    @builtins.property
    def outbound_resolver(
        self,
    ) -> _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint:
        '''
        :stability: experimental
        '''
        result = self._values.get("outbound_resolver")
        assert result is not None, "Required property 'outbound_resolver' is missing"
        return typing.cast(_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint, result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionalForwarderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.dns.CrossAccountProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "role_name": "roleName"},
)
class CrossAccountProps:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: 
        :param role_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff2136c0cb8d365b1efbae33ec78764fdfbd672c581c5e916e16cf15c2773cf)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.dns.DNSFirewallActions")
class DNSFirewallActions(enum.Enum):
    '''
    :stability: experimental
    '''

    ALLOW = "ALLOW"
    '''
    :stability: experimental
    '''
    BLOCK = "BLOCK"
    '''
    :stability: experimental
    '''
    ALERT = "ALERT"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.dns.DNSFirewallBlockResponse")
class DNSFirewallBlockResponse(enum.Enum):
    '''
    :stability: experimental
    '''

    NODATA = "NODATA"
    '''
    :stability: experimental
    '''
    NXDOMAIN = "NXDOMAIN"
    '''
    :stability: experimental
    '''
    OVERRIDE = "OVERRIDE"
    '''
    :stability: experimental
    '''


class EnterpriseZone(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.EnterpriseZone",
):
    '''(experimental) create forwarding rules and associate them with a vpc.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        enterprise_domain_name: builtins.str,
        local_vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        hub_vpcs: typing.Optional[typing.Sequence[typing.Union["HubVpc", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param enterprise_domain_name: 
        :param local_vpc: 
        :param hub_vpcs: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb636b3365093240e50f802199d242686750c89c470f1d008986b28390ea43f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnterpriseZoneProps(
            enterprise_domain_name=enterprise_domain_name,
            local_vpc=local_vpc,
            hub_vpcs=hub_vpcs,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="privateZone")
    def private_zone(self) -> _aws_cdk_aws_route53_ceddda9d.PrivateHostedZone:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.PrivateHostedZone, jsii.get(self, "privateZone"))


@jsii.data_type(
    jsii_type="raindancers-network.dns.EnterpriseZoneProps",
    jsii_struct_bases=[],
    name_mapping={
        "enterprise_domain_name": "enterpriseDomainName",
        "local_vpc": "localVpc",
        "hub_vpcs": "hubVpcs",
    },
)
class EnterpriseZoneProps:
    def __init__(
        self,
        *,
        enterprise_domain_name: builtins.str,
        local_vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        hub_vpcs: typing.Optional[typing.Sequence[typing.Union["HubVpc", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param enterprise_domain_name: 
        :param local_vpc: 
        :param hub_vpcs: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72dfb9cae457c91cb2ad0a5fc191ff43c6c5ea10c232bd22e3ced929db124a34)
            check_type(argname="argument enterprise_domain_name", value=enterprise_domain_name, expected_type=type_hints["enterprise_domain_name"])
            check_type(argname="argument local_vpc", value=local_vpc, expected_type=type_hints["local_vpc"])
            check_type(argname="argument hub_vpcs", value=hub_vpcs, expected_type=type_hints["hub_vpcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enterprise_domain_name": enterprise_domain_name,
            "local_vpc": local_vpc,
        }
        if hub_vpcs is not None:
            self._values["hub_vpcs"] = hub_vpcs

    @builtins.property
    def enterprise_domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("enterprise_domain_name")
        assert result is not None, "Required property 'enterprise_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("local_vpc")
        assert result is not None, "Required property 'local_vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    @builtins.property
    def hub_vpcs(self) -> typing.Optional[typing.List["HubVpc"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("hub_vpcs")
        return typing.cast(typing.Optional[typing.List["HubVpc"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ForwardingRules(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.ForwardingRules",
):
    '''(experimental) create forwarding rules and associate them with a vpc.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domains: typing.Sequence[builtins.str],
        resolver_id: builtins.str,
        resolver_ip: typing.Sequence[builtins.str],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domains: 
        :param resolver_id: 
        :param resolver_ip: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed43dbc1fa5faab7ada03729073cb1dafec7c30dabd2711a2214e2fcdab3e28)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ForwardingRulesProps(
            domains=domains, resolver_id=resolver_id, resolver_ip=resolver_ip, vpc=vpc
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.dns.ForwardingRulesProps",
    jsii_struct_bases=[],
    name_mapping={
        "domains": "domains",
        "resolver_id": "resolverId",
        "resolver_ip": "resolverIP",
        "vpc": "vpc",
    },
)
class ForwardingRulesProps:
    def __init__(
        self,
        *,
        domains: typing.Sequence[builtins.str],
        resolver_id: builtins.str,
        resolver_ip: typing.Sequence[builtins.str],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''
        :param domains: 
        :param resolver_id: 
        :param resolver_ip: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3820cbaaffcb8010443ea6d98c6454717b12175b8fb51cf4c16107e5a427bae8)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument resolver_id", value=resolver_id, expected_type=type_hints["resolver_id"])
            check_type(argname="argument resolver_ip", value=resolver_ip, expected_type=type_hints["resolver_ip"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
            "resolver_id": resolver_id,
            "resolver_ip": resolver_ip,
            "vpc": vpc,
        }

    @builtins.property
    def domains(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resolver_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("resolver_id")
        assert result is not None, "Required property 'resolver_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resolver_ip(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("resolver_ip")
        assert result is not None, "Required property 'resolver_ip' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForwardingRulesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.dns.HubVpc",
    jsii_struct_bases=[],
    name_mapping={
        "region": "region",
        "cross_account": "crossAccount",
        "vpc_search_tag": "vpcSearchTag",
    },
)
class HubVpc:
    def __init__(
        self,
        *,
        region: builtins.str,
        cross_account: typing.Optional[typing.Union[CrossAccountProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param region: (experimental) what region is the central account in.
        :param cross_account: 
        :param vpc_search_tag: 

        :stability: experimental
        '''
        if isinstance(cross_account, dict):
            cross_account = CrossAccountProps(**cross_account)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26cdea8a804edcc34c7571838842b8efa8806d31b1683ae3c92d34366350637)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cross_account", value=cross_account, expected_type=type_hints["cross_account"])
            check_type(argname="argument vpc_search_tag", value=vpc_search_tag, expected_type=type_hints["vpc_search_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
        }
        if cross_account is not None:
            self._values["cross_account"] = cross_account
        if vpc_search_tag is not None:
            self._values["vpc_search_tag"] = vpc_search_tag

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) what region is the central account in.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cross_account(self) -> typing.Optional[CrossAccountProps]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cross_account")
        return typing.cast(typing.Optional[CrossAccountProps], result)

    @builtins.property
    def vpc_search_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc_search_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HubVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.dns.OutboundForwardingRule",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "forward_to": "forwardTo"},
)
class OutboundForwardingRule:
    def __init__(
        self,
        *,
        domain: builtins.str,
        forward_to: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param domain: (experimental) domain to forward.
        :param forward_to: (experimental) array of ip address's to forward request to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0e5bb778c21503eb370039f503539f108f5e94940112ec8c1203a3f863ce79)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument forward_to", value=forward_to, expected_type=type_hints["forward_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "forward_to": forward_to,
        }

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) domain to forward.

        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forward_to(self) -> typing.List[builtins.str]:
        '''(experimental) array of ip address's to forward request to.

        :stability: experimental
        '''
        result = self._values.get("forward_to")
        assert result is not None, "Required property 'forward_to' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OutboundForwardingRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class R53Resolverendpoints(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.dns.R53Resolverendpoints",
):
    '''(experimental) Create Route53 Resolver Endpoints for MultiVPC and Hybrid DNS Resolution.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnet_group: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        outbound_forwarding_rules: typing.Optional[typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: the scope in which these resources are craeted.
        :param id: the id of the construct.
        :param subnet_group: (experimental) the subnetgroup to place the resolvers in.
        :param vpc: (experimental) the vpc that the resolvers will be placed in.
        :param outbound_forwarding_rules: (experimental) An array of Internal domains that can be centrally resolved in this VPC.
        :param tag_value: (experimental) Value for Sharing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d93defdd773436c75f8734c5e4f5e6237c8216ecbb03afeca8d24ff30ca311)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = R53ResolverendpointsProps(
            subnet_group=subnet_group,
            vpc=vpc,
            outbound_forwarding_rules=outbound_forwarding_rules,
            tag_value=tag_value,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="inboundResolver")
    def inbound_resolver(
        self,
    ) -> _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint:
        '''(experimental) inbound resolver.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint, jsii.get(self, "inboundResolver"))

    @inbound_resolver.setter
    def inbound_resolver(
        self,
        value: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a3e12456ebef4eaef1a2042a2e159ae6012d20e8265cdc07cde3c748925e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundResolver", value)

    @builtins.property
    @jsii.member(jsii_name="inboundResolversIp")
    def inbound_resolvers_ip(
        self,
    ) -> typing.List[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty]:
        '''(experimental) list of Resolver IP address's.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty], jsii.get(self, "inboundResolversIp"))

    @inbound_resolvers_ip.setter
    def inbound_resolvers_ip(
        self,
        value: typing.List[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d8f1abefe0f398b3cb41a9110a758f89101e88beeec81cbb5f69ac538e2c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundResolversIp", value)

    @builtins.property
    @jsii.member(jsii_name="outboundResolver")
    def outbound_resolver(
        self,
    ) -> _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint:
        '''(experimental) outbound resolver.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint, jsii.get(self, "outboundResolver"))

    @outbound_resolver.setter
    def outbound_resolver(
        self,
        value: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6234022c9b3745fee6897fc01873c9dbeb1e705b38dc76bed2e77d970139693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundResolver", value)


@jsii.data_type(
    jsii_type="raindancers-network.dns.R53ResolverendpointsProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_group": "subnetGroup",
        "vpc": "vpc",
        "outbound_forwarding_rules": "outboundForwardingRules",
        "tag_value": "tagValue",
    },
)
class R53ResolverendpointsProps:
    def __init__(
        self,
        *,
        subnet_group: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        outbound_forwarding_rules: typing.Optional[typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to for creating inbound resolvers.

        :param subnet_group: (experimental) the subnetgroup to place the resolvers in.
        :param vpc: (experimental) the vpc that the resolvers will be placed in.
        :param outbound_forwarding_rules: (experimental) An array of Internal domains that can be centrally resolved in this VPC.
        :param tag_value: (experimental) Value for Sharing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736fb2da257978c7a626639f2a3a60faf11d0e2bcad222bbb62cfa943a6236f5)
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument outbound_forwarding_rules", value=outbound_forwarding_rules, expected_type=type_hints["outbound_forwarding_rules"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_group": subnet_group,
            "vpc": vpc,
        }
        if outbound_forwarding_rules is not None:
            self._values["outbound_forwarding_rules"] = outbound_forwarding_rules
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def subnet_group(self) -> builtins.str:
        '''(experimental) the subnetgroup to place the resolvers in.

        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''(experimental) the vpc that the resolvers will be placed in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    @builtins.property
    def outbound_forwarding_rules(
        self,
    ) -> typing.Optional[typing.List[OutboundForwardingRule]]:
        '''(experimental) An array of Internal domains that can be centrally resolved in this VPC.

        :stability: experimental
        '''
        result = self._values.get("outbound_forwarding_rules")
        return typing.cast(typing.Optional[typing.List[OutboundForwardingRule]], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) Value for Sharing.

        :stability: experimental
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "R53ResolverendpointsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.dns.ResolverDirection")
class ResolverDirection(enum.Enum):
    '''(experimental) Direction of Resolver.

    :stability: experimental
    '''

    INBOUND = "INBOUND"
    '''(experimental) Resolver is Inbound.

    :stability: experimental
    '''
    OUTBOUND = "OUTBOUND"
    '''(experimental) Resolver is outbound.

    :stability: experimental
    '''


__all__ = [
    "AssociateSharedResolverRule",
    "AssociateSharedResolverRuleProps",
    "AwsManagedDNSFirewallRuleGroup",
    "CentralAccountAssnRole",
    "CentralAccountAssnRoleProps",
    "CentralResolverRules",
    "CentralResolverRulesProps",
    "ConditionalForwarder",
    "ConditionalForwarderProps",
    "CrossAccountProps",
    "DNSFirewallActions",
    "DNSFirewallBlockResponse",
    "EnterpriseZone",
    "EnterpriseZoneProps",
    "ForwardingRules",
    "ForwardingRulesProps",
    "HubVpc",
    "OutboundForwardingRule",
    "R53Resolverendpoints",
    "R53ResolverendpointsProps",
    "ResolverDirection",
]

publication.publish()

def _typecheckingstub__3ae22f953478fe352acc7bc74c6ade1acf4f04bb9cd525fe93b2ec5451fae8a2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_names: typing.Sequence[builtins.str],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65a67c65afa6cf00ad5c87e050a21b38872e7ca1786a6e74416ee909d7bc0cc(
    *,
    domain_names: typing.Sequence[builtins.str],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472e0270947c7ad3005640dd4cae38efa59fc59c96809ec55b6ded6e1a9016e2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d23a22d280213989c6113d9bb6c03a87dc39bf5d4df434bd159fb67b0a9869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c7359c8886b335a2341370c4d3930bcdd2ee857d5d6d5cf52981616842950e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    org_id: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d531557c3beeb761e272f75b243ab115ec57092a105e590695247615c8e7f8(
    *,
    org_id: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7b0b51a00acf5ecddaae109bf17a729da42372bea37e05c30a0c26e384565e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: typing.Sequence[builtins.str],
    resolvers: R53Resolverendpoints,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    vpc_search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11da622b6d6b59ec833c49fbc9e12cdef3e4970524dc537a6fb061717a60195(
    *,
    domains: typing.Sequence[builtins.str],
    resolvers: R53Resolverendpoints,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    vpc_search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fae23ba4a4b07a1d40b3e23f3e950dbd8e6eb6cd5af09b108bd94044ad75464(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    forwarding_rules: typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[builtins.str, typing.Any]]],
    inbound_resolver_targets: typing.Sequence[typing.Union[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]],
    outbound_resolver: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3b13529a40fc3c33ea7de31ce81e5d3b3862543d9f46ceb6eb17b9396749e9(
    *,
    forwarding_rules: typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[builtins.str, typing.Any]]],
    inbound_resolver_targets: typing.Sequence[typing.Union[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]],
    outbound_resolver: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff2136c0cb8d365b1efbae33ec78764fdfbd672c581c5e916e16cf15c2773cf(
    *,
    account_id: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb636b3365093240e50f802199d242686750c89c470f1d008986b28390ea43f4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    enterprise_domain_name: builtins.str,
    local_vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    hub_vpcs: typing.Optional[typing.Sequence[typing.Union[HubVpc, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dfb9cae457c91cb2ad0a5fc191ff43c6c5ea10c232bd22e3ced929db124a34(
    *,
    enterprise_domain_name: builtins.str,
    local_vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    hub_vpcs: typing.Optional[typing.Sequence[typing.Union[HubVpc, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed43dbc1fa5faab7ada03729073cb1dafec7c30dabd2711a2214e2fcdab3e28(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: typing.Sequence[builtins.str],
    resolver_id: builtins.str,
    resolver_ip: typing.Sequence[builtins.str],
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3820cbaaffcb8010443ea6d98c6454717b12175b8fb51cf4c16107e5a427bae8(
    *,
    domains: typing.Sequence[builtins.str],
    resolver_id: builtins.str,
    resolver_ip: typing.Sequence[builtins.str],
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26cdea8a804edcc34c7571838842b8efa8806d31b1683ae3c92d34366350637(
    *,
    region: builtins.str,
    cross_account: typing.Optional[typing.Union[CrossAccountProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0e5bb778c21503eb370039f503539f108f5e94940112ec8c1203a3f863ce79(
    *,
    domain: builtins.str,
    forward_to: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d93defdd773436c75f8734c5e4f5e6237c8216ecbb03afeca8d24ff30ca311(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnet_group: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    outbound_forwarding_rules: typing.Optional[typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a3e12456ebef4eaef1a2042a2e159ae6012d20e8265cdc07cde3c748925e13(
    value: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d8f1abefe0f398b3cb41a9110a758f89101e88beeec81cbb5f69ac538e2c98(
    value: typing.List[_aws_cdk_aws_route53resolver_ceddda9d.CfnResolverRule.TargetAddressProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6234022c9b3745fee6897fc01873c9dbeb1e705b38dc76bed2e77d970139693(
    value: _aws_cdk_aws_route53resolver_ceddda9d.CfnResolverEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736fb2da257978c7a626639f2a3a60faf11d0e2bcad222bbb62cfa943a6236f5(
    *,
    subnet_group: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    outbound_forwarding_rules: typing.Optional[typing.Sequence[typing.Union[OutboundForwardingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
