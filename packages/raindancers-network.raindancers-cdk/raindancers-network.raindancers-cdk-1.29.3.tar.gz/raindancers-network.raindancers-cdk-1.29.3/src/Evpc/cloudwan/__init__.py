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
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_networkmanager as _aws_cdk_aws_networkmanager_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="raindancers-network.cloudwan.AssociationMethod")
class AssociationMethod(enum.Enum):
    '''(experimental) Association Methods.

    :stability: experimental
    '''

    CONSTANT = "CONSTANT"
    '''
    :stability: experimental
    '''
    TAG = "TAG"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.AttachmentCondition")
class AttachmentCondition(enum.Enum):
    '''(experimental) Attachment Conditions.

    :stability: experimental
    '''

    ANY = "ANY"
    '''
    :stability: experimental
    '''
    RESOURCE_ID = "RESOURCE_ID"
    '''
    :stability: experimental
    '''
    ACCOUNT_ID = "ACCOUNT_ID"
    '''
    :stability: experimental
    '''
    REGION = "REGION"
    '''
    :stability: experimental
    '''
    ATTACHMENT_TYPE = "ATTACHMENT_TYPE"
    '''
    :stability: experimental
    '''
    TAG_EXISTS = "TAG_EXISTS"
    '''
    :stability: experimental
    '''
    TAG_VALUE = "TAG_VALUE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.AttachmentConditions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class AttachmentConditions:
    def __init__(
        self,
        *,
        type: AttachmentCondition,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional["Operators"] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) an attachmentconditions.

        :param type: 
        :param key: 
        :param operator: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4beff5203da213443685a48d253748a9c022d955e2475720248d46b97670a2c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> AttachmentCondition:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(AttachmentCondition, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional["Operators"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional["Operators"], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.AttachmentPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "conditions": "conditions",
        "rule_number": "ruleNumber",
        "condition_logic": "conditionLogic",
        "description": "description",
    },
)
class AttachmentPolicy:
    def __init__(
        self,
        *,
        action: typing.Union["AttachmentPolicyAction", typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Sequence[typing.Union[AttachmentConditions, typing.Dict[builtins.str, typing.Any]]],
        rule_number: jsii.Number,
        condition_logic: typing.Optional["ConditionLogic"] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) an attachment policy.

        :param action: 
        :param conditions: 
        :param rule_number: 
        :param condition_logic: 
        :param description: 

        :stability: experimental
        '''
        if isinstance(action, dict):
            action = AttachmentPolicyAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9081d338d1d0edb38ac67eac3098aa2a1ffd03df9ed61c01d33d85548571f14d)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument condition_logic", value=condition_logic, expected_type=type_hints["condition_logic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "conditions": conditions,
            "rule_number": rule_number,
        }
        if condition_logic is not None:
            self._values["condition_logic"] = condition_logic
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(self) -> "AttachmentPolicyAction":
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AttachmentPolicyAction", result)

    @builtins.property
    def conditions(self) -> typing.List[AttachmentConditions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.List[AttachmentConditions], result)

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def condition_logic(self) -> typing.Optional["ConditionLogic"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("condition_logic")
        return typing.cast(typing.Optional["ConditionLogic"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.AttachmentPolicyAction",
    jsii_struct_bases=[],
    name_mapping={
        "association_method": "associationMethod",
        "require_acceptance": "requireAcceptance",
        "segment": "segment",
    },
)
class AttachmentPolicyAction:
    def __init__(
        self,
        *,
        association_method: AssociationMethod,
        require_acceptance: typing.Optional[builtins.bool] = None,
        segment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attachment Policy Action.

        :param association_method: (experimental) The Assocation Method.
        :param require_acceptance: (experimental) Does this require approval.
        :param segment: (experimental) The Segment this applies to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea1ad6cb3aed5c2680d1220d689553eb05f291855bdf174af38f4b147546136)
            check_type(argname="argument association_method", value=association_method, expected_type=type_hints["association_method"])
            check_type(argname="argument require_acceptance", value=require_acceptance, expected_type=type_hints["require_acceptance"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "association_method": association_method,
        }
        if require_acceptance is not None:
            self._values["require_acceptance"] = require_acceptance
        if segment is not None:
            self._values["segment"] = segment

    @builtins.property
    def association_method(self) -> AssociationMethod:
        '''(experimental) The Assocation Method.

        :stability: experimental
        '''
        result = self._values.get("association_method")
        assert result is not None, "Required property 'association_method' is missing"
        return typing.cast(AssociationMethod, result)

    @builtins.property
    def require_acceptance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Does this require approval.

        :stability: experimental
        '''
        result = self._values.get("require_acceptance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Segment this applies to.

        :stability: experimental
        '''
        result = self._values.get("segment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachmentPolicyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWanTGW(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.cloudwan.CloudWanTGW",
):
    '''(experimental) Create a TransitGateway That is attached to Cloudwan.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        amazon_side_asn: builtins.str,
        attachment_segment: builtins.str,
        cloudwan: "CoreNetwork",
        description: builtins.str,
        cloud_wan_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_route_in_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
        tg_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: scope in which the resource is c.
        :param id: -
        :param amazon_side_asn: 
        :param attachment_segment: 
        :param cloudwan: 
        :param description: 
        :param cloud_wan_cidr: 
        :param default_route_in_segments: 
        :param tg_cidr: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f088616079545eb5c85f7f5348ae8a37cfae40e5d257585f3447604e6e6bb88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TGWOnCloudWanProps(
            amazon_side_asn=amazon_side_asn,
            attachment_segment=attachment_segment,
            cloudwan=cloudwan,
            description=description,
            cloud_wan_cidr=cloud_wan_cidr,
            default_route_in_segments=default_route_in_segments,
            tg_cidr=tg_cidr,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDXGateway")
    def add_dx_gateway(
        self,
        dxgatewayname: builtins.str,
        dxgateway_asn: jsii.Number,
    ) -> builtins.str:
        '''(experimental) provision a DX Gateway and attach it to the transit gateway.

        :param dxgatewayname: The name of the dxgateway.
        :param dxgateway_asn: An ASN for the Dxgateway.

        :return: Direct Connect gatewayId

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8b12d488dfd2a0bef1616d73d367833cf27a988fae47a9d9ea9e531127144b)
            check_type(argname="argument dxgatewayname", value=dxgatewayname, expected_type=type_hints["dxgatewayname"])
            check_type(argname="argument dxgateway_asn", value=dxgateway_asn, expected_type=type_hints["dxgateway_asn"])
        return typing.cast(builtins.str, jsii.invoke(self, "addDXGateway", [dxgatewayname, dxgateway_asn]))

    @jsii.member(jsii_name="adds2sVPN")
    def adds2s_vpn(
        self,
        name: builtins.str,
        *,
        customer_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway,
        vpnspec: typing.Union["VpnSpecProps", typing.Dict[builtins.str, typing.Any]],
        sampleconfig: typing.Optional[typing.Union["SampleConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel_inside_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_ipam_pool: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool] = None,
    ) -> None:
        '''(experimental) Creates a Site To Site IPSec VPN between the Transit Gateway and Customer Gateway, using a defined set of VPn Properties.

        :param name: A name to identify the vpn.
        :param customer_gateway: (experimental) The customer gateway where the vpn will terminate.
        :param vpnspec: (experimental) a VPN specification for the VPN.
        :param sampleconfig: (experimental) Optionally provide a sampleconfig specification.
        :param tunnel_inside_cidr: (experimental) Specify a pair of concrete Cidr's for the tunnel. Only use one of tunnelInsideCidr or tunnelIpmamPool
        :param tunnel_ipam_pool: (experimental) Specify an ipam pool to allocated the tunnel address's from. Use only one of tunnelInsideCidr or tunnelIpamPool

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa00cea3e9e0c8f0c517493e94994a623b0b7b1b974fc2f7b1080b6892865dcf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        vpnprops = VpnProps(
            customer_gateway=customer_gateway,
            vpnspec=vpnspec,
            sampleconfig=sampleconfig,
            tunnel_inside_cidr=tunnel_inside_cidr,
            tunnel_ipam_pool=tunnel_ipam_pool,
        )

        return typing.cast(None, jsii.invoke(self, "adds2sVPN", [name, vpnprops]))

    @jsii.member(jsii_name="createDirectConnectGatewayAssociation")
    def create_direct_connect_gateway_association(
        self,
        dxgateway_id: builtins.str,
    ) -> builtins.str:
        '''
        :param dxgateway_id: Id of a DX gateway that.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acf08598e3495fd74d7d3fd57e44c3feff6c17c6c5e27d76d23e7e3589e00b3)
            check_type(argname="argument dxgateway_id", value=dxgateway_id, expected_type=type_hints["dxgateway_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "createDirectConnectGatewayAssociation", [dxgateway_id]))

    @builtins.property
    @jsii.member(jsii_name="cloudwanTgAttachmentId")
    def cloudwan_tg_attachment_id(self) -> builtins.str:
        '''(experimental) the AttachmentId between the Transit Gateway and the cloudwan.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cloudwanTgAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway:
        '''(experimental) The created Transit Gateway.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway, jsii.get(self, "transitGateway"))

    @builtins.property
    @jsii.member(jsii_name="tgcidr")
    def tgcidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The Cidr Ranges assigned to the transit Gateway.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tgcidr"))

    @builtins.property
    @jsii.member(jsii_name="tgDXattachmentId")
    def tg_d_xattachment_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the AttachmentId between the Transit Gateway and DX ( if any ).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tgDXattachmentId"))

    @tg_d_xattachment_id.setter
    def tg_d_xattachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917364e1186de60c98928a7de3ab729bb5ba02360e2dcb92f866a1ed5a0412f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tgDXattachmentId", value)


@jsii.enum(jsii_type="raindancers-network.cloudwan.ConditionLogic")
class ConditionLogic(enum.Enum):
    '''(experimental) Conditon Logic.

    :stability: experimental
    '''

    AND = "AND"
    '''
    :stability: experimental
    '''
    OR = "OR"
    '''
    :stability: experimental
    '''


class CoreNetwork(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.cloudwan.CoreNetwork",
):
    '''(experimental) Create a CoreNework for a Cloudwan.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        core_name: builtins.str,
        edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
        global_network: _aws_cdk_aws_networkmanager_ceddda9d.CfnGlobalNetwork,
        policy_description: builtins.str,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        non_production: typing.Optional[builtins.bool] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param asn_ranges: (experimental) a list of of asn's that can be used.
        :param core_name: (experimental) core name.
        :param edge_locations: (experimental) list of edgeLocaitons.
        :param global_network: (experimental) Which Global Network.
        :param policy_description: (experimental) a decription for the policy Document.
        :param inside_cidr_blocks: (experimental) List of InsideCidr Blocks.
        :param non_production: (experimental) If this is a non production stack, backups will not be made.
        :param vpn_ecmp_support: (experimental) support VpnECmp.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8250cec8cd004488eac92d55d75c032d1e94e61a673900ec0d4ff6290084d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CoreNetworkProps(
            asn_ranges=asn_ranges,
            core_name=core_name,
            edge_locations=edge_locations,
            global_network=global_network,
            policy_description=policy_description,
            inside_cidr_blocks=inside_cidr_blocks,
            non_production=non_production,
            vpn_ecmp_support=vpn_ecmp_support,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSegment")
    def add_segment(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        isolate_attachments: typing.Optional[builtins.bool] = None,
        require_attachment_acceptance: typing.Optional[builtins.bool] = None,
    ) -> "CoreNetworkSegment":
        '''(experimental) Add a segment to the core network.

        :param name: (experimental) Name of the Segment.
        :param allow_filter: (experimental) A list of denys.
        :param deny_filter: (experimental) a List of denys.
        :param description: (experimental) A description of the of the segement.
        :param edge_locations: (experimental) A list of edge locations where the segement will be avaialble. Not that the locations must also be included in the core network edge ( CNE )
        :param isolate_attachments: (experimental) Set true if attached VPCS are isolated from each other.
        :param require_attachment_acceptance: (experimental) Set true if the attachment needs approval for connection. Currently not supported and requires an automation step

        :stability: experimental
        '''
        props = Segment(
            name=name,
            allow_filter=allow_filter,
            deny_filter=deny_filter,
            description=description,
            edge_locations=edge_locations,
            isolate_attachments=isolate_attachments,
            require_attachment_acceptance=require_attachment_acceptance,
        )

        return typing.cast("CoreNetworkSegment", jsii.invoke(self, "addSegment", [props]))

    @jsii.member(jsii_name="share")
    def share(
        self,
        *,
        allow_external_principals: builtins.bool,
        principals: typing.Sequence[builtins.str],
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''(experimental) Create a CoreNetwork Sharing.

        :param allow_external_principals: 
        :param principals: 
        :param tags: 

        :stability: experimental
        '''
        props = CoreNetworkShare(
            allow_external_principals=allow_external_principals,
            principals=principals,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "share", [props]))

    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> None:
        '''(experimental) Update the corewan policy after actions, segments are added.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "updatePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="cfnCoreNetwork")
    def cfn_core_network(self) -> _aws_cdk_aws_networkmanager_ceddda9d.CfnCoreNetwork:
        '''(experimental) The corenetwork object.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_networkmanager_ceddda9d.CfnCoreNetwork, jsii.get(self, "cfnCoreNetwork"))

    @builtins.property
    @jsii.member(jsii_name="coreName")
    def core_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "coreName"))

    @builtins.property
    @jsii.member(jsii_name="policyTable")
    def policy_table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        '''(experimental) THe dynamo table holding the policy.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "policyTable"))

    @builtins.property
    @jsii.member(jsii_name="policyTableName")
    def policy_table_name(self) -> builtins.str:
        '''(experimental) Name of the Dynamo Table holding the policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableName"))

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''(experimental) The policyTable Lamba's Service Token.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="updateProviderToken")
    def update_provider_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updateProviderToken"))

    @update_provider_token.setter
    def update_provider_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcaa1146649d1f5abb59b9631529005c656d53c854544c24210f21a3bb22d866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateProviderToken", value)


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.CoreNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "asn_ranges": "asnRanges",
        "core_name": "coreName",
        "edge_locations": "edgeLocations",
        "global_network": "globalNetwork",
        "policy_description": "policyDescription",
        "inside_cidr_blocks": "insideCidrBlocks",
        "non_production": "nonProduction",
        "vpn_ecmp_support": "vpnEcmpSupport",
    },
)
class CoreNetworkProps:
    def __init__(
        self,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        core_name: builtins.str,
        edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
        global_network: _aws_cdk_aws_networkmanager_ceddda9d.CfnGlobalNetwork,
        policy_description: builtins.str,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        non_production: typing.Optional[builtins.bool] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) CoreNetwork Properties.

        :param asn_ranges: (experimental) a list of of asn's that can be used.
        :param core_name: (experimental) core name.
        :param edge_locations: (experimental) list of edgeLocaitons.
        :param global_network: (experimental) Which Global Network.
        :param policy_description: (experimental) a decription for the policy Document.
        :param inside_cidr_blocks: (experimental) List of InsideCidr Blocks.
        :param non_production: (experimental) If this is a non production stack, backups will not be made.
        :param vpn_ecmp_support: (experimental) support VpnECmp.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b2cef97b467b8a6370abe89945b8981aff04b5dc665b0d41743a27f6b00f2c)
            check_type(argname="argument asn_ranges", value=asn_ranges, expected_type=type_hints["asn_ranges"])
            check_type(argname="argument core_name", value=core_name, expected_type=type_hints["core_name"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument global_network", value=global_network, expected_type=type_hints["global_network"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            check_type(argname="argument non_production", value=non_production, expected_type=type_hints["non_production"])
            check_type(argname="argument vpn_ecmp_support", value=vpn_ecmp_support, expected_type=type_hints["vpn_ecmp_support"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asn_ranges": asn_ranges,
            "core_name": core_name,
            "edge_locations": edge_locations,
            "global_network": global_network,
            "policy_description": policy_description,
        }
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks
        if non_production is not None:
            self._values["non_production"] = non_production
        if vpn_ecmp_support is not None:
            self._values["vpn_ecmp_support"] = vpn_ecmp_support

    @builtins.property
    def asn_ranges(self) -> typing.List[builtins.str]:
        '''(experimental) a list of of asn's that can be used.

        :stability: experimental
        '''
        result = self._values.get("asn_ranges")
        assert result is not None, "Required property 'asn_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def core_name(self) -> builtins.str:
        '''(experimental) core name.

        :stability: experimental
        '''
        result = self._values.get("core_name")
        assert result is not None, "Required property 'core_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edge_locations(self) -> typing.List[typing.Mapping[typing.Any, typing.Any]]:
        '''(experimental) list of edgeLocaitons.

        :stability: experimental
        '''
        result = self._values.get("edge_locations")
        assert result is not None, "Required property 'edge_locations' is missing"
        return typing.cast(typing.List[typing.Mapping[typing.Any, typing.Any]], result)

    @builtins.property
    def global_network(self) -> _aws_cdk_aws_networkmanager_ceddda9d.CfnGlobalNetwork:
        '''(experimental) Which Global Network.

        :stability: experimental
        '''
        result = self._values.get("global_network")
        assert result is not None, "Required property 'global_network' is missing"
        return typing.cast(_aws_cdk_aws_networkmanager_ceddda9d.CfnGlobalNetwork, result)

    @builtins.property
    def policy_description(self) -> builtins.str:
        '''(experimental) a decription for the policy Document.

        :stability: experimental
        '''
        result = self._values.get("policy_description")
        assert result is not None, "Required property 'policy_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of InsideCidr Blocks.

        :stability: experimental
        '''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def non_production(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is a non production stack, backups will not be made.

        :stability: experimental
        '''
        result = self._values.get("non_production")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_ecmp_support(self) -> typing.Optional[builtins.bool]:
        '''(experimental) support VpnECmp.

        :stability: experimental
        '''
        result = self._values.get("vpn_ecmp_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CoreNetworkSegment(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.cloudwan.CoreNetworkSegment",
):
    '''(experimental) Create a Network Segment in a core network.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "ICoreNetworkSegmentProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e636aa958d739f110f0ce9e0f2dfb17403e7943eef65b42f96d6ad04d1df3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAttachmentPolicy")
    def add_attachment_policy(
        self,
        *,
        action: typing.Union[AttachmentPolicyAction, typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Sequence[typing.Union[AttachmentConditions, typing.Dict[builtins.str, typing.Any]]],
        rule_number: jsii.Number,
        condition_logic: typing.Optional[ConditionLogic] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add an AttachmentPolicy to a segment.

        :param action: 
        :param conditions: 
        :param rule_number: 
        :param condition_logic: 
        :param description: 

        :stability: experimental
        '''
        props = AttachmentPolicy(
            action=action,
            conditions=conditions,
            rule_number=rule_number,
            condition_logic=condition_logic,
            description=description,
        )

        return typing.cast(None, jsii.invoke(self, "addAttachmentPolicy", [props]))

    @jsii.member(jsii_name="addSegmentAction")
    def add_segment_action(
        self,
        *,
        action: "SegmentActionType",
        description: builtins.str,
        destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        except_: typing.Optional[typing.Sequence[builtins.str]] = None,
        mode: typing.Optional["SegmentActionMode"] = None,
        share_with: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Add an Action to the Segment, ( Share or Route ).

        :param action: 
        :param description: 
        :param destination_cidr_blocks: 
        :param destinations: 
        :param except_: 
        :param mode: 
        :param share_with: 

        :stability: experimental
        '''
        props = SegmentAction(
            action=action,
            description=description,
            destination_cidr_blocks=destination_cidr_blocks,
            destinations=destinations,
            except_=except_,
            mode=mode,
            share_with=share_with,
        )

        return typing.cast(None, jsii.invoke(self, "addSegmentAction", [props]))

    @jsii.member(jsii_name="addSimpleAttachmentPolicy")
    def add_simple_attachment_policy(
        self,
        *,
        rule_number: jsii.Number,
        account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_number: 
        :param account: 

        :stability: experimental
        '''
        props = SimpleAttachmentPolicyProps(rule_number=rule_number, account=account)

        return typing.cast(None, jsii.invoke(self, "addSimpleAttachmentPolicy", [props]))

    @jsii.member(jsii_name="addSimpleShareAction")
    def add_simple_share_action(
        self,
        *,
        description: builtins.str,
        share_with: typing.Union[builtins.str, typing.Sequence["CoreNetworkSegment"]],
    ) -> None:
        '''
        :param description: 
        :param share_with: 

        :stability: experimental
        '''
        props = SimpleShareActionProps(description=description, share_with=share_with)

        return typing.cast(None, jsii.invoke(self, "addSimpleShareAction", [props]))

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''(experimental) Service token for.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''(experimental) the name for the segment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentName"))


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.CoreNetworkShare",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_principals": "allowExternalPrincipals",
        "principals": "principals",
        "tags": "tags",
    },
)
class CoreNetworkShare:
    def __init__(
        self,
        *,
        allow_external_principals: builtins.bool,
        principals: typing.Sequence[builtins.str],
        tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
    ) -> None:
        '''(experimental) CoreNetworkShare.

        :param allow_external_principals: 
        :param principals: 
        :param tags: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea13880429af47628b9623d3416319ee10b8f03b3e8e172a1bcb58527e646823)
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_external_principals": allow_external_principals,
            "principals": principals,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allow_external_principals(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("allow_external_principals")
        assert result is not None, "Required property 'allow_external_principals' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Tag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreNetworkShare(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.cloudwan.DPDTimeoutAction")
class DPDTimeoutAction(enum.Enum):
    '''(experimental) Dead Peer Detection Timeout Actions.

    :stability: experimental
    '''

    CLEAR = "CLEAR"
    '''(experimental) Clear the Session.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Do nothing.

    :stability: experimental
    '''
    RESTART = "RESTART"
    '''(experimental) Restart The Session.

    :stability: experimental
    '''


@jsii.interface(jsii_type="raindancers-network.cloudwan.ICoreNetworkSegmentProps")
class ICoreNetworkSegmentProps(typing_extensions.Protocol):
    '''(experimental) Properties creating a Corenetwork Segment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updateDependsOn")
    def update_depends_on(self) -> typing.List[_aws_cdk_ceddda9d.CustomResource]:
        '''
        :stability: experimental
        '''
        ...

    @update_depends_on.setter
    def update_depends_on(
        self,
        value: typing.List[_aws_cdk_ceddda9d.CustomResource],
    ) -> None:
        ...


class _ICoreNetworkSegmentPropsProxy:
    '''(experimental) Properties creating a Corenetwork Segment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "raindancers-network.cloudwan.ICoreNetworkSegmentProps"

    @builtins.property
    @jsii.member(jsii_name="policyTableServiceToken")
    def policy_table_service_token(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyTableServiceToken"))

    @builtins.property
    @jsii.member(jsii_name="segmentName")
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "segmentName"))

    @builtins.property
    @jsii.member(jsii_name="updateDependsOn")
    def update_depends_on(self) -> typing.List[_aws_cdk_ceddda9d.CustomResource]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_ceddda9d.CustomResource], jsii.get(self, "updateDependsOn"))

    @update_depends_on.setter
    def update_depends_on(
        self,
        value: typing.List[_aws_cdk_ceddda9d.CustomResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488bf3c7b78a130f30d96088a385ce8de9310cb01454bed905d75754bb6916a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateDependsOn", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICoreNetworkSegmentProps).__jsii_proxy_class__ = lambda : _ICoreNetworkSegmentPropsProxy


@jsii.enum(jsii_type="raindancers-network.cloudwan.IkeVersion")
class IkeVersion(enum.Enum):
    '''(experimental) Ike Version for S2S VPN.

    :stability: experimental
    '''

    IKEV1 = "IKEV1"
    '''(experimental) Use IKEv1.

    :stability: experimental
    '''
    IKEV2 = "IKEV2"
    '''(experimental) Use IKEv2.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Operators")
class Operators(enum.Enum):
    '''(experimental) Operatior COnditons for Attachments.

    :stability: experimental
    '''

    EQUALS = "EQUALS"
    '''
    :stability: experimental
    '''
    NOTEQUALS = "NOTEQUALS"
    '''
    :stability: experimental
    '''
    CONTAINS = "CONTAINS"
    '''
    :stability: experimental
    '''
    BEGINS_WITH = "BEGINS_WITH"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.OutsideIpAddressType")
class OutsideIpAddressType(enum.Enum):
    '''(experimental) Specify the use of public or private IP address's for Site to Site VPN.

    :stability: experimental
    '''

    PRIVATE = "PRIVATE"
    '''(experimental) Use Private IPv4 Address from the Transit Gateways IP address Pool.

    :stability: experimental
    '''
    PUBLIC = "PUBLIC"
    '''(experimental) Use Public IPv4 Address Assigned by AWS.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Phase1DHGroupNumbers")
class Phase1DHGroupNumbers(enum.Enum):
    '''
    :stability: experimental
    '''

    DH2 = "DH2"
    '''
    :stability: experimental
    '''
    DH14 = "DH14"
    '''
    :stability: experimental
    '''
    DH15 = "DH15"
    '''
    :stability: experimental
    '''
    DH16 = "DH16"
    '''
    :stability: experimental
    '''
    DH17 = "DH17"
    '''
    :stability: experimental
    '''
    DH18 = "DH18"
    '''
    :stability: experimental
    '''
    DH19 = "DH19"
    '''
    :stability: experimental
    '''
    DH20 = "DH20"
    '''
    :stability: experimental
    '''
    DH21 = "DH21"
    '''
    :stability: experimental
    '''
    DH22 = "DH22"
    '''
    :stability: experimental
    '''
    DH23 = "DH23"
    '''
    :stability: experimental
    '''
    DH24 = "DH24"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Phase1EncryptionAlgorithms")
class Phase1EncryptionAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    AES128 = "AES128"
    '''
    :stability: experimental
    '''
    AES256 = "AES256"
    '''
    :stability: experimental
    '''
    AES128_GCM_16 = "AES128_GCM_16"
    '''
    :stability: experimental
    '''
    AES256_GCM_16 = "AES256_GCM_16"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Phase1IntegrityAlgorithms")
class Phase1IntegrityAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    SHA1 = "SHA1"
    '''
    :stability: experimental
    '''
    SHA2_256 = "SHA2_256"
    '''
    :stability: experimental
    '''
    SHA2_384 = "SHA2_384"
    '''
    :stability: experimental
    '''
    SHA2_512 = "SHA2_512"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Phase2DHGroupNumbers")
class Phase2DHGroupNumbers(enum.Enum):
    '''
    :stability: experimental
    '''

    DH2 = "DH2"
    '''
    :stability: experimental
    '''
    DH5 = "DH5"
    '''
    :stability: experimental
    '''
    DH14 = "DH14"
    '''
    :stability: experimental
    '''
    DH15 = "DH15"
    '''
    :stability: experimental
    '''
    DH16 = "DH16"
    '''
    :stability: experimental
    '''
    DH17 = "DH17"
    '''
    :stability: experimental
    '''
    DH18 = "DH18"
    '''
    :stability: experimental
    '''
    DH19 = "DH19"
    '''
    :stability: experimental
    '''
    DH20 = "DH20"
    '''
    :stability: experimental
    '''
    DH21 = "DH21"
    '''
    :stability: experimental
    '''
    DH22 = "DH22"
    '''
    :stability: experimental
    '''
    DH23 = "DH23"
    '''
    :stability: experimental
    '''
    DH24 = "DH24"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Phase2EncryptionAlgorithms")
class Phase2EncryptionAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    AES128 = "AES128"
    '''
    :stability: experimental
    '''
    AES256 = "AES256"
    '''
    :stability: experimental
    '''
    AES128_GCM_16 = "AES128_GCM_16"
    '''
    :stability: experimental
    '''
    AES256_GCM_16 = "AES256_GCM_16"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.Phase2IntegrityAlgorithms")
class Phase2IntegrityAlgorithms(enum.Enum):
    '''
    :stability: experimental
    '''

    SHA1 = "SHA1"
    '''
    :stability: experimental
    '''
    SHA2_256 = "SHA2_256"
    '''
    :stability: experimental
    '''
    SHA2_384 = "SHA2_384"
    '''
    :stability: experimental
    '''
    SHA2_512 = "SHA2_512"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.SampleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "device_type": "deviceType",
        "ike_version": "ikeVersion",
    },
)
class SampleConfig:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
        device_type: "VpnDeviceType",
        ike_version: IkeVersion,
    ) -> None:
        '''(experimental) An interface that defines a set of Sample Configurations.

        :param bucket: (experimental) The S3 bucket where to place the sample configurations.
        :param device_type: (experimental) the type of device of the customer gateway.
        :param ike_version: (experimental) create configs for IKE1 or IKE2.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e503ce117878a6ecf8e86a5387df98a3d1502c673e4d15479c1cdb452b8716)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
            check_type(argname="argument ike_version", value=ike_version, expected_type=type_hints["ike_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "device_type": device_type,
            "ike_version": ike_version,
        }

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''(experimental) The S3 bucket where to place the sample configurations.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, result)

    @builtins.property
    def device_type(self) -> "VpnDeviceType":
        '''(experimental) the type of device of the customer gateway.

        :stability: experimental
        '''
        result = self._values.get("device_type")
        assert result is not None, "Required property 'device_type' is missing"
        return typing.cast("VpnDeviceType", result)

    @builtins.property
    def ike_version(self) -> IkeVersion:
        '''(experimental) create configs for IKE1 or IKE2.

        :stability: experimental
        '''
        result = self._values.get("ike_version")
        assert result is not None, "Required property 'ike_version' is missing"
        return typing.cast(IkeVersion, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SampleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.Segment",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_filter": "allowFilter",
        "deny_filter": "denyFilter",
        "description": "description",
        "edge_locations": "edgeLocations",
        "isolate_attachments": "isolateAttachments",
        "require_attachment_acceptance": "requireAttachmentAcceptance",
    },
)
class Segment:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        isolate_attachments: typing.Optional[builtins.bool] = None,
        require_attachment_acceptance: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Segment Properties.

        :param name: (experimental) Name of the Segment.
        :param allow_filter: (experimental) A list of denys.
        :param deny_filter: (experimental) a List of denys.
        :param description: (experimental) A description of the of the segement.
        :param edge_locations: (experimental) A list of edge locations where the segement will be avaialble. Not that the locations must also be included in the core network edge ( CNE )
        :param isolate_attachments: (experimental) Set true if attached VPCS are isolated from each other.
        :param require_attachment_acceptance: (experimental) Set true if the attachment needs approval for connection. Currently not supported and requires an automation step

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dcb5f1d0b8744c99bc2a045d812e86c0f2767e7cd773708599ef86d44bb43b2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_filter", value=allow_filter, expected_type=type_hints["allow_filter"])
            check_type(argname="argument deny_filter", value=deny_filter, expected_type=type_hints["deny_filter"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument isolate_attachments", value=isolate_attachments, expected_type=type_hints["isolate_attachments"])
            check_type(argname="argument require_attachment_acceptance", value=require_attachment_acceptance, expected_type=type_hints["require_attachment_acceptance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_filter is not None:
            self._values["allow_filter"] = allow_filter
        if deny_filter is not None:
            self._values["deny_filter"] = deny_filter
        if description is not None:
            self._values["description"] = description
        if edge_locations is not None:
            self._values["edge_locations"] = edge_locations
        if isolate_attachments is not None:
            self._values["isolate_attachments"] = isolate_attachments
        if require_attachment_acceptance is not None:
            self._values["require_attachment_acceptance"] = require_attachment_acceptance

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the Segment.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of denys.

        :stability: experimental
        '''
        result = self._values.get("allow_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) a List of denys.

        :stability: experimental
        '''
        result = self._values.get("deny_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the of the segement.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_locations(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]]:
        '''(experimental) A list of edge locations where the segement will be avaialble.

        Not that the
        locations must also be included in the core network edge ( CNE )

        :stability: experimental
        '''
        result = self._values.get("edge_locations")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]], result)

    @builtins.property
    def isolate_attachments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if attached VPCS are isolated from each other.

        :stability: experimental
        '''
        result = self._values.get("isolate_attachments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_attachment_acceptance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set true if the attachment needs approval for connection.

        Currently not supported
        and requires an automation step

        :stability: experimental
        '''
        result = self._values.get("require_attachment_acceptance")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Segment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.SegmentAction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "destination_cidr_blocks": "destinationCidrBlocks",
        "destinations": "destinations",
        "except_": "except",
        "mode": "mode",
        "share_with": "shareWith",
    },
)
class SegmentAction:
    def __init__(
        self,
        *,
        action: "SegmentActionType",
        description: builtins.str,
        destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        except_: typing.Optional[typing.Sequence[builtins.str]] = None,
        mode: typing.Optional["SegmentActionMode"] = None,
        share_with: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Segmment ACtions.

        :param action: 
        :param description: 
        :param destination_cidr_blocks: 
        :param destinations: 
        :param except_: 
        :param mode: 
        :param share_with: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720366174a28eb004e18a318e026f7bf9f0155fdcbb1578cf556d2e99e6e223e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_cidr_blocks", value=destination_cidr_blocks, expected_type=type_hints["destination_cidr_blocks"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument except_", value=except_, expected_type=type_hints["except_"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument share_with", value=share_with, expected_type=type_hints["share_with"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "description": description,
        }
        if destination_cidr_blocks is not None:
            self._values["destination_cidr_blocks"] = destination_cidr_blocks
        if destinations is not None:
            self._values["destinations"] = destinations
        if except_ is not None:
            self._values["except_"] = except_
        if mode is not None:
            self._values["mode"] = mode
        if share_with is not None:
            self._values["share_with"] = share_with

    @builtins.property
    def action(self) -> "SegmentActionType":
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("SegmentActionType", result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def except_(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("except_")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional["SegmentActionMode"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["SegmentActionMode"], result)

    @builtins.property
    def share_with(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("share_with")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.cloudwan.SegmentActionMode")
class SegmentActionMode(enum.Enum):
    '''(experimental) Segment Action Mode.

    :stability: experimental
    '''

    ATTACHMENT_ROUTE = "ATTACHMENT_ROUTE"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.SegmentActionType")
class SegmentActionType(enum.Enum):
    '''(experimental) Segment Action Type.

    :stability: experimental
    '''

    SHARE = "SHARE"
    '''
    :stability: experimental
    '''
    CREATE_ROUTE = "CREATE_ROUTE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.SimpleAttachmentPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"rule_number": "ruleNumber", "account": "account"},
)
class SimpleAttachmentPolicyProps:
    def __init__(
        self,
        *,
        rule_number: jsii.Number,
        account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_number: 
        :param account: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da580b31887123ae34275387881d6d816d7810ae88abcbf178fd857d8516ba6f)
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_number": rule_number,
        }
        if account is not None:
            self._values["account"] = account

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleAttachmentPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.SimpleShareActionProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "share_with": "shareWith"},
)
class SimpleShareActionProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        share_with: typing.Union[builtins.str, typing.Sequence[CoreNetworkSegment]],
    ) -> None:
        '''
        :param description: 
        :param share_with: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174af254cd37ae306f53afd67b72c4b201b03ea33b4bd49c683ccbe6f47ab408)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument share_with", value=share_with, expected_type=type_hints["share_with"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "share_with": share_with,
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
    def share_with(self) -> typing.Union[builtins.str, typing.List[CoreNetworkSegment]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("share_with")
        assert result is not None, "Required property 'share_with' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[CoreNetworkSegment]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleShareActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.cloudwan.StartupAction")
class StartupAction(enum.Enum):
    '''(experimental) Startup Action for S2S VPN.

    :stability: experimental
    '''

    START = "START"
    '''(experimental) AWS end to Intiate Startup.

    :stability: experimental
    '''
    ADD = "ADD"
    '''(experimental) Do not attempt to startup.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.TGWOnCloudWanProps",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_side_asn": "amazonSideAsn",
        "attachment_segment": "attachmentSegment",
        "cloudwan": "cloudwan",
        "description": "description",
        "cloud_wan_cidr": "cloudWanCidr",
        "default_route_in_segments": "defaultRouteInSegments",
        "tg_cidr": "tgCidr",
    },
)
class TGWOnCloudWanProps:
    def __init__(
        self,
        *,
        amazon_side_asn: builtins.str,
        attachment_segment: builtins.str,
        cloudwan: CoreNetwork,
        description: builtins.str,
        cloud_wan_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_route_in_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
        tg_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for a TWGOnCloudWan.

        :param amazon_side_asn: 
        :param attachment_segment: 
        :param cloudwan: 
        :param description: 
        :param cloud_wan_cidr: 
        :param default_route_in_segments: 
        :param tg_cidr: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d3cde16b7525c7c6384f3dcc12c540179962f2c2c2587b823c61752ef41951)
            check_type(argname="argument amazon_side_asn", value=amazon_side_asn, expected_type=type_hints["amazon_side_asn"])
            check_type(argname="argument attachment_segment", value=attachment_segment, expected_type=type_hints["attachment_segment"])
            check_type(argname="argument cloudwan", value=cloudwan, expected_type=type_hints["cloudwan"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument cloud_wan_cidr", value=cloud_wan_cidr, expected_type=type_hints["cloud_wan_cidr"])
            check_type(argname="argument default_route_in_segments", value=default_route_in_segments, expected_type=type_hints["default_route_in_segments"])
            check_type(argname="argument tg_cidr", value=tg_cidr, expected_type=type_hints["tg_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amazon_side_asn": amazon_side_asn,
            "attachment_segment": attachment_segment,
            "cloudwan": cloudwan,
            "description": description,
        }
        if cloud_wan_cidr is not None:
            self._values["cloud_wan_cidr"] = cloud_wan_cidr
        if default_route_in_segments is not None:
            self._values["default_route_in_segments"] = default_route_in_segments
        if tg_cidr is not None:
            self._values["tg_cidr"] = tg_cidr

    @builtins.property
    def amazon_side_asn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("amazon_side_asn")
        assert result is not None, "Required property 'amazon_side_asn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attachment_segment(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_segment")
        assert result is not None, "Required property 'attachment_segment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwan(self) -> CoreNetwork:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloudwan")
        assert result is not None, "Required property 'cloudwan' is missing"
        return typing.cast(CoreNetwork, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_wan_cidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloud_wan_cidr")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_route_in_segments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_route_in_segments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tg_cidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tg_cidr")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TGWOnCloudWanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.cloudwan.TunnelInsideIpVersion")
class TunnelInsideIpVersion(enum.Enum):
    '''(experimental) Determine if this is an IPv4 or IPv6 Tunnel.

    :stability: experimental
    '''

    IPV4 = "IPV4"
    '''(experimental) Use IPv4.

    :stability: experimental
    '''
    IPV6 = "IPV6"
    '''(experimental) Use IPv6.

    :stability: experimental
    '''


@jsii.enum(jsii_type="raindancers-network.cloudwan.VpnDeviceType")
class VpnDeviceType(enum.Enum):
    '''(experimental) Remote end Device Types.

    :stability: experimental
    '''

    CHECKPOINT_R77_10 = "CHECKPOINT_R77_10"
    '''(experimental) Checkpoint R77_10.

    :stability: experimental
    '''
    CHECKPOINT_R80_10 = "CHECKPOINT_R80_10"
    '''
    :stability: experimental
    '''
    CISCO_ISR_12_4 = "CISCO_ISR_12_4"
    '''
    :stability: experimental
    '''
    CISCO_ASR_12_4 = "CISCO_ASR_12_4"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.VpnProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway": "customerGateway",
        "vpnspec": "vpnspec",
        "sampleconfig": "sampleconfig",
        "tunnel_inside_cidr": "tunnelInsideCidr",
        "tunnel_ipam_pool": "tunnelIpamPool",
    },
)
class VpnProps:
    def __init__(
        self,
        *,
        customer_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway,
        vpnspec: typing.Union["VpnSpecProps", typing.Dict[builtins.str, typing.Any]],
        sampleconfig: typing.Optional[typing.Union[SampleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel_inside_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_ipam_pool: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool] = None,
    ) -> None:
        '''(experimental) Properties for S2S VPN.

        :param customer_gateway: (experimental) The customer gateway where the vpn will terminate.
        :param vpnspec: (experimental) a VPN specification for the VPN.
        :param sampleconfig: (experimental) Optionally provide a sampleconfig specification.
        :param tunnel_inside_cidr: (experimental) Specify a pair of concrete Cidr's for the tunnel. Only use one of tunnelInsideCidr or tunnelIpmamPool
        :param tunnel_ipam_pool: (experimental) Specify an ipam pool to allocated the tunnel address's from. Use only one of tunnelInsideCidr or tunnelIpamPool

        :stability: experimental
        '''
        if isinstance(vpnspec, dict):
            vpnspec = VpnSpecProps(**vpnspec)
        if isinstance(sampleconfig, dict):
            sampleconfig = SampleConfig(**sampleconfig)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3175b7d39afa1ff45148015ff62f7471e9d0b33322ee8677b01d33b7c059732)
            check_type(argname="argument customer_gateway", value=customer_gateway, expected_type=type_hints["customer_gateway"])
            check_type(argname="argument vpnspec", value=vpnspec, expected_type=type_hints["vpnspec"])
            check_type(argname="argument sampleconfig", value=sampleconfig, expected_type=type_hints["sampleconfig"])
            check_type(argname="argument tunnel_inside_cidr", value=tunnel_inside_cidr, expected_type=type_hints["tunnel_inside_cidr"])
            check_type(argname="argument tunnel_ipam_pool", value=tunnel_ipam_pool, expected_type=type_hints["tunnel_ipam_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway": customer_gateway,
            "vpnspec": vpnspec,
        }
        if sampleconfig is not None:
            self._values["sampleconfig"] = sampleconfig
        if tunnel_inside_cidr is not None:
            self._values["tunnel_inside_cidr"] = tunnel_inside_cidr
        if tunnel_ipam_pool is not None:
            self._values["tunnel_ipam_pool"] = tunnel_ipam_pool

    @builtins.property
    def customer_gateway(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway:
        '''(experimental) The customer gateway where the vpn will terminate.

        :stability: experimental
        '''
        result = self._values.get("customer_gateway")
        assert result is not None, "Required property 'customer_gateway' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway, result)

    @builtins.property
    def vpnspec(self) -> "VpnSpecProps":
        '''(experimental) a VPN specification for the VPN.

        :stability: experimental
        '''
        result = self._values.get("vpnspec")
        assert result is not None, "Required property 'vpnspec' is missing"
        return typing.cast("VpnSpecProps", result)

    @builtins.property
    def sampleconfig(self) -> typing.Optional[SampleConfig]:
        '''(experimental) Optionally provide a sampleconfig specification.

        :stability: experimental
        '''
        result = self._values.get("sampleconfig")
        return typing.cast(typing.Optional[SampleConfig], result)

    @builtins.property
    def tunnel_inside_cidr(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specify a pair of concrete Cidr's for the tunnel.

        Only use one of tunnelInsideCidr or tunnelIpmamPool

        :stability: experimental
        '''
        result = self._values.get("tunnel_inside_cidr")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel_ipam_pool(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool]:
        '''(experimental) Specify an ipam pool to allocated the tunnel address's from.

        Use only one of tunnelInsideCidr or tunnelIpamPool

        :stability: experimental
        '''
        result = self._values.get("tunnel_ipam_pool")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.cloudwan.VpnSpecProps",
    jsii_struct_bases=[],
    name_mapping={
        "dpd_timeout_action": "dpdTimeoutAction",
        "dpd_timeout_seconds": "dpdTimeoutSeconds",
        "enable_acceleration": "enableAcceleration",
        "enable_logging": "enableLogging",
        "ike_versions": "ikeVersions",
        "local_ipv4_network_cidr": "localIpv4NetworkCidr",
        "outside_ip_address_type": "outsideIpAddressType",
        "phase1_dh_group_numbers": "phase1DHGroupNumbers",
        "phase1_encryption_algorithms": "phase1EncryptionAlgorithms",
        "phase1_integrity_algorithms": "phase1IntegrityAlgorithms",
        "phase1_lifetime_seconds": "phase1LifetimeSeconds",
        "phase2_dh_group_numbers": "phase2DHGroupNumbers",
        "phase2_encryption_algorithms": "phase2EncryptionAlgorithms",
        "phase2_integrity_algorithms": "phase2IntegrityAlgorithms",
        "phase2_life_time_seconds": "phase2LifeTimeSeconds",
        "rekey_fuzz_percentage": "rekeyFuzzPercentage",
        "rekey_margin_time_seconds": "rekeyMarginTimeSeconds",
        "remote_ipv4_network_cidr": "remoteIpv4NetworkCidr",
        "replay_window_size": "replayWindowSize",
        "startup_action": "startupAction",
        "static_routes_only": "staticRoutesOnly",
        "tunnel_inside_ip_version": "tunnelInsideIpVersion",
    },
)
class VpnSpecProps:
    def __init__(
        self,
        *,
        dpd_timeout_action: typing.Optional[DPDTimeoutAction] = None,
        dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        enable_acceleration: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        ike_versions: typing.Optional[typing.Sequence[IkeVersion]] = None,
        local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        outside_ip_address_type: typing.Optional[OutsideIpAddressType] = None,
        phase1_dh_group_numbers: typing.Optional[typing.Sequence[Phase1DHGroupNumbers]] = None,
        phase1_encryption_algorithms: typing.Optional[typing.Sequence[Phase1EncryptionAlgorithms]] = None,
        phase1_integrity_algorithms: typing.Optional[typing.Sequence[Phase1IntegrityAlgorithms]] = None,
        phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        phase2_dh_group_numbers: typing.Optional[typing.Sequence[Phase2DHGroupNumbers]] = None,
        phase2_encryption_algorithms: typing.Optional[typing.Sequence[Phase2EncryptionAlgorithms]] = None,
        phase2_integrity_algorithms: typing.Optional[typing.Sequence[Phase2IntegrityAlgorithms]] = None,
        phase2_life_time_seconds: typing.Optional[jsii.Number] = None,
        rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        replay_window_size: typing.Optional[jsii.Number] = None,
        startup_action: typing.Optional[StartupAction] = None,
        static_routes_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tunnel_inside_ip_version: typing.Optional[TunnelInsideIpVersion] = None,
    ) -> None:
        '''(experimental) THe properties for a S2S Ipsec Vpn Connection https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateVpnConnection.html.

        :param dpd_timeout_action: Default: CLEAR The action to take after DPD timeout occurs. Specify restart to restart the IKE initiation. Specify clear to end the IKE session.
        :param dpd_timeout_seconds: Default: 30 The number of seconds after which a DPD timeout occurs.
        :param enable_acceleration: (experimental) Indicate whether to enable acceleration for the VPN connection.
        :param enable_logging: (experimental) Enable CloudwatchLogging for the S2S VPN.
        :param ike_versions: (experimental) The IKE versions that are permitted for the VPN tunnel.
        :param local_ipv4_network_cidr: Default: 0.0.0.0/0 The IPv4 CIDR on the AWS side of the VPN connection.
        :param outside_ip_address_type: Default: PUBLIC The type of IPv4 address assigned to the outside interface of the customer gateway device.
        :param phase1_dh_group_numbers: (experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 1 IKE negotiations.
        :param phase1_encryption_algorithms: (experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.
        :param phase1_integrity_algorithms: (experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.
        :param phase1_lifetime_seconds: (experimental) The lifetime for phase 1 of the IKE negotiation, in seconds.
        :param phase2_dh_group_numbers: (experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 2 IKE negotiations.
        :param phase2_encryption_algorithms: (experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.
        :param phase2_integrity_algorithms: (experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.
        :param phase2_life_time_seconds: (experimental) The lifetime for phase 2 of the IKE negotiation, in seconds.
        :param rekey_fuzz_percentage: Default: 100 The percentage of the rekey window (determined by RekeyMarginTimeSeconds) during which the rekey time is randomly selected.
        :param rekey_margin_time_seconds: Default: 540 The margin time, in seconds, before the phase 2 lifetime expires, during which the AWS side of the VPN connection performs an IKE rekey. The exact time of the rekey is randomly selected based on the value for RekeyFuzzPercentage.
        :param remote_ipv4_network_cidr: Default: 0.0.0.0/0 The IPv4 CIDR on the Remote side of the VPN connection.
        :param replay_window_size: Default: 1024 The number of packets in an IKE replay window.
        :param startup_action: (experimental) The action to take when the establishing the tunnel for the VPN connection. By default, your customer gateway device must initiate the IKE negotiation and bring up the tunnel. Specify start for AWS to initiate the IKE negotiation.
        :param static_routes_only: (experimental) Indicate if this will only use Static Routes Only.
        :param tunnel_inside_ip_version: Default: IPV4 Indicate whether the VPN tunnels process IPv4 or IPv6 traffic.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20fe01279c7090c98e9384d9a1bdad1cfe307739f8647631932340862041790)
            check_type(argname="argument dpd_timeout_action", value=dpd_timeout_action, expected_type=type_hints["dpd_timeout_action"])
            check_type(argname="argument dpd_timeout_seconds", value=dpd_timeout_seconds, expected_type=type_hints["dpd_timeout_seconds"])
            check_type(argname="argument enable_acceleration", value=enable_acceleration, expected_type=type_hints["enable_acceleration"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument ike_versions", value=ike_versions, expected_type=type_hints["ike_versions"])
            check_type(argname="argument local_ipv4_network_cidr", value=local_ipv4_network_cidr, expected_type=type_hints["local_ipv4_network_cidr"])
            check_type(argname="argument outside_ip_address_type", value=outside_ip_address_type, expected_type=type_hints["outside_ip_address_type"])
            check_type(argname="argument phase1_dh_group_numbers", value=phase1_dh_group_numbers, expected_type=type_hints["phase1_dh_group_numbers"])
            check_type(argname="argument phase1_encryption_algorithms", value=phase1_encryption_algorithms, expected_type=type_hints["phase1_encryption_algorithms"])
            check_type(argname="argument phase1_integrity_algorithms", value=phase1_integrity_algorithms, expected_type=type_hints["phase1_integrity_algorithms"])
            check_type(argname="argument phase1_lifetime_seconds", value=phase1_lifetime_seconds, expected_type=type_hints["phase1_lifetime_seconds"])
            check_type(argname="argument phase2_dh_group_numbers", value=phase2_dh_group_numbers, expected_type=type_hints["phase2_dh_group_numbers"])
            check_type(argname="argument phase2_encryption_algorithms", value=phase2_encryption_algorithms, expected_type=type_hints["phase2_encryption_algorithms"])
            check_type(argname="argument phase2_integrity_algorithms", value=phase2_integrity_algorithms, expected_type=type_hints["phase2_integrity_algorithms"])
            check_type(argname="argument phase2_life_time_seconds", value=phase2_life_time_seconds, expected_type=type_hints["phase2_life_time_seconds"])
            check_type(argname="argument rekey_fuzz_percentage", value=rekey_fuzz_percentage, expected_type=type_hints["rekey_fuzz_percentage"])
            check_type(argname="argument rekey_margin_time_seconds", value=rekey_margin_time_seconds, expected_type=type_hints["rekey_margin_time_seconds"])
            check_type(argname="argument remote_ipv4_network_cidr", value=remote_ipv4_network_cidr, expected_type=type_hints["remote_ipv4_network_cidr"])
            check_type(argname="argument replay_window_size", value=replay_window_size, expected_type=type_hints["replay_window_size"])
            check_type(argname="argument startup_action", value=startup_action, expected_type=type_hints["startup_action"])
            check_type(argname="argument static_routes_only", value=static_routes_only, expected_type=type_hints["static_routes_only"])
            check_type(argname="argument tunnel_inside_ip_version", value=tunnel_inside_ip_version, expected_type=type_hints["tunnel_inside_ip_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dpd_timeout_action is not None:
            self._values["dpd_timeout_action"] = dpd_timeout_action
        if dpd_timeout_seconds is not None:
            self._values["dpd_timeout_seconds"] = dpd_timeout_seconds
        if enable_acceleration is not None:
            self._values["enable_acceleration"] = enable_acceleration
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if ike_versions is not None:
            self._values["ike_versions"] = ike_versions
        if local_ipv4_network_cidr is not None:
            self._values["local_ipv4_network_cidr"] = local_ipv4_network_cidr
        if outside_ip_address_type is not None:
            self._values["outside_ip_address_type"] = outside_ip_address_type
        if phase1_dh_group_numbers is not None:
            self._values["phase1_dh_group_numbers"] = phase1_dh_group_numbers
        if phase1_encryption_algorithms is not None:
            self._values["phase1_encryption_algorithms"] = phase1_encryption_algorithms
        if phase1_integrity_algorithms is not None:
            self._values["phase1_integrity_algorithms"] = phase1_integrity_algorithms
        if phase1_lifetime_seconds is not None:
            self._values["phase1_lifetime_seconds"] = phase1_lifetime_seconds
        if phase2_dh_group_numbers is not None:
            self._values["phase2_dh_group_numbers"] = phase2_dh_group_numbers
        if phase2_encryption_algorithms is not None:
            self._values["phase2_encryption_algorithms"] = phase2_encryption_algorithms
        if phase2_integrity_algorithms is not None:
            self._values["phase2_integrity_algorithms"] = phase2_integrity_algorithms
        if phase2_life_time_seconds is not None:
            self._values["phase2_life_time_seconds"] = phase2_life_time_seconds
        if rekey_fuzz_percentage is not None:
            self._values["rekey_fuzz_percentage"] = rekey_fuzz_percentage
        if rekey_margin_time_seconds is not None:
            self._values["rekey_margin_time_seconds"] = rekey_margin_time_seconds
        if remote_ipv4_network_cidr is not None:
            self._values["remote_ipv4_network_cidr"] = remote_ipv4_network_cidr
        if replay_window_size is not None:
            self._values["replay_window_size"] = replay_window_size
        if startup_action is not None:
            self._values["startup_action"] = startup_action
        if static_routes_only is not None:
            self._values["static_routes_only"] = static_routes_only
        if tunnel_inside_ip_version is not None:
            self._values["tunnel_inside_ip_version"] = tunnel_inside_ip_version

    @builtins.property
    def dpd_timeout_action(self) -> typing.Optional[DPDTimeoutAction]:
        '''
        :default: CLEAR The action to take after DPD timeout occurs. Specify restart to restart the IKE initiation. Specify clear to end the IKE session.

        :stability: experimental
        '''
        result = self._values.get("dpd_timeout_action")
        return typing.cast(typing.Optional[DPDTimeoutAction], result)

    @builtins.property
    def dpd_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 30 The number of seconds after which a DPD timeout occurs.

        :stability: experimental
        '''
        result = self._values.get("dpd_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_acceleration(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicate whether to enable acceleration for the VPN connection.

        :stability: experimental
        '''
        result = self._values.get("enable_acceleration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable CloudwatchLogging for the S2S VPN.

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ike_versions(self) -> typing.Optional[typing.List[IkeVersion]]:
        '''(experimental) The IKE versions that are permitted for the VPN tunnel.

        :stability: experimental
        '''
        result = self._values.get("ike_versions")
        return typing.cast(typing.Optional[typing.List[IkeVersion]], result)

    @builtins.property
    def local_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''
        :default: 0.0.0.0/0 The IPv4 CIDR on the AWS side of the VPN connection.

        :stability: experimental
        '''
        result = self._values.get("local_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outside_ip_address_type(self) -> typing.Optional[OutsideIpAddressType]:
        '''
        :default: PUBLIC The type of IPv4 address assigned to the outside interface of the customer gateway device.

        :stability: experimental
        '''
        result = self._values.get("outside_ip_address_type")
        return typing.cast(typing.Optional[OutsideIpAddressType], result)

    @builtins.property
    def phase1_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[Phase1DHGroupNumbers]]:
        '''(experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 1 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase1_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[Phase1DHGroupNumbers]], result)

    @builtins.property
    def phase1_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase1EncryptionAlgorithms]]:
        '''(experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase1_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase1EncryptionAlgorithms]], result)

    @builtins.property
    def phase1_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase1IntegrityAlgorithms]]:
        '''(experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 1 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase1_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase1IntegrityAlgorithms]], result)

    @builtins.property
    def phase1_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The lifetime for phase 1 of the IKE negotiation, in seconds.

        :stability: experimental
        '''
        result = self._values.get("phase1_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def phase2_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[Phase2DHGroupNumbers]]:
        '''(experimental) One or more Diffie-Hellman group numbers that are permitted for the VPN tunnel for phase 2 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase2_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[Phase2DHGroupNumbers]], result)

    @builtins.property
    def phase2_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase2EncryptionAlgorithms]]:
        '''(experimental) One or more encryption algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase2_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase2EncryptionAlgorithms]], result)

    @builtins.property
    def phase2_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[Phase2IntegrityAlgorithms]]:
        '''(experimental) One or more integrity algorithms that are permitted for the VPN tunnel for phase 2 IKE negotiations.

        :stability: experimental
        '''
        result = self._values.get("phase2_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[Phase2IntegrityAlgorithms]], result)

    @builtins.property
    def phase2_life_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The lifetime for phase 2 of the IKE negotiation, in seconds.

        :stability: experimental
        '''
        result = self._values.get("phase2_life_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rekey_fuzz_percentage(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 100 The percentage of the rekey window (determined by RekeyMarginTimeSeconds) during which the rekey time is randomly selected.

        :stability: experimental
        '''
        result = self._values.get("rekey_fuzz_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rekey_margin_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 540 The margin time, in seconds, before the phase 2 lifetime expires, during which the AWS side of the VPN connection performs an IKE rekey. The exact time of the rekey is randomly selected based on the value for RekeyFuzzPercentage.

        :stability: experimental
        '''
        result = self._values.get("rekey_margin_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def remote_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''
        :default: 0.0.0.0/0 The IPv4 CIDR on the Remote side of the VPN connection.

        :stability: experimental
        '''
        result = self._values.get("remote_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replay_window_size(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 1024 The number of packets in an IKE replay window.

        :stability: experimental
        '''
        result = self._values.get("replay_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def startup_action(self) -> typing.Optional[StartupAction]:
        '''(experimental) The action to take when the establishing the tunnel for the VPN connection.

        By default, your customer gateway device must initiate the IKE negotiation and bring up the tunnel. Specify start for AWS to initiate the IKE negotiation.

        :stability: experimental
        '''
        result = self._values.get("startup_action")
        return typing.cast(typing.Optional[StartupAction], result)

    @builtins.property
    def static_routes_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''(experimental) Indicate if this will only use Static Routes Only.

        :stability: experimental
        '''
        result = self._values.get("static_routes_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tunnel_inside_ip_version(self) -> typing.Optional[TunnelInsideIpVersion]:
        '''
        :default: IPV4 Indicate whether the VPN tunnels process IPv4 or IPv6 traffic.

        :stability: experimental
        '''
        result = self._values.get("tunnel_inside_ip_version")
        return typing.cast(typing.Optional[TunnelInsideIpVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSpecProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AssociationMethod",
    "AttachmentCondition",
    "AttachmentConditions",
    "AttachmentPolicy",
    "AttachmentPolicyAction",
    "CloudWanTGW",
    "ConditionLogic",
    "CoreNetwork",
    "CoreNetworkProps",
    "CoreNetworkSegment",
    "CoreNetworkShare",
    "DPDTimeoutAction",
    "ICoreNetworkSegmentProps",
    "IkeVersion",
    "Operators",
    "OutsideIpAddressType",
    "Phase1DHGroupNumbers",
    "Phase1EncryptionAlgorithms",
    "Phase1IntegrityAlgorithms",
    "Phase2DHGroupNumbers",
    "Phase2EncryptionAlgorithms",
    "Phase2IntegrityAlgorithms",
    "SampleConfig",
    "Segment",
    "SegmentAction",
    "SegmentActionMode",
    "SegmentActionType",
    "SimpleAttachmentPolicyProps",
    "SimpleShareActionProps",
    "StartupAction",
    "TGWOnCloudWanProps",
    "TunnelInsideIpVersion",
    "VpnDeviceType",
    "VpnProps",
    "VpnSpecProps",
]

publication.publish()

def _typecheckingstub__d4beff5203da213443685a48d253748a9c022d955e2475720248d46b97670a2c(
    *,
    type: AttachmentCondition,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[Operators] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9081d338d1d0edb38ac67eac3098aa2a1ffd03df9ed61c01d33d85548571f14d(
    *,
    action: typing.Union[AttachmentPolicyAction, typing.Dict[builtins.str, typing.Any]],
    conditions: typing.Sequence[typing.Union[AttachmentConditions, typing.Dict[builtins.str, typing.Any]]],
    rule_number: jsii.Number,
    condition_logic: typing.Optional[ConditionLogic] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea1ad6cb3aed5c2680d1220d689553eb05f291855bdf174af38f4b147546136(
    *,
    association_method: AssociationMethod,
    require_acceptance: typing.Optional[builtins.bool] = None,
    segment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f088616079545eb5c85f7f5348ae8a37cfae40e5d257585f3447604e6e6bb88(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    amazon_side_asn: builtins.str,
    attachment_segment: builtins.str,
    cloudwan: CoreNetwork,
    description: builtins.str,
    cloud_wan_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_route_in_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
    tg_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8b12d488dfd2a0bef1616d73d367833cf27a988fae47a9d9ea9e531127144b(
    dxgatewayname: builtins.str,
    dxgateway_asn: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa00cea3e9e0c8f0c517493e94994a623b0b7b1b974fc2f7b1080b6892865dcf(
    name: builtins.str,
    *,
    customer_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway,
    vpnspec: typing.Union[VpnSpecProps, typing.Dict[builtins.str, typing.Any]],
    sampleconfig: typing.Optional[typing.Union[SampleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel_inside_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel_ipam_pool: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acf08598e3495fd74d7d3fd57e44c3feff6c17c6c5e27d76d23e7e3589e00b3(
    dxgateway_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917364e1186de60c98928a7de3ab729bb5ba02360e2dcb92f866a1ed5a0412f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8250cec8cd004488eac92d55d75c032d1e94e61a673900ec0d4ff6290084d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    asn_ranges: typing.Sequence[builtins.str],
    core_name: builtins.str,
    edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
    global_network: _aws_cdk_aws_networkmanager_ceddda9d.CfnGlobalNetwork,
    policy_description: builtins.str,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    non_production: typing.Optional[builtins.bool] = None,
    vpn_ecmp_support: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcaa1146649d1f5abb59b9631529005c656d53c854544c24210f21a3bb22d866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b2cef97b467b8a6370abe89945b8981aff04b5dc665b0d41743a27f6b00f2c(
    *,
    asn_ranges: typing.Sequence[builtins.str],
    core_name: builtins.str,
    edge_locations: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
    global_network: _aws_cdk_aws_networkmanager_ceddda9d.CfnGlobalNetwork,
    policy_description: builtins.str,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    non_production: typing.Optional[builtins.bool] = None,
    vpn_ecmp_support: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e636aa958d739f110f0ce9e0f2dfb17403e7943eef65b42f96d6ad04d1df3c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: ICoreNetworkSegmentProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea13880429af47628b9623d3416319ee10b8f03b3e8e172a1bcb58527e646823(
    *,
    allow_external_principals: builtins.bool,
    principals: typing.Sequence[builtins.str],
    tags: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Tag]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488bf3c7b78a130f30d96088a385ce8de9310cb01454bed905d75754bb6916a6(
    value: typing.List[_aws_cdk_ceddda9d.CustomResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e503ce117878a6ecf8e86a5387df98a3d1502c673e4d15479c1cdb452b8716(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
    device_type: VpnDeviceType,
    ike_version: IkeVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcb5f1d0b8744c99bc2a045d812e86c0f2767e7cd773708599ef86d44bb43b2(
    *,
    name: builtins.str,
    allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_locations: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
    isolate_attachments: typing.Optional[builtins.bool] = None,
    require_attachment_acceptance: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720366174a28eb004e18a318e026f7bf9f0155fdcbb1578cf556d2e99e6e223e(
    *,
    action: SegmentActionType,
    description: builtins.str,
    destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    except_: typing.Optional[typing.Sequence[builtins.str]] = None,
    mode: typing.Optional[SegmentActionMode] = None,
    share_with: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da580b31887123ae34275387881d6d816d7810ae88abcbf178fd857d8516ba6f(
    *,
    rule_number: jsii.Number,
    account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174af254cd37ae306f53afd67b72c4b201b03ea33b4bd49c683ccbe6f47ab408(
    *,
    description: builtins.str,
    share_with: typing.Union[builtins.str, typing.Sequence[CoreNetworkSegment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d3cde16b7525c7c6384f3dcc12c540179962f2c2c2587b823c61752ef41951(
    *,
    amazon_side_asn: builtins.str,
    attachment_segment: builtins.str,
    cloudwan: CoreNetwork,
    description: builtins.str,
    cloud_wan_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_route_in_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
    tg_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3175b7d39afa1ff45148015ff62f7471e9d0b33322ee8677b01d33b7c059732(
    *,
    customer_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway,
    vpnspec: typing.Union[VpnSpecProps, typing.Dict[builtins.str, typing.Any]],
    sampleconfig: typing.Optional[typing.Union[SampleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel_inside_cidr: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel_ipam_pool: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20fe01279c7090c98e9384d9a1bdad1cfe307739f8647631932340862041790(
    *,
    dpd_timeout_action: typing.Optional[DPDTimeoutAction] = None,
    dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    enable_acceleration: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    ike_versions: typing.Optional[typing.Sequence[IkeVersion]] = None,
    local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    outside_ip_address_type: typing.Optional[OutsideIpAddressType] = None,
    phase1_dh_group_numbers: typing.Optional[typing.Sequence[Phase1DHGroupNumbers]] = None,
    phase1_encryption_algorithms: typing.Optional[typing.Sequence[Phase1EncryptionAlgorithms]] = None,
    phase1_integrity_algorithms: typing.Optional[typing.Sequence[Phase1IntegrityAlgorithms]] = None,
    phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    phase2_dh_group_numbers: typing.Optional[typing.Sequence[Phase2DHGroupNumbers]] = None,
    phase2_encryption_algorithms: typing.Optional[typing.Sequence[Phase2EncryptionAlgorithms]] = None,
    phase2_integrity_algorithms: typing.Optional[typing.Sequence[Phase2IntegrityAlgorithms]] = None,
    phase2_life_time_seconds: typing.Optional[jsii.Number] = None,
    rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    replay_window_size: typing.Optional[jsii.Number] = None,
    startup_action: typing.Optional[StartupAction] = None,
    static_routes_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tunnel_inside_ip_version: typing.Optional[TunnelInsideIpVersion] = None,
) -> None:
    """Type checking stubs"""
    pass
