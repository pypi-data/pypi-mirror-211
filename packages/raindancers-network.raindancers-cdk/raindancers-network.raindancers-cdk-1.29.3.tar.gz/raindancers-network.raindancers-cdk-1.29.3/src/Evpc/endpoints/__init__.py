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


class AwsServiceEndPoints(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.endpoints.AwsServiceEndPoints",
):
    '''(experimental) Provisions a set of AWS Service Endpoints in a VPC.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
        subnet_group: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        dynamo_db_gateway_interface: typing.Optional[builtins.bool] = None,
        s3_gateway_interface: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: The scope that this construct is created in.
        :param id: Id for the construct.
        :param services: (experimental) An arry of InterfaceVPCEndpoints.
        :param subnet_group: (experimental) Subnet Group in which to create the service. Typically a subnet Dedicated to the task
        :param vpc: (experimental) The vpc in which the service is created.
        :param dynamo_db_gateway_interface: (experimental) indicate true for a Dynamo Gateway Interface.
        :param s3_gateway_interface: (experimental) indicate true for a S3 Gateway Interface.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9d1674e1e2bdc4e740dc3ebfc3fb7e14d9e9b40c8104972e16cc6e8df720b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsServiceEndPointsProps(
            services=services,
            subnet_group=subnet_group,
            vpc=vpc,
            dynamo_db_gateway_interface=dynamo_db_gateway_interface,
            s3_gateway_interface=s3_gateway_interface,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.endpoints.AwsServiceEndPointsProps",
    jsii_struct_bases=[],
    name_mapping={
        "services": "services",
        "subnet_group": "subnetGroup",
        "vpc": "vpc",
        "dynamo_db_gateway_interface": "dynamoDBGatewayInterface",
        "s3_gateway_interface": "s3GatewayInterface",
    },
)
class AwsServiceEndPointsProps:
    def __init__(
        self,
        *,
        services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
        subnet_group: builtins.str,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        dynamo_db_gateway_interface: typing.Optional[builtins.bool] = None,
        s3_gateway_interface: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties to create a set of AWS service Endpoints.

        :param services: (experimental) An arry of InterfaceVPCEndpoints.
        :param subnet_group: (experimental) Subnet Group in which to create the service. Typically a subnet Dedicated to the task
        :param vpc: (experimental) The vpc in which the service is created.
        :param dynamo_db_gateway_interface: (experimental) indicate true for a Dynamo Gateway Interface.
        :param s3_gateway_interface: (experimental) indicate true for a S3 Gateway Interface.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4163cde9819d6303bedde00823f37d64dd51f8bd1658717936967f791762e5c1)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument dynamo_db_gateway_interface", value=dynamo_db_gateway_interface, expected_type=type_hints["dynamo_db_gateway_interface"])
            check_type(argname="argument s3_gateway_interface", value=s3_gateway_interface, expected_type=type_hints["s3_gateway_interface"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "services": services,
            "subnet_group": subnet_group,
            "vpc": vpc,
        }
        if dynamo_db_gateway_interface is not None:
            self._values["dynamo_db_gateway_interface"] = dynamo_db_gateway_interface
        if s3_gateway_interface is not None:
            self._values["s3_gateway_interface"] = s3_gateway_interface

    @builtins.property
    def services(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService]:
        '''(experimental) An arry of InterfaceVPCEndpoints.

        :stability: experimental
        '''
        result = self._values.get("services")
        assert result is not None, "Required property 'services' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService], result)

    @builtins.property
    def subnet_group(self) -> builtins.str:
        '''(experimental) Subnet Group in which to create the service.

        Typically a subnet Dedicated to the task

        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''(experimental) The vpc in which the service is created.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    @builtins.property
    def dynamo_db_gateway_interface(self) -> typing.Optional[builtins.bool]:
        '''(experimental) indicate true for a Dynamo Gateway Interface.

        :stability: experimental
        '''
        result = self._values.get("dynamo_db_gateway_interface")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def s3_gateway_interface(self) -> typing.Optional[builtins.bool]:
        '''(experimental) indicate true for a S3 Gateway Interface.

        :stability: experimental
        '''
        result = self._values.get("s3_gateway_interface")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsServiceEndPointsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsServiceEndPoints",
    "AwsServiceEndPointsProps",
]

publication.publish()

def _typecheckingstub__8f9d1674e1e2bdc4e740dc3ebfc3fb7e14d9e9b40c8104972e16cc6e8df720b9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
    subnet_group: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    dynamo_db_gateway_interface: typing.Optional[builtins.bool] = None,
    s3_gateway_interface: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4163cde9819d6303bedde00823f37d64dd51f8bd1658717936967f791762e5c1(
    *,
    services: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
    subnet_group: builtins.str,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    dynamo_db_gateway_interface: typing.Optional[builtins.bool] = None,
    s3_gateway_interface: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
