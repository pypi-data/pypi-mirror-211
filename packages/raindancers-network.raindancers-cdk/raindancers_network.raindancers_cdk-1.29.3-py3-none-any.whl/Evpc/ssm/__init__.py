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
import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8


class CrossRegionParameterReader(
    _aws_cdk_custom_resources_ceddda9d.AwsCustomResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ssm.CrossRegionParameterReader",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        parameter_name: builtins.str,
        region: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param parameter_name: 
        :param region: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b29966b8f2a9776fea7fba0d1ba8e4cf9f23a3b2c72c625be1cda276cab44a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = CrossRegionParameterReaderProps(
            parameter_name=parameter_name, region=region
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "parameterValue", []))


@jsii.data_type(
    jsii_type="raindancers-network.ssm.CrossRegionParameterReaderProps",
    jsii_struct_bases=[],
    name_mapping={"parameter_name": "parameterName", "region": "region"},
)
class CrossRegionParameterReaderProps:
    def __init__(self, *, parameter_name: builtins.str, region: builtins.str) -> None:
        '''
        :param parameter_name: 
        :param region: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0226b290189f138a98ac3b2f756e87be80da84d5fbd9941a70878fe3d2ca07d3)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "region": region,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossRegionParameterReaderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CrossRegionParameterWriter(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ssm.CrossRegionParameterWriter",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        parameter_name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: 
        :param parameter_name: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ddcf254f66d058b1ee2b10aff82a9e416454e214ef34240b1a6ee6dd211ff7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrossRegionParameterWriterProps(
            description=description, parameter_name=parameter_name, value=value
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.ssm.CrossRegionParameterWriterProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "parameter_name": "parameterName",
        "value": "value",
    },
)
class CrossRegionParameterWriterProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        parameter_name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param description: 
        :param parameter_name: 
        :param value: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce967ccbc6aeb3e67d3be561d009cded0b8aad6950776f810f0557f3c65c630)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "parameter_name": parameter_name,
            "value": value,
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
    def parameter_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossRegionParameterWriterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UpdateSSMAgent(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ssm.UpdateSSMAgent",
):
    '''(experimental) Creates a period task to update the SSM Agent on an EC2 Instance.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance: _aws_cdk_aws_ec2_ceddda9d.Instance,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance: (experimental) The EC2 Instance that will be udpated.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e650c502c54415f32cd56939a62006ccf8f7422faeb49f993117c714cfe5e52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UpdateSSMAgentProps(instance=instance)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.ssm.UpdateSSMAgentProps",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance"},
)
class UpdateSSMAgentProps:
    def __init__(self, *, instance: _aws_cdk_aws_ec2_ceddda9d.Instance) -> None:
        '''
        :param instance: (experimental) The EC2 Instance that will be udpated.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422a0a9fca0e8ba896a6e4b0b1235a965b24d157527e0cfe1552acfb2cbf8c7a)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance": instance,
        }

    @builtins.property
    def instance(self) -> _aws_cdk_aws_ec2_ceddda9d.Instance:
        '''(experimental) The EC2 Instance that will be udpated.

        :stability: experimental
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Instance, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpdateSSMAgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CrossRegionParameterReader",
    "CrossRegionParameterReaderProps",
    "CrossRegionParameterWriter",
    "CrossRegionParameterWriterProps",
    "UpdateSSMAgent",
    "UpdateSSMAgentProps",
]

publication.publish()

def _typecheckingstub__8b29966b8f2a9776fea7fba0d1ba8e4cf9f23a3b2c72c625be1cda276cab44a7(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    parameter_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0226b290189f138a98ac3b2f756e87be80da84d5fbd9941a70878fe3d2ca07d3(
    *,
    parameter_name: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ddcf254f66d058b1ee2b10aff82a9e416454e214ef34240b1a6ee6dd211ff7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    parameter_name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce967ccbc6aeb3e67d3be561d009cded0b8aad6950776f810f0557f3c65c630(
    *,
    description: builtins.str,
    parameter_name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e650c502c54415f32cd56939a62006ccf8f7422faeb49f993117c714cfe5e52(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance: _aws_cdk_aws_ec2_ceddda9d.Instance,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422a0a9fca0e8ba896a6e4b0b1235a965b24d157527e0cfe1552acfb2cbf8c7a(
    *,
    instance: _aws_cdk_aws_ec2_ceddda9d.Instance,
) -> None:
    """Type checking stubs"""
    pass
