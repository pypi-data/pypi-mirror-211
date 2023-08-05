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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class GetTunnelAddressPair(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ipam.GetTunnelAddressPair",
):
    '''(experimental) Allocate a pair of /30 networks CIDRS for use in Ipsec VPN Tunnels.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ipam_pool_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: scope in which this resource is created.
        :param id: scope id of the resoruce.
        :param ipam_pool_id: (experimental) The IPAM Pool Id from which the assginment will be made from.
        :param name: (experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09787e313792d042328d7ebe8cb7530a5d79fbc28056596dd2cb67120a8256d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GetTunnelAddressPairProps(ipam_pool_id=ipam_pool_id, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignedCidrPair")
    def assigned_cidr_pair(self) -> typing.List[builtins.str]:
        '''(experimental) returns 2 cidr blocks as an array to be used by an IPsec Tunnel.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assignedCidrPair"))


@jsii.data_type(
    jsii_type="raindancers-network.ipam.GetTunnelAddressPairProps",
    jsii_struct_bases=[],
    name_mapping={"ipam_pool_id": "ipamPoolId", "name": "name"},
)
class GetTunnelAddressPairProps:
    def __init__(self, *, ipam_pool_id: builtins.str, name: builtins.str) -> None:
        '''(experimental) Properties for obtaining an IPAM assigned address pair for use on IPsec VPN Tunnels.

        :param ipam_pool_id: (experimental) The IPAM Pool Id from which the assginment will be made from.
        :param name: (experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d16444c6a14ab5c7216f823accf7637575460adf4ad51dc842f410ecf960c7)
            check_type(argname="argument ipam_pool_id", value=ipam_pool_id, expected_type=type_hints["ipam_pool_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ipam_pool_id": ipam_pool_id,
            "name": name,
        }

    @builtins.property
    def ipam_pool_id(self) -> builtins.str:
        '''(experimental) The IPAM Pool Id from which the assginment will be made from.

        :stability: experimental
        '''
        result = self._values.get("ipam_pool_id")
        assert result is not None, "Required property 'ipam_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The Name used by IPAM to record the allocation.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetTunnelAddressPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpsecTunnelPool(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ipam.IpsecTunnelPool",
):
    '''(experimental) Creates an IPAM pool to assign address's for IPsec VPNS.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cidr: builtins.str,
        description: builtins.str,
        ipam_scope_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: scope in which this resource is defined.
        :param id: id of the resource.
        :param cidr: (experimental) The Cidr range for pools to be created from eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24. It must also not overlap the AWS reserved ranges. T
        :param description: (experimental) the description used by IPAM to describe the pool.
        :param ipam_scope_id: (experimental) The IPAM Scope Id to use to create the Pool.
        :param name: (experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332a23c478c773770c208fee7335e22a4531f9866eda2594c87fef56377db962)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpsecTunnelPoolProps(
            cidr=cidr, description=description, ipam_scope_id=ipam_scope_id, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="ipampool")
    def ipampool(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool:
        '''(experimental) returns the created ipam Pool.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPool, jsii.get(self, "ipampool"))


@jsii.data_type(
    jsii_type="raindancers-network.ipam.IpsecTunnelPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr": "cidr",
        "description": "description",
        "ipam_scope_id": "ipamScopeId",
        "name": "name",
    },
)
class IpsecTunnelPoolProps:
    def __init__(
        self,
        *,
        cidr: builtins.str,
        description: builtins.str,
        ipam_scope_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''(experimental) Properties for defining a IPAM Pool specifically for IPSec VPN Tunnels.

        :param cidr: (experimental) The Cidr range for pools to be created from eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24. It must also not overlap the AWS reserved ranges. T
        :param description: (experimental) the description used by IPAM to describe the pool.
        :param ipam_scope_id: (experimental) The IPAM Scope Id to use to create the Pool.
        :param name: (experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94611bad4bf3289460122035a77887274e0052b5d8c5e0ff9145f7cd513e2f82)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ipam_scope_id", value=ipam_scope_id, expected_type=type_hints["ipam_scope_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "description": description,
            "ipam_scope_id": ipam_scope_id,
            "name": name,
        }

    @builtins.property
    def cidr(self) -> builtins.str:
        '''(experimental) The Cidr range for pools to be created from    eg, 169.254.100.0/27 The cidr must be in the 169.254.0.0/16 range and must be a minimum of a /29 and a maximum of /24.

        It must also not overlap the AWS reserved ranges. T

        :stability: experimental
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) the description used by IPAM to describe the pool.

        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipam_scope_id(self) -> builtins.str:
        '''(experimental) The IPAM Scope Id to use to create the Pool.

        :stability: experimental
        '''
        result = self._values.get("ipam_scope_id")
        assert result is not None, "Required property 'ipam_scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name used by IPAM to identify the pool.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpsecTunnelPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GetTunnelAddressPair",
    "GetTunnelAddressPairProps",
    "IpsecTunnelPool",
    "IpsecTunnelPoolProps",
]

publication.publish()

def _typecheckingstub__a09787e313792d042328d7ebe8cb7530a5d79fbc28056596dd2cb67120a8256d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ipam_pool_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d16444c6a14ab5c7216f823accf7637575460adf4ad51dc842f410ecf960c7(
    *,
    ipam_pool_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332a23c478c773770c208fee7335e22a4531f9866eda2594c87fef56377db962(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cidr: builtins.str,
    description: builtins.str,
    ipam_scope_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94611bad4bf3289460122035a77887274e0052b5d8c5e0ff9145f7cd513e2f82(
    *,
    cidr: builtins.str,
    description: builtins.str,
    ipam_scope_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
