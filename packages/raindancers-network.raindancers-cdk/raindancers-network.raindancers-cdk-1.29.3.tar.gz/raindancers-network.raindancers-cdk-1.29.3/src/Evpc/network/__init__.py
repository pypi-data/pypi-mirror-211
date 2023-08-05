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
import aws_cdk.aws_networkfirewall as _aws_cdk_aws_networkfirewall_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8
from ..dns import (
    HubVpc as _HubVpc_f33ed7e6,
    OutboundForwardingRule as _OutboundForwardingRule_a6d0cb0c,
    R53Resolverendpoints as _R53Resolverendpoints_5d3b063e,
)


@jsii.data_type(
    jsii_type="raindancers-network.network.AddAwsServiceEndPointsProps",
    jsii_struct_bases=[],
    name_mapping={
        "services": "services",
        "subnet_group": "subnetGroup",
        "dynamo_db_gateway": "dynamoDbGateway",
        "s3_gateway_interface": "s3GatewayInterface",
    },
)
class AddAwsServiceEndPointsProps:
    def __init__(
        self,
        *,
        services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
        subnet_group: "SubnetGroup",
        dynamo_db_gateway: typing.Optional[builtins.bool] = None,
        s3_gateway_interface: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param services: 
        :param subnet_group: 
        :param dynamo_db_gateway: 
        :param s3_gateway_interface: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3d871d7a3d34269b14ecf698271c72a9e7ce024ad1cfd130b46ef122eac944)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument dynamo_db_gateway", value=dynamo_db_gateway, expected_type=type_hints["dynamo_db_gateway"])
            check_type(argname="argument s3_gateway_interface", value=s3_gateway_interface, expected_type=type_hints["s3_gateway_interface"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "services": services,
            "subnet_group": subnet_group,
        }
        if dynamo_db_gateway is not None:
            self._values["dynamo_db_gateway"] = dynamo_db_gateway
        if s3_gateway_interface is not None:
            self._values["s3_gateway_interface"] = s3_gateway_interface

    @builtins.property
    def services(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService]:
        '''
        :stability: experimental
        '''
        result = self._values.get("services")
        assert result is not None, "Required property 'services' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService], result)

    @builtins.property
    def subnet_group(self) -> "SubnetGroup":
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast("SubnetGroup", result)

    @builtins.property
    def dynamo_db_gateway(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("dynamo_db_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def s3_gateway_interface(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("s3_gateway_interface")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddAwsServiceEndPointsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.AddCoreRoutesProps",
    jsii_struct_bases=[],
    name_mapping={
        "attachment_id": "attachmentId",
        "core_name": "coreName",
        "description": "description",
        "destination_cidr_blocks": "destinationCidrBlocks",
        "policy_table_arn": "policyTableArn",
        "segments": "segments",
    },
)
class AddCoreRoutesProps:
    def __init__(
        self,
        *,
        attachment_id: builtins.str,
        core_name: builtins.str,
        description: builtins.str,
        destination_cidr_blocks: typing.Sequence[builtins.str],
        policy_table_arn: builtins.str,
        segments: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attachment_id: 
        :param core_name: 
        :param description: 
        :param destination_cidr_blocks: 
        :param policy_table_arn: 
        :param segments: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe781b9a5afbd9cbd3eb283c2a155d0c6fa2fc8f058fac471750ebd8e16fa41)
            check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
            check_type(argname="argument core_name", value=core_name, expected_type=type_hints["core_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_cidr_blocks", value=destination_cidr_blocks, expected_type=type_hints["destination_cidr_blocks"])
            check_type(argname="argument policy_table_arn", value=policy_table_arn, expected_type=type_hints["policy_table_arn"])
            check_type(argname="argument segments", value=segments, expected_type=type_hints["segments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attachment_id": attachment_id,
            "core_name": core_name,
            "description": description,
            "destination_cidr_blocks": destination_cidr_blocks,
            "policy_table_arn": policy_table_arn,
            "segments": segments,
        }

    @builtins.property
    def attachment_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_id")
        assert result is not None, "Required property 'attachment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def core_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("core_name")
        assert result is not None, "Required property 'core_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_cidr_blocks(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination_cidr_blocks")
        assert result is not None, "Required property 'destination_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def policy_table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("policy_table_arn")
        assert result is not None, "Required property 'policy_table_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def segments(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("segments")
        assert result is not None, "Required property 'segments' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddCoreRoutesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.AddEnterprizeZoneProps",
    jsii_struct_bases=[],
    name_mapping={
        "domainname": "domainname",
        "hub_vpcs": "hubVpcs",
        "is_hub_vpc": "isHubVpc",
    },
)
class AddEnterprizeZoneProps:
    def __init__(
        self,
        *,
        domainname: builtins.str,
        hub_vpcs: typing.Sequence[typing.Union[_HubVpc_f33ed7e6, typing.Dict[builtins.str, typing.Any]]],
        is_hub_vpc: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domainname: 
        :param hub_vpcs: 
        :param is_hub_vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be8aa3bf69e127ac8e18750deed08580355b3b98e66808099c26b5fe42b735a)
            check_type(argname="argument domainname", value=domainname, expected_type=type_hints["domainname"])
            check_type(argname="argument hub_vpcs", value=hub_vpcs, expected_type=type_hints["hub_vpcs"])
            check_type(argname="argument is_hub_vpc", value=is_hub_vpc, expected_type=type_hints["is_hub_vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domainname": domainname,
            "hub_vpcs": hub_vpcs,
        }
        if is_hub_vpc is not None:
            self._values["is_hub_vpc"] = is_hub_vpc

    @builtins.property
    def domainname(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("domainname")
        assert result is not None, "Required property 'domainname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hub_vpcs(self) -> typing.List[_HubVpc_f33ed7e6]:
        '''
        :stability: experimental
        '''
        result = self._values.get("hub_vpcs")
        assert result is not None, "Required property 'hub_vpcs' is missing"
        return typing.cast(typing.List[_HubVpc_f33ed7e6], result)

    @builtins.property
    def is_hub_vpc(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("is_hub_vpc")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddEnterprizeZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.AddR53ZoneProps",
    jsii_struct_bases=[],
    name_mapping={"zone": "zone", "central_vpc": "centralVpc"},
)
class AddR53ZoneProps:
    def __init__(
        self,
        *,
        zone: builtins.str,
        central_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc] = None,
    ) -> None:
        '''
        :param zone: 
        :param central_vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2edde8cbf8bdb1e42676cf48c6225d58e8c220128c31d8408e26f4fd622a3cf)
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument central_vpc", value=central_vpc, expected_type=type_hints["central_vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "zone": zone,
        }
        if central_vpc is not None:
            self._values["central_vpc"] = central_vpc

    @builtins.property
    def zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def central_vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("central_vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddR53ZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.AddRoutesProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "description": "description",
        "destination": "destination",
        "subnet_groups": "subnetGroups",
        "cloudwan_name": "cloudwanName",
        "network_firewall_arn": "networkFirewallArn",
    },
)
class AddRoutesProps:
    def __init__(
        self,
        *,
        cidr: typing.Sequence[builtins.str],
        description: builtins.str,
        destination: "Destination",
        subnet_groups: typing.Sequence[builtins.str],
        cloudwan_name: typing.Optional[builtins.str] = None,
        network_firewall_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Propertys for Adding Routes in VPC.

        :param cidr: 
        :param description: 
        :param destination: 
        :param subnet_groups: 
        :param cloudwan_name: 
        :param network_firewall_arn: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956d15f36f571d23526ddfa187efe9f7033d2ef4872d9ffdf8e7d89ba7f3001a)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument subnet_groups", value=subnet_groups, expected_type=type_hints["subnet_groups"])
            check_type(argname="argument cloudwan_name", value=cloudwan_name, expected_type=type_hints["cloudwan_name"])
            check_type(argname="argument network_firewall_arn", value=network_firewall_arn, expected_type=type_hints["network_firewall_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "description": description,
            "destination": destination,
            "subnet_groups": subnet_groups,
        }
        if cloudwan_name is not None:
            self._values["cloudwan_name"] = cloudwan_name
        if network_firewall_arn is not None:
            self._values["network_firewall_arn"] = network_firewall_arn

    @builtins.property
    def cidr(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> "Destination":
        '''
        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("Destination", result)

    @builtins.property
    def subnet_groups(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        assert result is not None, "Required property 'subnet_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloudwan_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloudwan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_firewall_arn(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("network_firewall_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRoutesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.network.ApplianceMode")
class ApplianceMode(enum.Enum):
    '''(experimental) Propertys for Appliance Mode.

    :stability: experimental
    '''

    ENABLED = "ENABLED"
    '''(experimental) enable Connecting VPC to TransitGateway in Appliance Mode.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.network.AttachToCloudWanProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_name": "coreNetworkName",
        "segment_name": "segmentName",
        "appliance_mode": "applianceMode",
        "attachment_subnet_group": "attachmentSubnetGroup",
    },
)
class AttachToCloudWanProps:
    def __init__(
        self,
        *,
        core_network_name: builtins.str,
        segment_name: builtins.str,
        appliance_mode: typing.Optional[builtins.bool] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Propertys for Attaching to a Cloudwan Core Network.

        :param core_network_name: (experimental) corenetworkName.
        :param segment_name: 
        :param appliance_mode: 
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d14da943ad99aff58715a46c233ed344e3ed682a856dae617fd06e857dd3da7)
            check_type(argname="argument core_network_name", value=core_network_name, expected_type=type_hints["core_network_name"])
            check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
            check_type(argname="argument appliance_mode", value=appliance_mode, expected_type=type_hints["appliance_mode"])
            check_type(argname="argument attachment_subnet_group", value=attachment_subnet_group, expected_type=type_hints["attachment_subnet_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "core_network_name": core_network_name,
            "segment_name": segment_name,
        }
        if appliance_mode is not None:
            self._values["appliance_mode"] = appliance_mode
        if attachment_subnet_group is not None:
            self._values["attachment_subnet_group"] = attachment_subnet_group

    @builtins.property
    def core_network_name(self) -> builtins.str:
        '''(experimental) corenetworkName.

        :stability: experimental
        '''
        result = self._values.get("core_network_name")
        assert result is not None, "Required property 'core_network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def segment_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("segment_name")
        assert result is not None, "Required property 'segment_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def appliance_mode(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("appliance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def attachment_subnet_group(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_subnet_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachToCloudWanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.AttachToTransitGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "transit_gateway": "transitGateway",
        "applicance_mode": "applicanceMode",
        "attachment_subnet_group": "attachmentSubnetGroup",
    },
)
class AttachToTransitGatewayProps:
    def __init__(
        self,
        *,
        transit_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway,
        applicance_mode: typing.Optional[ApplianceMode] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Propertys to attach the Vpc To Transit Gateway.

        :param transit_gateway: (experimental) the TransitGateway to connect to.
        :param applicance_mode: (experimental) Will this be connected in appliance mode ( used if you have Network Firewalls ).
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cab874cb1ee5844e2300e3fc9a5501a89fd8cececd7db3ee9c9befc96c2f39f)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument applicance_mode", value=applicance_mode, expected_type=type_hints["applicance_mode"])
            check_type(argname="argument attachment_subnet_group", value=attachment_subnet_group, expected_type=type_hints["attachment_subnet_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway": transit_gateway,
        }
        if applicance_mode is not None:
            self._values["applicance_mode"] = applicance_mode
        if attachment_subnet_group is not None:
            self._values["attachment_subnet_group"] = attachment_subnet_group

    @builtins.property
    def transit_gateway(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway:
        '''(experimental) the TransitGateway to connect to.

        :stability: experimental
        '''
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway, result)

    @builtins.property
    def applicance_mode(self) -> typing.Optional[ApplianceMode]:
        '''(experimental) Will this be connected in appliance mode ( used if you have Network Firewalls ).

        :stability: experimental
        '''
        result = self._values.get("applicance_mode")
        return typing.cast(typing.Optional[ApplianceMode], result)

    @builtins.property
    def attachment_subnet_group(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("attachment_subnet_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachToTransitGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.CloudWanRoutingProtocolProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_groups": "subnetGroups",
        "accept_route_filter": "acceptRouteFilter",
        "deny_route_filter": "denyRouteFilter",
    },
)
class CloudWanRoutingProtocolProps:
    def __init__(
        self,
        *,
        subnet_groups: typing.Sequence[builtins.str],
        accept_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_groups: 
        :param accept_route_filter: 
        :param deny_route_filter: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0db49e994c0a98983684f628c9ad2922224075c0fbd5b61bdd2e16996f36458)
            check_type(argname="argument subnet_groups", value=subnet_groups, expected_type=type_hints["subnet_groups"])
            check_type(argname="argument accept_route_filter", value=accept_route_filter, expected_type=type_hints["accept_route_filter"])
            check_type(argname="argument deny_route_filter", value=deny_route_filter, expected_type=type_hints["deny_route_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_groups": subnet_groups,
        }
        if accept_route_filter is not None:
            self._values["accept_route_filter"] = accept_route_filter
        if deny_route_filter is not None:
            self._values["deny_route_filter"] = deny_route_filter

    @builtins.property
    def subnet_groups(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        assert result is not None, "Required property 'subnet_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def accept_route_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("accept_route_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny_route_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deny_route_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWanRoutingProtocolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.network.Destination")
class Destination(enum.Enum):
    '''(experimental) The Destinations for Adding Routes.

    :stability: experimental
    '''

    CLOUDWAN = "CLOUDWAN"
    '''(experimental) route to the cloudwan that the vpc is attached to.

    :stability: experimental
    '''
    TRANSITGATEWAY = "TRANSITGATEWAY"
    '''(experimental) route to the transitGateway that the vpc is attached to.

    :stability: experimental
    '''
    NWFIREWALL = "NWFIREWALL"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.network.ESubnetGroup",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_mask": "cidrMask",
        "name": "name",
        "subnet_type": "subnetType",
    },
)
class ESubnetGroup:
    def __init__(
        self,
        *,
        cidr_mask: jsii.Number,
        name: builtins.str,
        subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
    ) -> None:
        '''
        :param cidr_mask: 
        :param name: 
        :param subnet_type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66bc48a5c59cb727347d874191c2cdafd8fb0f400c361e88bdaac0ab58e9bd2)
            check_type(argname="argument cidr_mask", value=cidr_mask, expected_type=type_hints["cidr_mask"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_type", value=subnet_type, expected_type=type_hints["subnet_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_mask": cidr_mask,
            "name": name,
            "subnet_type": subnet_type,
        }

    @builtins.property
    def cidr_mask(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("cidr_mask")
        assert result is not None, "Required property 'cidr_mask' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_type")
        assert result is not None, "Required property 'subnet_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ESubnetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.ESubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_mask": "cidrMask",
        "name": "name",
        "subnet_type": "subnetType",
    },
)
class ESubnetGroupProps:
    def __init__(
        self,
        *,
        cidr_mask: jsii.Number,
        name: builtins.str,
        subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
    ) -> None:
        '''
        :param cidr_mask: 
        :param name: 
        :param subnet_type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233a2cc463688abf925c28cf81d573ef1990683283b8cfb18f61113d104e8934)
            check_type(argname="argument cidr_mask", value=cidr_mask, expected_type=type_hints["cidr_mask"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_type", value=subnet_type, expected_type=type_hints["subnet_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_mask": cidr_mask,
            "name": name,
            "subnet_type": subnet_type,
        }

    @builtins.property
    def cidr_mask(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("cidr_mask")
        assert result is not None, "Required property 'cidr_mask' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_type")
        assert result is not None, "Required property 'subnet_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ESubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpc(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.network.EnterpriseVpc",
):
    '''(experimental) Enteprise VPC's take the stock ec2.Vpc and provide numerous convience methods primarly related to connecting to internal networks.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        evpc: typing.Optional[typing.Union["EvpcProps", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param evpc: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7824f738e0341f5f59379d8b0e09dbac312a796352b0a37fab71ad9a75526bb6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnterpriseVpcProps(evpc=evpc, vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addCentralResolverRules")
    def add_central_resolver_rules(
        self,
        domains: typing.Sequence[builtins.str],
        search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param domains: -
        :param search_tag: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e85c0d88596b9b5b0002423ab7ee5bea9376c71e0417447f4eb31aebcd6a1e)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument search_tag", value=search_tag, expected_type=type_hints["search_tag"])
        return typing.cast(None, jsii.invoke(self, "addCentralResolverRules", [domains, search_tag]))

    @jsii.member(jsii_name="addConditionalFowardingRules")
    def add_conditional_fowarding_rules(
        self,
        forwarding_rules: typing.Sequence[typing.Union[_OutboundForwardingRule_a6d0cb0c, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param forwarding_rules: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb7fb9484ab77ad1c99ec06db745aee4a2d43d54a858f55bb310fbf21076ecf)
            check_type(argname="argument forwarding_rules", value=forwarding_rules, expected_type=type_hints["forwarding_rules"])
        return typing.cast(None, jsii.invoke(self, "addConditionalFowardingRules", [forwarding_rules]))

    @jsii.member(jsii_name="addCoreRoutes")
    def add_core_routes(
        self,
        *,
        attachment_id: builtins.str,
        core_name: builtins.str,
        description: builtins.str,
        destination_cidr_blocks: typing.Sequence[builtins.str],
        policy_table_arn: builtins.str,
        segments: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attachment_id: 
        :param core_name: 
        :param description: 
        :param destination_cidr_blocks: 
        :param policy_table_arn: 
        :param segments: 

        :stability: experimental
        '''
        props = AddCoreRoutesProps(
            attachment_id=attachment_id,
            core_name=core_name,
            description=description,
            destination_cidr_blocks=destination_cidr_blocks,
            policy_table_arn=policy_table_arn,
            segments=segments,
        )

        return typing.cast(None, jsii.invoke(self, "addCoreRoutes", [props]))

    @jsii.member(jsii_name="addCrossAccountR53AssociationRole")
    def add_cross_account_r53_association_role(
        self,
        rolename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rolename: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729a7b9f9fea1efe93ee55ffe575d1b4b9fc730cde62198c1abaf530b6fcd5bd)
            check_type(argname="argument rolename", value=rolename, expected_type=type_hints["rolename"])
        return typing.cast(None, jsii.invoke(self, "addCrossAccountR53AssociationRole", [rolename]))

    @jsii.member(jsii_name="addNetworkFirewall")
    def add_network_firewall(
        self,
        firewall_name: builtins.str,
        firewall_policy: _aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy,
        subnet: "SubnetGroup",
    ) -> None:
        '''
        :param firewall_name: -
        :param firewall_policy: -
        :param subnet: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a7366a3c0ccc32921eff015ae01d1ec3d9e2f80d238071c4c5306c3052e354)
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument firewall_policy", value=firewall_policy, expected_type=type_hints["firewall_policy"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(None, jsii.invoke(self, "addNetworkFirewall", [firewall_name, firewall_policy, subnet]))

    @jsii.member(jsii_name="addPrivateHostedZone")
    def add_private_hosted_zone(
        self,
        zonename: builtins.str,
    ) -> _aws_cdk_aws_route53_ceddda9d.HostedZone:
        '''
        :param zonename: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4e5400634be40939a319974a19264c5e947d8d1dd279b75358fe5e4a13258e)
            check_type(argname="argument zonename", value=zonename, expected_type=type_hints["zonename"])
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.HostedZone, jsii.invoke(self, "addPrivateHostedZone", [zonename]))

    @jsii.member(jsii_name="addR53Resolvers")
    def add_r53_resolvers(
        self,
        subnet: "SubnetGroup",
    ) -> _R53Resolverendpoints_5d3b063e:
        '''
        :param subnet: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b86fd69f20f6c1a45edefb0b52b3d176011a0a373dc2e57ef1f59dab0f7ee72)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(_R53Resolverendpoints_5d3b063e, jsii.invoke(self, "addR53Resolvers", [subnet]))

    @jsii.member(jsii_name="addR53Zone")
    def add_r53_zone(
        self,
        *,
        zone: builtins.str,
        central_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc] = None,
    ) -> None:
        '''
        :param zone: 
        :param central_vpc: 

        :stability: experimental
        '''
        props = AddR53ZoneProps(zone=zone, central_vpc=central_vpc)

        return typing.cast(None, jsii.invoke(self, "addR53Zone", [props]))

    @jsii.member(jsii_name="addRoutes")
    def add_routes(
        self,
        *,
        cidr: typing.Sequence[builtins.str],
        description: builtins.str,
        destination: Destination,
        subnet_groups: typing.Sequence[builtins.str],
        cloudwan_name: typing.Optional[builtins.str] = None,
        network_firewall_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add routes to SubnetGroups ( by implication their routing tables ).

        :param cidr: 
        :param description: 
        :param destination: 
        :param subnet_groups: 
        :param cloudwan_name: 
        :param network_firewall_arn: 

        :stability: experimental
        '''
        props = AddRoutesProps(
            cidr=cidr,
            description=description,
            destination=destination,
            subnet_groups=subnet_groups,
            cloudwan_name=cloudwan_name,
            network_firewall_arn=network_firewall_arn,
        )

        return typing.cast(None, jsii.invoke(self, "addRoutes", [props]))

    @jsii.member(jsii_name="addServiceEndpoints")
    def add_service_endpoints(
        self,
        *,
        services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
        subnet_group: "SubnetGroup",
        dynamo_db_gateway: typing.Optional[builtins.bool] = None,
        s3_gateway_interface: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Add a collection of service endpopints to the VPC.

        :param services: 
        :param subnet_group: 
        :param dynamo_db_gateway: 
        :param s3_gateway_interface: 

        :stability: experimental
        '''
        props = AddAwsServiceEndPointsProps(
            services=services,
            subnet_group=subnet_group,
            dynamo_db_gateway=dynamo_db_gateway,
            s3_gateway_interface=s3_gateway_interface,
        )

        return typing.cast(None, jsii.invoke(self, "addServiceEndpoints", [props]))

    @jsii.member(jsii_name="associateSharedResolverRules")
    def associate_shared_resolver_rules(
        self,
        domain_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param domain_names: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d84ae63ffa0860bf6396107b287070d21498898593e9fbb04aef32d20951dba)
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
        return typing.cast(None, jsii.invoke(self, "associateSharedResolverRules", [domain_names]))

    @jsii.member(jsii_name="attachAWSManagedDNSFirewallRules")
    def attach_aws_managed_dns_firewall_rules(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "attachAWSManagedDNSFirewallRules", []))

    @jsii.member(jsii_name="attachToCloudWan")
    def attach_to_cloud_wan(
        self,
        *,
        core_network_name: builtins.str,
        segment_name: builtins.str,
        appliance_mode: typing.Optional[builtins.bool] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) attachToCloudWan will attach a VPC to CloudWan, in a particular Segment.

        :param core_network_name: (experimental) corenetworkName.
        :param segment_name: 
        :param appliance_mode: 
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        props = AttachToCloudWanProps(
            core_network_name=core_network_name,
            segment_name=segment_name,
            appliance_mode=appliance_mode,
            attachment_subnet_group=attachment_subnet_group,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "attachToCloudWan", [props]))

    @jsii.member(jsii_name="attachToTransitGateway")
    def attach_to_transit_gateway(
        self,
        *,
        transit_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway,
        applicance_mode: typing.Optional[ApplianceMode] = None,
        attachment_subnet_group: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Attach a vpc to a transit gateway, possibly in appliance mode Its intended purpose is provide a.

        :param transit_gateway: (experimental) the TransitGateway to connect to.
        :param applicance_mode: (experimental) Will this be connected in appliance mode ( used if you have Network Firewalls ).
        :param attachment_subnet_group: 

        :stability: experimental
        '''
        props = AttachToTransitGatewayProps(
            transit_gateway=transit_gateway,
            applicance_mode=applicance_mode,
            attachment_subnet_group=attachment_subnet_group,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "attachToTransitGateway", [props]))

    @jsii.member(jsii_name="cloudWanRoutingProtocol")
    def cloud_wan_routing_protocol(
        self,
        *,
        subnet_groups: typing.Sequence[builtins.str],
        accept_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Enable CloudWanRoutingProtocol.

        :param subnet_groups: 
        :param accept_route_filter: 
        :param deny_route_filter: 

        :stability: experimental
        '''
        props = CloudWanRoutingProtocolProps(
            subnet_groups=subnet_groups,
            accept_route_filter=accept_route_filter,
            deny_route_filter=deny_route_filter,
        )

        return typing.cast(None, jsii.invoke(self, "cloudWanRoutingProtocol", [props]))

    @jsii.member(jsii_name="createAndAttachR53EnterprizeZone")
    def create_and_attach_r53_enterprize_zone(
        self,
        *,
        domainname: builtins.str,
        hub_vpcs: typing.Sequence[typing.Union[_HubVpc_f33ed7e6, typing.Dict[builtins.str, typing.Any]]],
        is_hub_vpc: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_route53_ceddda9d.PrivateHostedZone:
        '''
        :param domainname: 
        :param hub_vpcs: 
        :param is_hub_vpc: 

        :stability: experimental
        '''
        props = AddEnterprizeZoneProps(
            domainname=domainname, hub_vpcs=hub_vpcs, is_hub_vpc=is_hub_vpc
        )

        return typing.cast(_aws_cdk_aws_route53_ceddda9d.PrivateHostedZone, jsii.invoke(self, "createAndAttachR53EnterprizeZone", [props]))

    @jsii.member(jsii_name="createAndAttachR53PrivateZone")
    def create_and_attach_r53_private_zone(
        self,
        zone_name: builtins.str,
    ) -> _aws_cdk_aws_route53_ceddda9d.PrivateHostedZone:
        '''
        :param zone_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a4f8e336f8adf81160fcf70b4cdc7f1b8e54f9e9a3ccdb5fa9242f6cc9f896)
            check_type(argname="argument zone_name", value=zone_name, expected_type=type_hints["zone_name"])
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.PrivateHostedZone, jsii.invoke(self, "createAndAttachR53PrivateZone", [zone_name]))

    @jsii.member(jsii_name="createAndShareSubnetPrefixList")
    def create_and_share_subnet_prefix_list(
        self,
        name: builtins.str,
        subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        org_arn: builtins.str,
    ) -> _aws_cdk_aws_ec2_ceddda9d.CfnPrefixList:
        '''
        :param name: -
        :param subnets: -
        :param org_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c62bec98a484dd918c8fe08ceae85a9bdcc834cc9488f18fe5bc502c0c8be95)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument org_arn", value=org_arn, expected_type=type_hints["org_arn"])
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnPrefixList, jsii.invoke(self, "createAndShareSubnetPrefixList", [name, subnets, org_arn]))

    @jsii.member(jsii_name="createFlowLog")
    def create_flow_log(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        local_athena_querys: typing.Optional[builtins.bool] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Create Enterprise VPC Flow Logs (to central log account) and advanced diagnostics with Athena Querys.

        :param bucket: (experimental) the central s3 location for enterprise flow logs.
        :param local_athena_querys: (experimental) create in Account Athena Querys for flow logs.
        :param one_minute_flow_logs: (experimental) 1 minute resolution.

        :stability: experimental
        '''
        props = FlowLogProps(
            bucket=bucket,
            local_athena_querys=local_athena_querys,
            one_minute_flow_logs=one_minute_flow_logs,
        )

        return typing.cast(None, jsii.invoke(self, "createFlowLog", [props]))

    @jsii.member(jsii_name="router")
    def router(
        self,
        router_groups: typing.Sequence[typing.Union["RouterGroup", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) This is a convience method to present the routing for the Vpc in a simpler format, than the addRoutes Method, which it calls.

        :param router_groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c65b63affdb274a16435a517e07c119cd527facd7674bf9183cd22ce947c45)
            check_type(argname="argument router_groups", value=router_groups, expected_type=type_hints["router_groups"])
        return typing.cast(None, jsii.invoke(self, "router", [router_groups]))

    @jsii.member(jsii_name="shareSubnetGroup")
    def share_subnet_group(
        self,
        *,
        accounts: typing.Sequence[builtins.str],
        subnet_group: "SubnetGroup",
    ) -> None:
        '''(experimental) Share a subnetGroup with another AWS Account.

        :param accounts: 
        :param subnet_group: 

        :stability: experimental
        '''
        props = ShareSubnetGroupProps(accounts=accounts, subnet_group=subnet_group)

        return typing.cast(None, jsii.invoke(self, "shareSubnetGroup", [props]))

    @builtins.property
    @jsii.member(jsii_name="addRoutesProvider")
    def add_routes_provider(self) -> _aws_cdk_custom_resources_ceddda9d.Provider:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_custom_resources_ceddda9d.Provider, jsii.get(self, "addRoutesProvider"))

    @builtins.property
    @jsii.member(jsii_name="attachToCloudwanProvider")
    def attach_to_cloudwan_provider(
        self,
    ) -> _aws_cdk_custom_resources_ceddda9d.Provider:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_custom_resources_ceddda9d.Provider, jsii.get(self, "attachToCloudwanProvider"))

    @builtins.property
    @jsii.member(jsii_name="tgWaiterProvider")
    def tg_waiter_provider(self) -> _aws_cdk_custom_resources_ceddda9d.Provider:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_custom_resources_ceddda9d.Provider, jsii.get(self, "tgWaiterProvider"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''(experimental) the ec2.Vpc that is passed in as property.

        :stability: experimental
        '''
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="subnetConfiguration")
    def subnet_configuration(self) -> typing.List["SubnetGroup"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["SubnetGroup"], jsii.get(self, "subnetConfiguration"))

    @subnet_configuration.setter
    def subnet_configuration(self, value: typing.List["SubnetGroup"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874c8e8ac17aa1174acd7556424d965e8fef34d0d78342859fd925cf953730ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanCoreId")
    def cloud_wan_core_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanCoreId"))

    @cloud_wan_core_id.setter
    def cloud_wan_core_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33472325ed8494f2720ac2bf73ae8ce81b1cf3d512d6a0b2ec992932fe8eded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanCoreId", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanName")
    def cloud_wan_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) the Name of the cloudwan that the VPC is attached to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanName"))

    @cloud_wan_name.setter
    def cloud_wan_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d3412c9c859abe49586df5ed644e1d0685b6490c89fd436d0f32c6dc91d077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanName", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanSegment")
    def cloud_wan_segment(self) -> typing.Optional[builtins.str]:
        '''(experimental) the Name of the Cloudwan segment that the vpc is attached to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanSegment"))

    @cloud_wan_segment.setter
    def cloud_wan_segment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3216263b5ec104270e647b0063a56af2ad7b347eb810faf2c153942e4880a845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanSegment", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWanVpcAttachmentId")
    def cloud_wan_vpc_attachment_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) AttachmentId when the vpc is attached to a Cloudwan.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWanVpcAttachmentId"))

    @cloud_wan_vpc_attachment_id.setter
    def cloud_wan_vpc_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d9832737229a122a367ec3e7a07bba8892066861c43dd6cd0ca154ffcc7ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWanVpcAttachmentId", value)

    @builtins.property
    @jsii.member(jsii_name="firewallArn")
    def firewall_arn(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallArn"))

    @firewall_arn.setter
    def firewall_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd03bb5ab7531fde0e9147e92417cdb74a01fe2148af6cc2a2fcc9c429c419c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallArn", value)

    @builtins.property
    @jsii.member(jsii_name="r53endpointResolvers")
    def r53endpoint_resolvers(self) -> typing.Optional[_R53Resolverendpoints_5d3b063e]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_R53Resolverendpoints_5d3b063e], jsii.get(self, "r53endpointResolvers"))

    @r53endpoint_resolvers.setter
    def r53endpoint_resolvers(
        self,
        value: typing.Optional[_R53Resolverendpoints_5d3b063e],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e1ef772b1b9e9d5f3b075a06770f1de8e52d1931bc918f641f296a86515421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "r53endpointResolvers", value)

    @builtins.property
    @jsii.member(jsii_name="transitGWAttachmentID")
    def transit_gw_attachment_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) AttachmentId when the vpc is attached to a transitGateway.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGWAttachmentID"))

    @transit_gw_attachment_id.setter
    def transit_gw_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe9abb18409a4dbbcd8416ba209bdc1910f6b8b4352acc7070be01ad66ec043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGWAttachmentID", value)

    @builtins.property
    @jsii.member(jsii_name="transitGWID")
    def transit_gwid(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Id of the transitgateway that the VPC is attached to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGWID"))

    @transit_gwid.setter
    def transit_gwid(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb380a6ee549fc59e2ded36fe903386129598774b73c1d248849f8cf3892a525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGWID", value)

    @builtins.property
    @jsii.member(jsii_name="vpcAttachmentCR")
    def vpc_attachment_cr(self) -> typing.Optional[_aws_cdk_ceddda9d.CustomResource]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.CustomResource], jsii.get(self, "vpcAttachmentCR"))

    @vpc_attachment_cr.setter
    def vpc_attachment_cr(
        self,
        value: typing.Optional[_aws_cdk_ceddda9d.CustomResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e73fb7a6a7f7fb76432edb6435464f67d8420f256acb7bc648462511a595b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAttachmentCR", value)

    @builtins.property
    @jsii.member(jsii_name="vpcAttachmentId")
    def vpc_attachment_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAttachmentId"))

    @vpc_attachment_id.setter
    def vpc_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53cd355a791ff7536b5fdcf2ddac38402c085a4376115e465e7ca42208af28bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAttachmentId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcAttachmentSegmentName")
    def vpc_attachment_segment_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAttachmentSegmentName"))

    @vpc_attachment_segment_name.setter
    def vpc_attachment_segment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab68d0f381e1db64512d31662c14fddd48cee062eedca69250311c85adb3ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAttachmentSegmentName", value)


class EnterpriseVpcLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.network.EnterpriseVpcLambda",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f0ebf7319e30d2da6d4a9a6f731ce3817635d86938155d76abafabcd8216d63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="addRoutesProvider")
    def add_routes_provider(self) -> _aws_cdk_custom_resources_ceddda9d.Provider:
        '''(experimental) A custom resource to use for adding routes.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_custom_resources_ceddda9d.Provider, jsii.get(self, "addRoutesProvider"))

    @builtins.property
    @jsii.member(jsii_name="attachToCloudwanProvider")
    def attach_to_cloudwan_provider(
        self,
    ) -> _aws_cdk_custom_resources_ceddda9d.Provider:
        '''(experimental) attach to cloudwan with a water.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_custom_resources_ceddda9d.Provider, jsii.get(self, "attachToCloudwanProvider"))

    @builtins.property
    @jsii.member(jsii_name="tgWaiterProvider")
    def tg_waiter_provider(self) -> _aws_cdk_custom_resources_ceddda9d.Provider:
        '''(experimental) A check to see if transitgateway is ready to route to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_custom_resources_ceddda9d.Provider, jsii.get(self, "tgWaiterProvider"))


@jsii.data_type(
    jsii_type="raindancers-network.network.EnterpriseVpcProps",
    jsii_struct_bases=[],
    name_mapping={"evpc": "evpc", "vpc": "vpc"},
)
class EnterpriseVpcProps:
    def __init__(
        self,
        *,
        evpc: typing.Optional[typing.Union["EvpcProps", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]] = None,
    ) -> None:
        '''(experimental) Propertys for an Enterprise VPC.

        :param evpc: 
        :param vpc: 

        :stability: experimental
        '''
        if isinstance(evpc, dict):
            evpc = EvpcProps(**evpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10c67d63f70a244cebb22fef76a08bf66da2272c5f70c49da3a75c9a7059ab6)
            check_type(argname="argument evpc", value=evpc, expected_type=type_hints["evpc"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evpc is not None:
            self._values["evpc"] = evpc
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def evpc(self) -> typing.Optional["EvpcProps"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("evpc")
        return typing.cast(typing.Optional["EvpcProps"], result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.EvpcProps",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.VpcProps],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "ip_addresses": "ipAddresses",
        "max_azs": "maxAzs",
        "nat_gateway_provider": "natGatewayProvider",
        "nat_gateways": "natGateways",
        "nat_gateway_subnets": "natGatewaySubnets",
        "reserved_azs": "reservedAzs",
        "restrict_default_security_group": "restrictDefaultSecurityGroup",
        "subnet_configuration": "subnetConfiguration",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
        "subnet_groups": "subnetGroups",
    },
)
class EvpcProps(_aws_cdk_aws_ec2_ceddda9d.VpcProps):
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        ip_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        reserved_azs: typing.Optional[jsii.Number] = None,
        restrict_default_security_group: typing.Optional[builtins.bool] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_groups: typing.Optional[typing.Sequence["SubnetGroup"]] = None,
    ) -> None:
        '''
        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: (deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param ip_addresses: The Provider to use to allocate IP Space to your VPC. Options include static allocation or from a pool. Default: ec2.IpAddresses.cidr
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param reserved_azs: Define the number of AZs to reserve. When specified, the IP space is reserved for the azs but no actual resources are provisioned. Default: 0
        :param restrict_default_security_group: If set to true then the default inbound & outbound rules will be removed from the default security group. Default: true if '@aws-cdk/aws-ec2:restrictDefaultSecurityGroup' is enabled, false otherwise
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.
        :param subnet_groups: 

        :stability: experimental
        '''
        if isinstance(nat_gateway_subnets, dict):
            nat_gateway_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**nat_gateway_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f62cf51aa556ac2591b1189a13819e3db258d77ee3600dfd2fa96bdd1324f21)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument nat_gateway_provider", value=nat_gateway_provider, expected_type=type_hints["nat_gateway_provider"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument nat_gateway_subnets", value=nat_gateway_subnets, expected_type=type_hints["nat_gateway_subnets"])
            check_type(argname="argument reserved_azs", value=reserved_azs, expected_type=type_hints["reserved_azs"])
            check_type(argname="argument restrict_default_security_group", value=restrict_default_security_group, expected_type=type_hints["restrict_default_security_group"])
            check_type(argname="argument subnet_configuration", value=subnet_configuration, expected_type=type_hints["subnet_configuration"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
            check_type(argname="argument subnet_groups", value=subnet_groups, expected_type=type_hints["subnet_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if nat_gateway_provider is not None:
            self._values["nat_gateway_provider"] = nat_gateway_provider
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if nat_gateway_subnets is not None:
            self._values["nat_gateway_subnets"] = nat_gateway_subnets
        if reserved_azs is not None:
            self._values["reserved_azs"] = reserved_azs
        if restrict_default_security_group is not None:
            self._values["restrict_default_security_group"] = restrict_default_security_group
        if subnet_configuration is not None:
            self._values["subnet_configuration"] = subnet_configuration
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation
        if subnet_groups is not None:
            self._values["subnet_groups"] = subnet_groups

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Availability zones this VPC spans.

        Specify this option only if you do not specify ``maxAzs``.

        :default: - a subset of AZs of the stack
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'.

        Should be a minimum of /28 and maximum size of /16. The range will be
        split across all subnets per Availability Zone.

        :default: Vpc.DEFAULT_CIDR_RANGE

        :deprecated: Use ipAddresses instead

        :stability: deprecated
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        '''The default tenancy of instances launched into the VPC.

        By setting this to dedicated tenancy, instances will be launched on
        hardware dedicated to a single AWS customer, unless specifically specified
        at instance launch time. Please note, not all instance types are usable
        with Dedicated tenancy.

        :default: DefaultInstanceTenancy.Default (shared) tenancy
        '''
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the instances launched in the VPC get public DNS hostnames.

        If this attribute is true, instances in the VPC get public DNS hostnames,
        but only if the enableDnsSupport attribute is also set to true.

        :default: true
        '''
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DNS resolution is supported for the VPC.

        If this attribute is false, the Amazon-provided DNS server in the VPC that
        resolves public DNS hostnames to IP addresses is not enabled. If this
        attribute is true, queries to the Amazon provided DNS server at the
        169.254.169.253 IP address, or the reserved IP address at the base of the
        VPC IPv4 network range plus two will succeed.

        :default: true
        '''
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]]:
        '''Flow logs to add to this VPC.

        :default: - No flow logs.
        '''
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        '''Gateway endpoints to add to this VPC.

        :default: - None.
        '''
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses]:
        '''The Provider to use to allocate IP Space to your VPC.

        Options include static allocation or from a pool.

        :default: ec2.IpAddresses.cidr
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the maximum number of AZs to use in this region.

        If the region has more AZs than you want to use (for example, because of
        EIP limits), pick a lower number here. The AZs will be sorted and picked
        from the start of the list.

        If you pick a higher number than the number of AZs in the region, all AZs
        in the region will be selected. To use "all AZs" available to your
        account, use a high number (such as 99).

        Be aware that environment-agnostic stacks will be created with access to
        only 2 AZs, so to use more than 2 AZs, be sure to specify the account and
        region on your stack.

        Specify this option only if you do not specify ``availabilityZones``.

        :default: 3
        '''
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider]:
        '''What type of NAT provider to use.

        Select between NAT gateways or NAT instances. NAT gateways
        may not be available in all AWS regions.

        :default: NatProvider.gateway()
        '''
        result = self._values.get("nat_gateway_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider], result)

    @builtins.property
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        '''The number of NAT Gateways/Instances to create.

        The type of NAT gateway or instance will be determined by the
        ``natGatewayProvider`` parameter.

        You can set this number lower than the number of Availability Zones in your
        VPC in order to save on NAT cost. Be aware you may be charged for
        cross-AZ data traffic instead.

        :default: - One NAT gateway/instance per Availability Zone
        '''
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Configures the subnets which will have NAT Gateways/Instances.

        You can pick a specific group of subnets by specifying the group name;
        the picked subnets must be public subnets.

        Only necessary if you have more than one public subnet group.

        :default: - All public subnets.
        '''
        result = self._values.get("nat_gateway_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def reserved_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the number of AZs to reserve.

        When specified, the IP space is reserved for the azs but no actual
        resources are provisioned.

        :default: 0
        '''
        result = self._values.get("reserved_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def restrict_default_security_group(self) -> typing.Optional[builtins.bool]:
        '''If set to true then the default inbound & outbound rules will be removed from the default security group.

        :default: true if '@aws-cdk/aws-ec2:restrictDefaultSecurityGroup' is enabled, false otherwise
        '''
        result = self._values.get("restrict_default_security_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_configuration(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration]]:
        '''Configure the subnets to build for each AZ.

        Each entry in this list configures a Subnet Group; each group will contain a
        subnet for each Availability Zone.

        For example, if you want 1 public subnet, 1 private subnet, and 1 isolated
        subnet in each AZ provide the following::

           new ec2.Vpc(this, 'VPC', {
             subnetConfiguration: [
                {
                  cidrMask: 24,
                  name: 'ingress',
                  subnetType: ec2.SubnetType.PUBLIC,
                },
                {
                  cidrMask: 24,
                  name: 'application',
                  subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
                },
                {
                  cidrMask: 28,
                  name: 'rds',
                  subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
                }
             ]
           });

        :default:

        - The VPC CIDR will be evenly divided between 1 public and 1
        private subnet per AZ.
        '''
        result = self._values.get("subnet_configuration")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration]], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        '''The VPC name.

        Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag

        :default: this.node.path
        '''
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        '''VPN connections to this VPC.

        :default: - No connections.
        '''
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether a VPN gateway should be created and attached to this VPC.

        :default: - true when vpnGatewayAsn or vpnConnections is specified
        '''
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        '''The private Autonomous System Number (ASN) for the VPN gateway.

        :default: - Amazon default ASN.
        '''
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        '''Where to propagate VPN routes.

        :default:

        - On the route tables associated with private subnets. If no
        private subnets exists, isolated subnets are used. If no isolated subnets
        exists, public subnets are used.
        '''
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    @builtins.property
    def subnet_groups(self) -> typing.Optional[typing.List["SubnetGroup"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        return typing.cast(typing.Optional[typing.List["SubnetGroup"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.FlowLogProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "local_athena_querys": "localAthenaQuerys",
        "one_minute_flow_logs": "oneMinuteFlowLogs",
    },
)
class FlowLogProps:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        local_athena_querys: typing.Optional[builtins.bool] = None,
        one_minute_flow_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for flow logs *.

        :param bucket: (experimental) the central s3 location for enterprise flow logs.
        :param local_athena_querys: (experimental) create in Account Athena Querys for flow logs.
        :param one_minute_flow_logs: (experimental) 1 minute resolution.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb64a1c2b7e064306854c5cb6f5854426149885c46ac6e5ff279f68f78d5a3c6)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument local_athena_querys", value=local_athena_querys, expected_type=type_hints["local_athena_querys"])
            check_type(argname="argument one_minute_flow_logs", value=one_minute_flow_logs, expected_type=type_hints["one_minute_flow_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if local_athena_querys is not None:
            self._values["local_athena_querys"] = local_athena_querys
        if one_minute_flow_logs is not None:
            self._values["one_minute_flow_logs"] = one_minute_flow_logs

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) the central s3 location for enterprise flow logs.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def local_athena_querys(self) -> typing.Optional[builtins.bool]:
        '''(experimental) create in Account Athena Querys for flow logs.

        :stability: experimental
        '''
        result = self._values.get("local_athena_querys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def one_minute_flow_logs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) 1 minute resolution.

        :stability: experimental
        '''
        result = self._values.get("one_minute_flow_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.PrefixCidr",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr"},
)
class PrefixCidr:
    def __init__(self, *, cidr: builtins.str) -> None:
        '''
        :param cidr: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff0e93ff81dd8aacaf7be68de0e065fa7e86d4bb9f6b4608264a21e2b4668d4)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
        }

    @builtins.property
    def cidr(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrefixCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResolveSubnetGroupName(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.network.ResolveSubnetGroupName",
):
    '''(experimental) Creates a period task to update the SSM Agent on an EC2 Instance.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        azcount: jsii.Number,
        subnet_group_name: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param azcount: 
        :param subnet_group_name: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e8875c39688f72d7e0a0f2e693afc81cd4c268b4d01fb49cf80d7818b72925)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResolveSubnetGroupNameProps(
            azcount=azcount, subnet_group_name=subnet_group_name, vpc=vpc
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="subnetSelection")
    def subnet_selection(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, jsii.get(self, "subnetSelection"))

    @subnet_selection.setter
    def subnet_selection(
        self,
        value: _aws_cdk_aws_ec2_ceddda9d.SubnetSelection,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5771c33a80fd138204122c80e60a118dd7f427e82e606d17c24706c69945b370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetSelection", value)


@jsii.data_type(
    jsii_type="raindancers-network.network.ResolveSubnetGroupNameProps",
    jsii_struct_bases=[],
    name_mapping={
        "azcount": "azcount",
        "subnet_group_name": "subnetGroupName",
        "vpc": "vpc",
    },
)
class ResolveSubnetGroupNameProps:
    def __init__(
        self,
        *,
        azcount: jsii.Number,
        subnet_group_name: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    ) -> None:
        '''
        :param azcount: 
        :param subnet_group_name: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a758b1c1400b443c04ccb0c832370f245d451a3de204e3edbebc39f7d6530b0)
            check_type(argname="argument azcount", value=azcount, expected_type=type_hints["azcount"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "azcount": azcount,
            "subnet_group_name": subnet_group_name,
            "vpc": vpc,
        }

    @builtins.property
    def azcount(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("azcount")
        assert result is not None, "Required property 'azcount' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_group_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_group_name")
        assert result is not None, "Required property 'subnet_group_name' is missing"
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolveSubnetGroupNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.Route",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "destination": "destination",
        "cidr": "cidr",
        "subnet": "subnet",
    },
)
class Route:
    def __init__(
        self,
        *,
        description: builtins.str,
        destination: Destination,
        cidr: typing.Optional[builtins.str] = None,
        subnet: typing.Optional[typing.Union["SubnetGroup", "SubnetWildCards"]] = None,
    ) -> None:
        '''
        :param description: 
        :param destination: 
        :param cidr: 
        :param subnet: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6891e3733365f9894602c6936e4c0e21aad0a90ebf89bae562960c98a040b66a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "destination": destination,
        }
        if cidr is not None:
            self._values["cidr"] = cidr
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> Destination:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(Destination, result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet(self) -> typing.Optional[typing.Union["SubnetGroup", "SubnetWildCards"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[typing.Union["SubnetGroup", "SubnetWildCards"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.RouterGroup",
    jsii_struct_bases=[],
    name_mapping={"routes": "routes", "subnet_group": "subnetGroup"},
)
class RouterGroup:
    def __init__(
        self,
        *,
        routes: typing.Sequence[typing.Union[Route, typing.Dict[builtins.str, typing.Any]]],
        subnet_group: "SubnetGroup",
    ) -> None:
        '''
        :param routes: 
        :param subnet_group: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26f96a40e8c4d5155e7c5d432ed24d3937b0d7fafbc2dcf9627a3008c29f1a5)
            check_type(argname="argument routes", value=routes, expected_type=type_hints["routes"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "routes": routes,
            "subnet_group": subnet_group,
        }

    @builtins.property
    def routes(self) -> typing.List[Route]:
        '''
        :stability: experimental
        '''
        result = self._values.get("routes")
        assert result is not None, "Required property 'routes' is missing"
        return typing.cast(typing.List[Route], result)

    @builtins.property
    def subnet_group(self) -> "SubnetGroup":
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast("SubnetGroup", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouterGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.network.ShareSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={"accounts": "accounts", "subnet_group": "subnetGroup"},
)
class ShareSubnetGroupProps:
    def __init__(
        self,
        *,
        accounts: typing.Sequence[builtins.str],
        subnet_group: "SubnetGroup",
    ) -> None:
        '''
        :param accounts: 
        :param subnet_group: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e990e8ebb3f807eac11f2a28a6c06874c4ba4d31fb3a4b7be1a7672dc1c7a6)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "subnet_group": subnet_group,
        }

    @builtins.property
    def accounts(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_group(self) -> "SubnetGroup":
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast("SubnetGroup", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShareSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubnetGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.network.SubnetGroup",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cidr_mask: jsii.Number,
        name: builtins.str,
        subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr_mask: 
        :param name: 
        :param subnet_type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3765337098773fabb60dbf2ee92fa614f311e5f8b7be69a99738b9fd6a5b5bdb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ESubnetGroupProps(
            cidr_mask=cidr_mask, name=name, subnet_type=subnet_type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> ESubnetGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(ESubnetGroup, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: ESubnetGroup) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c9ecaf3f3eaa06d53c1f39abc7af0daeb54f4400bab997c9e033b9d3ca97a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value)


@jsii.enum(jsii_type="raindancers-network.network.SubnetWildCards")
class SubnetWildCards(enum.Enum):
    '''
    :stability: experimental
    '''

    ALLSUBNETS = "ALLSUBNETS"
    '''
    :stability: experimental
    '''


__all__ = [
    "AddAwsServiceEndPointsProps",
    "AddCoreRoutesProps",
    "AddEnterprizeZoneProps",
    "AddR53ZoneProps",
    "AddRoutesProps",
    "ApplianceMode",
    "AttachToCloudWanProps",
    "AttachToTransitGatewayProps",
    "CloudWanRoutingProtocolProps",
    "Destination",
    "ESubnetGroup",
    "ESubnetGroupProps",
    "EnterpriseVpc",
    "EnterpriseVpcLambda",
    "EnterpriseVpcProps",
    "EvpcProps",
    "FlowLogProps",
    "PrefixCidr",
    "ResolveSubnetGroupName",
    "ResolveSubnetGroupNameProps",
    "Route",
    "RouterGroup",
    "ShareSubnetGroupProps",
    "SubnetGroup",
    "SubnetWildCards",
]

publication.publish()

def _typecheckingstub__ba3d871d7a3d34269b14ecf698271c72a9e7ce024ad1cfd130b46ef122eac944(
    *,
    services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
    subnet_group: SubnetGroup,
    dynamo_db_gateway: typing.Optional[builtins.bool] = None,
    s3_gateway_interface: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe781b9a5afbd9cbd3eb283c2a155d0c6fa2fc8f058fac471750ebd8e16fa41(
    *,
    attachment_id: builtins.str,
    core_name: builtins.str,
    description: builtins.str,
    destination_cidr_blocks: typing.Sequence[builtins.str],
    policy_table_arn: builtins.str,
    segments: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be8aa3bf69e127ac8e18750deed08580355b3b98e66808099c26b5fe42b735a(
    *,
    domainname: builtins.str,
    hub_vpcs: typing.Sequence[typing.Union[_HubVpc_f33ed7e6, typing.Dict[builtins.str, typing.Any]]],
    is_hub_vpc: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2edde8cbf8bdb1e42676cf48c6225d58e8c220128c31d8408e26f4fd622a3cf(
    *,
    zone: builtins.str,
    central_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956d15f36f571d23526ddfa187efe9f7033d2ef4872d9ffdf8e7d89ba7f3001a(
    *,
    cidr: typing.Sequence[builtins.str],
    description: builtins.str,
    destination: Destination,
    subnet_groups: typing.Sequence[builtins.str],
    cloudwan_name: typing.Optional[builtins.str] = None,
    network_firewall_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d14da943ad99aff58715a46c233ed344e3ed682a856dae617fd06e857dd3da7(
    *,
    core_network_name: builtins.str,
    segment_name: builtins.str,
    appliance_mode: typing.Optional[builtins.bool] = None,
    attachment_subnet_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cab874cb1ee5844e2300e3fc9a5501a89fd8cececd7db3ee9c9befc96c2f39f(
    *,
    transit_gateway: _aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway,
    applicance_mode: typing.Optional[ApplianceMode] = None,
    attachment_subnet_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0db49e994c0a98983684f628c9ad2922224075c0fbd5b61bdd2e16996f36458(
    *,
    subnet_groups: typing.Sequence[builtins.str],
    accept_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny_route_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66bc48a5c59cb727347d874191c2cdafd8fb0f400c361e88bdaac0ab58e9bd2(
    *,
    cidr_mask: jsii.Number,
    name: builtins.str,
    subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233a2cc463688abf925c28cf81d573ef1990683283b8cfb18f61113d104e8934(
    *,
    cidr_mask: jsii.Number,
    name: builtins.str,
    subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7824f738e0341f5f59379d8b0e09dbac312a796352b0a37fab71ad9a75526bb6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    evpc: typing.Optional[typing.Union[EvpcProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e85c0d88596b9b5b0002423ab7ee5bea9376c71e0417447f4eb31aebcd6a1e(
    domains: typing.Sequence[builtins.str],
    search_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb7fb9484ab77ad1c99ec06db745aee4a2d43d54a858f55bb310fbf21076ecf(
    forwarding_rules: typing.Sequence[typing.Union[_OutboundForwardingRule_a6d0cb0c, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729a7b9f9fea1efe93ee55ffe575d1b4b9fc730cde62198c1abaf530b6fcd5bd(
    rolename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a7366a3c0ccc32921eff015ae01d1ec3d9e2f80d238071c4c5306c3052e354(
    firewall_name: builtins.str,
    firewall_policy: _aws_cdk_aws_networkfirewall_ceddda9d.CfnFirewallPolicy,
    subnet: SubnetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4e5400634be40939a319974a19264c5e947d8d1dd279b75358fe5e4a13258e(
    zonename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b86fd69f20f6c1a45edefb0b52b3d176011a0a373dc2e57ef1f59dab0f7ee72(
    subnet: SubnetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d84ae63ffa0860bf6396107b287070d21498898593e9fbb04aef32d20951dba(
    domain_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a4f8e336f8adf81160fcf70b4cdc7f1b8e54f9e9a3ccdb5fa9242f6cc9f896(
    zone_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c62bec98a484dd918c8fe08ceae85a9bdcc834cc9488f18fe5bc502c0c8be95(
    name: builtins.str,
    subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    org_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c65b63affdb274a16435a517e07c119cd527facd7674bf9183cd22ce947c45(
    router_groups: typing.Sequence[typing.Union[RouterGroup, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874c8e8ac17aa1174acd7556424d965e8fef34d0d78342859fd925cf953730ec(
    value: typing.List[SubnetGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33472325ed8494f2720ac2bf73ae8ce81b1cf3d512d6a0b2ec992932fe8eded(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d3412c9c859abe49586df5ed644e1d0685b6490c89fd436d0f32c6dc91d077(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3216263b5ec104270e647b0063a56af2ad7b347eb810faf2c153942e4880a845(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d9832737229a122a367ec3e7a07bba8892066861c43dd6cd0ca154ffcc7ebd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd03bb5ab7531fde0e9147e92417cdb74a01fe2148af6cc2a2fcc9c429c419c0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e1ef772b1b9e9d5f3b075a06770f1de8e52d1931bc918f641f296a86515421(
    value: typing.Optional[_R53Resolverendpoints_5d3b063e],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe9abb18409a4dbbcd8416ba209bdc1910f6b8b4352acc7070be01ad66ec043(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb380a6ee549fc59e2ded36fe903386129598774b73c1d248849f8cf3892a525(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e73fb7a6a7f7fb76432edb6435464f67d8420f256acb7bc648462511a595b35(
    value: typing.Optional[_aws_cdk_ceddda9d.CustomResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cd355a791ff7536b5fdcf2ddac38402c085a4376115e465e7ca42208af28bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab68d0f381e1db64512d31662c14fddd48cee062eedca69250311c85adb3ab6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0ebf7319e30d2da6d4a9a6f731ce3817635d86938155d76abafabcd8216d63(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10c67d63f70a244cebb22fef76a08bf66da2272c5f70c49da3a75c9a7059ab6(
    *,
    evpc: typing.Optional[typing.Union[EvpcProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f62cf51aa556ac2591b1189a13819e3db258d77ee3600dfd2fa96bdd1324f21(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    reserved_azs: typing.Optional[jsii.Number] = None,
    restrict_default_security_group: typing.Optional[builtins.bool] = None,
    subnet_configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_groups: typing.Optional[typing.Sequence[SubnetGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb64a1c2b7e064306854c5cb6f5854426149885c46ac6e5ff279f68f78d5a3c6(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    local_athena_querys: typing.Optional[builtins.bool] = None,
    one_minute_flow_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff0e93ff81dd8aacaf7be68de0e065fa7e86d4bb9f6b4608264a21e2b4668d4(
    *,
    cidr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e8875c39688f72d7e0a0f2e693afc81cd4c268b4d01fb49cf80d7818b72925(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    azcount: jsii.Number,
    subnet_group_name: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5771c33a80fd138204122c80e60a118dd7f427e82e606d17c24706c69945b370(
    value: _aws_cdk_aws_ec2_ceddda9d.SubnetSelection,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a758b1c1400b443c04ccb0c832370f245d451a3de204e3edbebc39f7d6530b0(
    *,
    azcount: jsii.Number,
    subnet_group_name: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6891e3733365f9894602c6936e4c0e21aad0a90ebf89bae562960c98a040b66a(
    *,
    description: builtins.str,
    destination: Destination,
    cidr: typing.Optional[builtins.str] = None,
    subnet: typing.Optional[typing.Union[SubnetGroup, SubnetWildCards]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26f96a40e8c4d5155e7c5d432ed24d3937b0d7fafbc2dcf9627a3008c29f1a5(
    *,
    routes: typing.Sequence[typing.Union[Route, typing.Dict[builtins.str, typing.Any]]],
    subnet_group: SubnetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e990e8ebb3f807eac11f2a28a6c06874c4ba4d31fb3a4b7be1a7672dc1c7a6(
    *,
    accounts: typing.Sequence[builtins.str],
    subnet_group: SubnetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3765337098773fabb60dbf2ee92fa614f311e5f8b7be69a99738b9fd6a5b5bdb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cidr_mask: jsii.Number,
    name: builtins.str,
    subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c9ecaf3f3eaa06d53c1f39abc7af0daeb54f4400bab997c9e033b9d3ca97a5(
    value: ESubnetGroup,
) -> None:
    """Type checking stubs"""
    pass
