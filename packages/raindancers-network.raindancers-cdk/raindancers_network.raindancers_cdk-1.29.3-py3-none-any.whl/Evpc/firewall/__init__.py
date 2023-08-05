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
import aws_cdk.aws_networkfirewall as _aws_cdk_aws_networkfirewall_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="raindancers-network.firewall.AddStatefulRulesProps",
    jsii_struct_bases=[],
    name_mapping={"aws_managed_rules": "awsManagedRules"},
)
class AddStatefulRulesProps:
    def __init__(
        self,
        *,
        aws_managed_rules: typing.Sequence["ManagedAwsFirewallRules"],
    ) -> None:
        '''
        :param aws_managed_rules: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ea0f84387576ba16d0553ab554d28a4b08cf9efafe62e537439313e9710883)
            check_type(argname="argument aws_managed_rules", value=aws_managed_rules, expected_type=type_hints["aws_managed_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_managed_rules": aws_managed_rules,
        }

    @builtins.property
    def aws_managed_rules(self) -> typing.List["ManagedAwsFirewallRules"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("aws_managed_rules")
        assert result is not None, "Required property 'aws_managed_rules' is missing"
        return typing.cast(typing.List["ManagedAwsFirewallRules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStatefulRulesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.firewall.AddStatelessRulesProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "group_name": "groupName",
        "rules": "rules",
    },
)
class AddStatelessRulesProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        group_name: builtins.str,
        rules: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param description: 
        :param group_name: 
        :param rules: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f899e7bd165175985b55bf129db6e5477559ec80a27ed2998334a0c8edb6b715)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "group_name": group_name,
            "rules": rules,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty]:
        '''
        :stability: experimental
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStatelessRulesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicy(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.firewall.FirewallPolicy",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        policy_name: builtins.str,
        stateless_default_actions: typing.Sequence["StatelessActions"],
        stateless_fragment_default_actions: typing.Sequence["StatelessActions"],
        stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param policy_name: 
        :param stateless_default_actions: 
        :param stateless_fragment_default_actions: 
        :param stateful_engine_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35735e2d85fa6c6e7e8795dd04383d88e08c2bf98872ddbaa7926067217104f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallPolicyProps(
            policy_name=policy_name,
            stateless_default_actions=stateless_default_actions,
            stateless_fragment_default_actions=stateless_fragment_default_actions,
            stateful_engine_options=stateful_engine_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addManagedStatefulRules")
    def add_managed_stateful_rules(
        self,
        *,
        aws_managed_rules: typing.Sequence["ManagedAwsFirewallRules"],
    ) -> None:
        '''
        :param aws_managed_rules: 

        :stability: experimental
        '''
        props = AddStatefulRulesProps(aws_managed_rules=aws_managed_rules)

        return typing.cast(None, jsii.invoke(self, "addManagedStatefulRules", [props]))

    @jsii.member(jsii_name="addStatelessRuleGroup")
    def add_stateless_rule_group(
        self,
        *,
        description: builtins.str,
        group_name: builtins.str,
        rules: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param description: 
        :param group_name: 
        :param rules: 

        :stability: experimental
        '''
        props = AddStatelessRulesProps(
            description=description, group_name=group_name, rules=rules
        )

        return typing.cast(None, jsii.invoke(self, "addStatelessRuleGroup", [props]))

    @builtins.property
    @jsii.member(jsii_name="firewallpolicy")
    def firewallpolicy(self) -> _aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy, jsii.get(self, "firewallpolicy"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> "IFirewallPolicyProperty":
        '''
        :stability: experimental
        '''
        return typing.cast("IFirewallPolicyProperty", jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: "IFirewallPolicyProperty") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d06b2cb9ea14c763b913431cc679731cd7e6b31511f3ef54ae6fd9e9447adea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)


@jsii.data_type(
    jsii_type="raindancers-network.firewall.FirewallPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_name": "policyName",
        "stateless_default_actions": "statelessDefaultActions",
        "stateless_fragment_default_actions": "statelessFragmentDefaultActions",
        "stateful_engine_options": "statefulEngineOptions",
    },
)
class FirewallPolicyProps:
    def __init__(
        self,
        *,
        policy_name: builtins.str,
        stateless_default_actions: typing.Sequence["StatelessActions"],
        stateless_fragment_default_actions: typing.Sequence["StatelessActions"],
        stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param policy_name: 
        :param stateless_default_actions: 
        :param stateless_fragment_default_actions: 
        :param stateful_engine_options: 

        :stability: experimental
        '''
        if isinstance(stateful_engine_options, dict):
            stateful_engine_options = _aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty(**stateful_engine_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc18aca8b81d2ce71217f5d1e7d403ed7083146f12b3fa95c6faed06c5498069)
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument stateless_default_actions", value=stateless_default_actions, expected_type=type_hints["stateless_default_actions"])
            check_type(argname="argument stateless_fragment_default_actions", value=stateless_fragment_default_actions, expected_type=type_hints["stateless_fragment_default_actions"])
            check_type(argname="argument stateful_engine_options", value=stateful_engine_options, expected_type=type_hints["stateful_engine_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_name": policy_name,
            "stateless_default_actions": stateless_default_actions,
            "stateless_fragment_default_actions": stateless_fragment_default_actions,
        }
        if stateful_engine_options is not None:
            self._values["stateful_engine_options"] = stateful_engine_options

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stateless_default_actions(self) -> typing.List["StatelessActions"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stateless_default_actions")
        assert result is not None, "Required property 'stateless_default_actions' is missing"
        return typing.cast(typing.List["StatelessActions"], result)

    @builtins.property
    def stateless_fragment_default_actions(self) -> typing.List["StatelessActions"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stateless_fragment_default_actions")
        assert result is not None, "Required property 'stateless_fragment_default_actions' is missing"
        return typing.cast(typing.List["StatelessActions"], result)

    @builtins.property
    def stateful_engine_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stateful_engine_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="raindancers-network.firewall.IFirewallPolicyProperty")
class IFirewallPolicyProperty(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="statelessDefaultActions")
    def stateless_default_actions(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @stateless_default_actions.setter
    def stateless_default_actions(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statelessFragmentDefaultActions")
    def stateless_fragment_default_actions(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @stateless_fragment_default_actions.setter
    def stateless_fragment_default_actions(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statefulDefaultActions")
    def stateful_default_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        ...

    @stateful_default_actions.setter
    def stateful_default_actions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statefulEngineOptions")
    def stateful_engine_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :stability: experimental
        '''
        ...

    @stateful_engine_options.setter
    def stateful_engine_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, _aws_cdk_ceddda9d.IResolvable]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statefulRuleGroupReferences")
    def stateful_rule_group_references(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty]]:
        '''
        :stability: experimental
        '''
        ...

    @stateful_rule_group_references.setter
    def stateful_rule_group_references(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statelessCustomActions")
    def stateless_custom_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, _aws_cdk_ceddda9d.IResolvable]]]]:
        '''
        :stability: experimental
        '''
        ...

    @stateless_custom_actions.setter
    def stateless_custom_actions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, _aws_cdk_ceddda9d.IResolvable]]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="statelessRuleGroupReferences")
    def stateless_rule_group_references(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]]:
        '''
        :stability: experimental
        '''
        ...

    @stateless_rule_group_references.setter
    def stateless_rule_group_references(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]],
    ) -> None:
        ...


class _IFirewallPolicyPropertyProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "raindancers-network.firewall.IFirewallPolicyProperty"

    @builtins.property
    @jsii.member(jsii_name="statelessDefaultActions")
    def stateless_default_actions(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statelessDefaultActions"))

    @stateless_default_actions.setter
    def stateless_default_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edf1f1a0d5f20fb3add4c5b51fb5dd58fed184ac979140e6501bcfe9c50ac84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statelessDefaultActions", value)

    @builtins.property
    @jsii.member(jsii_name="statelessFragmentDefaultActions")
    def stateless_fragment_default_actions(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statelessFragmentDefaultActions"))

    @stateless_fragment_default_actions.setter
    def stateless_fragment_default_actions(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2397ea190084c1fcfce1802975b994221c5c66044b86bc6d882325de8f5aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statelessFragmentDefaultActions", value)

    @builtins.property
    @jsii.member(jsii_name="statefulDefaultActions")
    def stateful_default_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "statefulDefaultActions"))

    @stateful_default_actions.setter
    def stateful_default_actions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09af2ad5eab00e627e1d9bfcbaec7ad4d9ac4ac3658703612b4781c7caf0fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statefulDefaultActions", value)

    @builtins.property
    @jsii.member(jsii_name="statefulEngineOptions")
    def stateful_engine_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, _aws_cdk_ceddda9d.IResolvable]], jsii.get(self, "statefulEngineOptions"))

    @stateful_engine_options.setter
    def stateful_engine_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, _aws_cdk_ceddda9d.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456484d36eaade38b50bf69aba75f3adb0044432098b974da8024451d901360f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statefulEngineOptions", value)

    @builtins.property
    @jsii.member(jsii_name="statefulRuleGroupReferences")
    def stateful_rule_group_references(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty]], jsii.get(self, "statefulRuleGroupReferences"))

    @stateful_rule_group_references.setter
    def stateful_rule_group_references(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df9f94a207c804d36ebb388b7df4c75d51d98324a37d8373593db51b80156cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statefulRuleGroupReferences", value)

    @builtins.property
    @jsii.member(jsii_name="statelessCustomActions")
    def stateless_custom_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, _aws_cdk_ceddda9d.IResolvable]]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, _aws_cdk_ceddda9d.IResolvable]]]], jsii.get(self, "statelessCustomActions"))

    @stateless_custom_actions.setter
    def stateless_custom_actions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, _aws_cdk_ceddda9d.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6929aba6a0340caf441e1d0c6b18e2fa3a69cf6f4cc127eccf22c9d260d339b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statelessCustomActions", value)

    @builtins.property
    @jsii.member(jsii_name="statelessRuleGroupReferences")
    def stateless_rule_group_references(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]], jsii.get(self, "statelessRuleGroupReferences"))

    @stateless_rule_group_references.setter
    def stateless_rule_group_references(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628a61cfeb75ba1bc2f7ce5a321b07644869230e96969053d378d14dda59e807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statelessRuleGroupReferences", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewallPolicyProperty).__jsii_proxy_class__ = lambda : _IFirewallPolicyPropertyProxy


@jsii.enum(jsii_type="raindancers-network.firewall.ManagedAwsFirewallRules")
class ManagedAwsFirewallRules(enum.Enum):
    '''
    :stability: experimental
    '''

    ABUSED_LEGIT_MALWARE_DOMAINS_ACTION_ORDER = "ABUSED_LEGIT_MALWARE_DOMAINS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    ABUSED_LEGIT_BOTNET_COMMAND_AND_CONTROL_DOMAINS_ACTION_ORDER = "ABUSED_LEGIT_BOTNET_COMMAND_AND_CONTROL_DOMAINS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    MALWARE_DOMAINS_ACTION_ORDER = "MALWARE_DOMAINS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    BOTNET_COMMAND_AND_CONTROL_DOMAINS_ACTION_ORDER = "BOTNET_COMMAND_AND_CONTROL_DOMAINS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_BOTNET_ACTION_ORDER = "THREAT_SIGNATURES_BOTNET_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_BOTNET_WEB_ACTION_ORDER = "THREAT_SIGNATURES_BOTNET_WEB_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_BOTNET_WINDOWS_ACTION_ODER = "THREAT_SIGNATURES_BOTNET_WINDOWS_ACTION_ODER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_DOS_ACTION_ORDER = "THREAT_SIGNATURES_DOS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_EMERGING_EVENTS_ACTION_ORDER = "THREAT_SIGNATURES_EMERGING_EVENTS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_EXPLOITS_ACTION_ORDER = "THREAT_SIGNATURES_EXPLOITS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_FUP_ACTION_ORDER = "THREAT_SIGNATURES_FUP_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_IOC_ACTION_ORDER = "THREAT_SIGNATURES_IOC_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_MALWARE_ACTION_ORDER = "THREAT_SIGNATURES_MALWARE_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_MALWARE_COIN_MINING_ACTION_ORDER = "THREAT_SIGNATURES_MALWARE_COIN_MINING_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_MAWLARE_WEB_ACTION_ORDER = "THREAT_SIGNATURES_MAWLARE_WEB_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_MALWARE_MOBILE_ACTION_ORDER = "THREAT_SIGNATURES_MALWARE_MOBILE_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_PHISHING_ACTION_ORDER = "THREAT_SIGNATURES_PHISHING_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_SCANNERS_ACTION_ORDER = "THREAT_SIGNATURES_SCANNERS_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_SUSPECT_ACTION_ORDER = "THREAT_SIGNATURES_SUSPECT_ACTION_ORDER"
    '''
    :stability: experimental
    '''
    THREAT_SIGNATURES_WEB_ATTACKS_ACTION_ORDER = "THREAT_SIGNATURES_WEB_ATTACKS_ACTION_ORDER"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.firewall.Protocol")
class Protocol(enum.Enum):
    '''
    :stability: experimental
    '''

    ICMP = "ICMP"
    '''
    :stability: experimental
    '''
    TCP = "TCP"
    '''
    :stability: experimental
    '''
    UDP = "UDP"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.firewall.RuleGroupType")
class RuleGroupType(enum.Enum):
    '''
    :stability: experimental
    '''

    STATEFUL = "STATEFUL"
    '''
    :stability: experimental
    '''
    STATELESS = "STATELESS"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.firewall.StatefulDefaultActions")
class StatefulDefaultActions(enum.Enum):
    '''
    :stability: experimental
    '''

    DROP_STRICT = "DROP_STRICT"
    '''
    :stability: experimental
    '''
    DROP_ESTABLISHED = "DROP_ESTABLISHED"
    '''
    :stability: experimental
    '''
    ALERT_STRICT = "ALERT_STRICT"
    '''
    :stability: experimental
    '''
    ALERT_ESTABLISHED = "ALERT_ESTABLISHED"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.firewall.StatelessActions")
class StatelessActions(enum.Enum):
    '''
    :stability: experimental
    '''

    PASS = "PASS"
    '''
    :stability: experimental
    '''
    DROP = "DROP"
    '''
    :stability: experimental
    '''
    STATEFUL = "STATEFUL"
    '''
    :stability: experimental
    '''


class StatelessRule(
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.firewall.StatelessRule",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        actions: typing.Sequence[StatelessActions],
        priority: jsii.Number,
        destination_ports: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
        destinations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        protocols: typing.Optional[typing.Sequence[Protocol]] = None,
        source_ports: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
        sources: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tcp_flags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param actions: 
        :param priority: 
        :param destination_ports: 
        :param destinations: 
        :param protocols: 
        :param source_ports: 
        :param sources: 
        :param tcp_flags: 

        :stability: experimental
        '''
        props = StatelessRuleProps(
            actions=actions,
            priority=priority,
            destination_ports=destination_ports,
            destinations=destinations,
            protocols=protocols,
            source_ports=source_ports,
            sources=sources,
            tcp_flags=tcp_flags,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="statelessRuleProperty")
    def stateless_rule_property(
        self,
    ) -> _aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty, jsii.get(self, "statelessRuleProperty"))


@jsii.data_type(
    jsii_type="raindancers-network.firewall.StatelessRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "priority": "priority",
        "destination_ports": "destinationPorts",
        "destinations": "destinations",
        "protocols": "protocols",
        "source_ports": "sourcePorts",
        "sources": "sources",
        "tcp_flags": "tcpFlags",
    },
)
class StatelessRuleProps:
    def __init__(
        self,
        *,
        actions: typing.Sequence[StatelessActions],
        priority: jsii.Number,
        destination_ports: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
        destinations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        protocols: typing.Optional[typing.Sequence[Protocol]] = None,
        source_ports: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
        sources: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tcp_flags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param actions: 
        :param priority: 
        :param destination_ports: 
        :param destinations: 
        :param protocols: 
        :param source_ports: 
        :param sources: 
        :param tcp_flags: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc71ccde7d817dda4079246fa13d4d30e58ccec2ef26cac9348da05db8e5805)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tcp_flags", value=tcp_flags, expected_type=type_hints["tcp_flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "priority": priority,
        }
        if destination_ports is not None:
            self._values["destination_ports"] = destination_ports
        if destinations is not None:
            self._values["destinations"] = destinations
        if protocols is not None:
            self._values["protocols"] = protocols
        if source_ports is not None:
            self._values["source_ports"] = source_ports
        if sources is not None:
            self._values["sources"] = sources
        if tcp_flags is not None:
            self._values["tcp_flags"] = tcp_flags

    @builtins.property
    def actions(self) -> typing.List[StatelessActions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[StatelessActions], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def destination_ports(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, jsii.Number]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination_ports")
        return typing.cast(typing.Optional[typing.List[typing.Union[builtins.str, jsii.Number]]], result)

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty]], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[Protocol]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[Protocol]], result)

    @builtins.property
    def source_ports(
        self,
    ) -> typing.Optional[typing.List[typing.Union[builtins.str, jsii.Number]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("source_ports")
        return typing.cast(typing.Optional[typing.List[typing.Union[builtins.str, jsii.Number]]], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty]], result)

    @builtins.property
    def tcp_flags(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tcp_flags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatelessRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.firewall.WellKnownPorts")
class WellKnownPorts(enum.Enum):
    '''
    :stability: experimental
    '''

    SSH = "SSH"
    '''
    :stability: experimental
    '''
    HTTP = "HTTP"
    '''
    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''
    :stability: experimental
    '''
    RDP = "RDP"
    '''
    :stability: experimental
    '''


__all__ = [
    "AddStatefulRulesProps",
    "AddStatelessRulesProps",
    "FirewallPolicy",
    "FirewallPolicyProps",
    "IFirewallPolicyProperty",
    "ManagedAwsFirewallRules",
    "Protocol",
    "RuleGroupType",
    "StatefulDefaultActions",
    "StatelessActions",
    "StatelessRule",
    "StatelessRuleProps",
    "WellKnownPorts",
]

publication.publish()

def _typecheckingstub__70ea0f84387576ba16d0553ab554d28a4b08cf9efafe62e537439313e9710883(
    *,
    aws_managed_rules: typing.Sequence[ManagedAwsFirewallRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f899e7bd165175985b55bf129db6e5477559ec80a27ed2998334a0c8edb6b715(
    *,
    description: builtins.str,
    group_name: builtins.str,
    rules: typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.StatelessRuleProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35735e2d85fa6c6e7e8795dd04383d88e08c2bf98872ddbaa7926067217104f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    policy_name: builtins.str,
    stateless_default_actions: typing.Sequence[StatelessActions],
    stateless_fragment_default_actions: typing.Sequence[StatelessActions],
    stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d06b2cb9ea14c763b913431cc679731cd7e6b31511f3ef54ae6fd9e9447adea(
    value: IFirewallPolicyProperty,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc18aca8b81d2ce71217f5d1e7d403ed7083146f12b3fa95c6faed06c5498069(
    *,
    policy_name: builtins.str,
    stateless_default_actions: typing.Sequence[StatelessActions],
    stateless_fragment_default_actions: typing.Sequence[StatelessActions],
    stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edf1f1a0d5f20fb3add4c5b51fb5dd58fed184ac979140e6501bcfe9c50ac84(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2397ea190084c1fcfce1802975b994221c5c66044b86bc6d882325de8f5aa4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09af2ad5eab00e627e1d9bfcbaec7ad4d9ac4ac3658703612b4781c7caf0fc8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456484d36eaade38b50bf69aba75f3adb0044432098b974da8024451d901360f(
    value: typing.Optional[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulEngineOptionsProperty, _aws_cdk_ceddda9d.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df9f94a207c804d36ebb388b7df4c75d51d98324a37d8373593db51b80156cb(
    value: typing.Optional[typing.List[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6929aba6a0340caf441e1d0c6b18e2fa3a69cf6f4cc127eccf22c9d260d339b(
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.CustomActionProperty, _aws_cdk_ceddda9d.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628a61cfeb75ba1bc2f7ce5a321b07644869230e96969053d378d14dda59e807(
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc71ccde7d817dda4079246fa13d4d30e58ccec2ef26cac9348da05db8e5805(
    *,
    actions: typing.Sequence[StatelessActions],
    priority: jsii.Number,
    destination_ports: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
    destinations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protocols: typing.Optional[typing.Sequence[Protocol]] = None,
    source_ports: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
    sources: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tcp_flags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_networkfirewall_ceddda9d.CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
