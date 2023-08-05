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


class EnforceImdsv2(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ec2.EnforceImdsv2",
):
    '''(experimental) Enforces the use of IMDSv2, without causing replacement of the Instance.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instances: typing.Union[_aws_cdk_aws_ec2_ceddda9d.Instance, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Instance]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instances: (experimental) ec2 Instance or Instances.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac7261017303ebe3993c97d96ae46a9d669f472dbad762a9317f72db7f4af0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnforceImdsv2Props(instances=instances)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.ec2.EnforceImdsv2Props",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class EnforceImdsv2Props:
    def __init__(
        self,
        *,
        instances: typing.Union[_aws_cdk_aws_ec2_ceddda9d.Instance, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Instance]],
    ) -> None:
        '''
        :param instances: (experimental) ec2 Instance or Instances.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445cf0d748c2b2e8dcf5c50bc1ae643e9a66673cd6330c0a52185c6fea187ee1)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
        }

    @builtins.property
    def instances(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.Instance, typing.List[_aws_cdk_aws_ec2_ceddda9d.Instance]]:
        '''(experimental) ec2 Instance or Instances.

        :stability: experimental
        '''
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.Instance, typing.List[_aws_cdk_aws_ec2_ceddda9d.Instance]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnforceImdsv2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FindPrefixList(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.ec2.FindPrefixList",
):
    '''(experimental) Enforces the use of IMDSv2, without causing replacement of the Instance.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        prefix_list_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param prefix_list_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d982a1726ef0bad3bb761d66c42a25359881f13456d4503fa2d2a078410672)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FindPrefixListProps(prefix_list_name=prefix_list_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="prefixListId")
    def prefix_list_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "prefixListId"))

    @prefix_list_id.setter
    def prefix_list_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7708415f04807405a68b00b6b2387c2840a67db81e34f300228ecb4ce497e2dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixListId", value)


@jsii.data_type(
    jsii_type="raindancers-network.ec2.FindPrefixListProps",
    jsii_struct_bases=[],
    name_mapping={"prefix_list_name": "prefixListName"},
)
class FindPrefixListProps:
    def __init__(self, *, prefix_list_name: builtins.str) -> None:
        '''
        :param prefix_list_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e10b3240a4ea1cfef2cd0987dfb43700428ad199fc38b155b69965cd7adf208)
            check_type(argname="argument prefix_list_name", value=prefix_list_name, expected_type=type_hints["prefix_list_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix_list_name": prefix_list_name,
        }

    @builtins.property
    def prefix_list_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("prefix_list_name")
        assert result is not None, "Required property 'prefix_list_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FindPrefixListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EnforceImdsv2",
    "EnforceImdsv2Props",
    "FindPrefixList",
    "FindPrefixListProps",
]

publication.publish()

def _typecheckingstub__1ac7261017303ebe3993c97d96ae46a9d669f472dbad762a9317f72db7f4af0e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instances: typing.Union[_aws_cdk_aws_ec2_ceddda9d.Instance, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Instance]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445cf0d748c2b2e8dcf5c50bc1ae643e9a66673cd6330c0a52185c6fea187ee1(
    *,
    instances: typing.Union[_aws_cdk_aws_ec2_ceddda9d.Instance, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Instance]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d982a1726ef0bad3bb761d66c42a25359881f13456d4503fa2d2a078410672(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    prefix_list_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7708415f04807405a68b00b6b2387c2840a67db81e34f300228ecb4ce497e2dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e10b3240a4ea1cfef2cd0987dfb43700428ad199fc38b155b69965cd7adf208(
    *,
    prefix_list_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
