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
from ..dns import R53Resolverendpoints as _R53Resolverendpoints_5d3b063e


@jsii.enum(jsii_type="raindancers-network.crowdstrike.CrowdStrikeCloud")
class CrowdStrikeCloud(enum.Enum):
    '''
    :stability: experimental
    '''

    US1 = "US1"
    '''
    :stability: experimental
    '''
    US2 = "US2"
    '''
    :stability: experimental
    '''
    EU1 = "EU1"
    '''
    :stability: experimental
    '''


class CrowdStrikeExtendedEndpoint(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.crowdstrike.CrowdStrikeExtendedEndpoint",
):
    '''(experimental) This will.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        crowdstrike_cloud: CrowdStrikeCloud,
        peering_vpc: typing.Optional[typing.Union["VpcRegionId", typing.Dict[builtins.str, typing.Any]]] = None,
        use_elb_in_peered_vpc: typing.Optional[builtins.bool] = None,
        vpccidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param crowdstrike_cloud: (experimental) aws The EC2 Instance that will be udpated.
        :param peering_vpc: 
        :param use_elb_in_peered_vpc: 
        :param vpccidr: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ff544863099fe7ea4efc06cb7118e4451593edb21ee5d916921793ea6da24b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrowdStrikeExtendedEndpointProps(
            crowdstrike_cloud=crowdstrike_cloud,
            peering_vpc=peering_vpc,
            use_elb_in_peered_vpc=use_elb_in_peered_vpc,
            vpccidr=vpccidr,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="download")
    def download(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "download"))

    @builtins.property
    @jsii.member(jsii_name="downloadZone")
    def download_zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "downloadZone"))

    @builtins.property
    @jsii.member(jsii_name="downloadZoneName")
    def download_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "downloadZoneName"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="proxyZone")
    def proxy_zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "proxyZone"))

    @builtins.property
    @jsii.member(jsii_name="proxyZoneName")
    def proxy_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "proxyZoneName"))


@jsii.data_type(
    jsii_type="raindancers-network.crowdstrike.CrowdStrikeExtendedEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "crowdstrike_cloud": "crowdstrikeCloud",
        "peering_vpc": "peeringVpc",
        "use_elb_in_peered_vpc": "useELBInPeeredVpc",
        "vpccidr": "vpccidr",
    },
)
class CrowdStrikeExtendedEndpointProps:
    def __init__(
        self,
        *,
        crowdstrike_cloud: CrowdStrikeCloud,
        peering_vpc: typing.Optional[typing.Union["VpcRegionId", typing.Dict[builtins.str, typing.Any]]] = None,
        use_elb_in_peered_vpc: typing.Optional[builtins.bool] = None,
        vpccidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crowdstrike_cloud: (experimental) aws The EC2 Instance that will be udpated.
        :param peering_vpc: 
        :param use_elb_in_peered_vpc: 
        :param vpccidr: 

        :stability: experimental
        '''
        if isinstance(peering_vpc, dict):
            peering_vpc = VpcRegionId(**peering_vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2aa18b77860bc37384c047078ec7f28782acbc3d735bb812f5d6700bac5e671)
            check_type(argname="argument crowdstrike_cloud", value=crowdstrike_cloud, expected_type=type_hints["crowdstrike_cloud"])
            check_type(argname="argument peering_vpc", value=peering_vpc, expected_type=type_hints["peering_vpc"])
            check_type(argname="argument use_elb_in_peered_vpc", value=use_elb_in_peered_vpc, expected_type=type_hints["use_elb_in_peered_vpc"])
            check_type(argname="argument vpccidr", value=vpccidr, expected_type=type_hints["vpccidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crowdstrike_cloud": crowdstrike_cloud,
        }
        if peering_vpc is not None:
            self._values["peering_vpc"] = peering_vpc
        if use_elb_in_peered_vpc is not None:
            self._values["use_elb_in_peered_vpc"] = use_elb_in_peered_vpc
        if vpccidr is not None:
            self._values["vpccidr"] = vpccidr

    @builtins.property
    def crowdstrike_cloud(self) -> CrowdStrikeCloud:
        '''(experimental) aws The EC2 Instance that will be udpated.

        :stability: experimental
        '''
        result = self._values.get("crowdstrike_cloud")
        assert result is not None, "Required property 'crowdstrike_cloud' is missing"
        return typing.cast(CrowdStrikeCloud, result)

    @builtins.property
    def peering_vpc(self) -> typing.Optional["VpcRegionId"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("peering_vpc")
        return typing.cast(typing.Optional["VpcRegionId"], result)

    @builtins.property
    def use_elb_in_peered_vpc(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("use_elb_in_peered_vpc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpccidr(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpccidr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrowdStrikeExtendedEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CrowdStrikeNLB(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.crowdstrike.CrowdStrikeNLB",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        crowdstrike_region: CrowdStrikeCloud,
        download: builtins.str,
        downloadhosted_zone: builtins.str,
        downloadhosted_zone_name: builtins.str,
        proxy: builtins.str,
        proxyhosted_zone: builtins.str,
        proxyhosted_zone_name: builtins.str,
        region: builtins.str,
        routeresolver_endpoints: _R53Resolverendpoints_5d3b063e,
        subnet_group_name: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param crowdstrike_region: 
        :param download: 
        :param downloadhosted_zone: 
        :param downloadhosted_zone_name: 
        :param proxy: 
        :param proxyhosted_zone: 
        :param proxyhosted_zone_name: 
        :param region: 
        :param routeresolver_endpoints: 
        :param subnet_group_name: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ebec4a9b78326a3d1168516dd8675cb18751b5623134c74652b9e6786d5613)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrowdStrikeNLBProps(
            crowdstrike_region=crowdstrike_region,
            download=download,
            downloadhosted_zone=downloadhosted_zone,
            downloadhosted_zone_name=downloadhosted_zone_name,
            proxy=proxy,
            proxyhosted_zone=proxyhosted_zone,
            proxyhosted_zone_name=proxyhosted_zone_name,
            region=region,
            routeresolver_endpoints=routeresolver_endpoints,
            subnet_group_name=subnet_group_name,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="raindancers-network.crowdstrike.CrowdStrikeNLBProps",
    jsii_struct_bases=[],
    name_mapping={
        "crowdstrike_region": "crowdstrikeRegion",
        "download": "download",
        "downloadhosted_zone": "downloadhostedZone",
        "downloadhosted_zone_name": "downloadhostedZoneName",
        "proxy": "proxy",
        "proxyhosted_zone": "proxyhostedZone",
        "proxyhosted_zone_name": "proxyhostedZoneName",
        "region": "region",
        "routeresolver_endpoints": "routeresolverEndpoints",
        "subnet_group_name": "subnetGroupName",
        "vpc": "vpc",
    },
)
class CrowdStrikeNLBProps:
    def __init__(
        self,
        *,
        crowdstrike_region: CrowdStrikeCloud,
        download: builtins.str,
        downloadhosted_zone: builtins.str,
        downloadhosted_zone_name: builtins.str,
        proxy: builtins.str,
        proxyhosted_zone: builtins.str,
        proxyhosted_zone_name: builtins.str,
        region: builtins.str,
        routeresolver_endpoints: _R53Resolverendpoints_5d3b063e,
        subnet_group_name: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''
        :param crowdstrike_region: 
        :param download: 
        :param downloadhosted_zone: 
        :param downloadhosted_zone_name: 
        :param proxy: 
        :param proxyhosted_zone: 
        :param proxyhosted_zone_name: 
        :param region: 
        :param routeresolver_endpoints: 
        :param subnet_group_name: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d308ba88b22248f14a2ebf2b44beb884bdd3e50edb3e33ca8efcb6d7f99c9e9)
            check_type(argname="argument crowdstrike_region", value=crowdstrike_region, expected_type=type_hints["crowdstrike_region"])
            check_type(argname="argument download", value=download, expected_type=type_hints["download"])
            check_type(argname="argument downloadhosted_zone", value=downloadhosted_zone, expected_type=type_hints["downloadhosted_zone"])
            check_type(argname="argument downloadhosted_zone_name", value=downloadhosted_zone_name, expected_type=type_hints["downloadhosted_zone_name"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument proxyhosted_zone", value=proxyhosted_zone, expected_type=type_hints["proxyhosted_zone"])
            check_type(argname="argument proxyhosted_zone_name", value=proxyhosted_zone_name, expected_type=type_hints["proxyhosted_zone_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument routeresolver_endpoints", value=routeresolver_endpoints, expected_type=type_hints["routeresolver_endpoints"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crowdstrike_region": crowdstrike_region,
            "download": download,
            "downloadhosted_zone": downloadhosted_zone,
            "downloadhosted_zone_name": downloadhosted_zone_name,
            "proxy": proxy,
            "proxyhosted_zone": proxyhosted_zone,
            "proxyhosted_zone_name": proxyhosted_zone_name,
            "region": region,
            "routeresolver_endpoints": routeresolver_endpoints,
            "subnet_group_name": subnet_group_name,
            "vpc": vpc,
        }

    @builtins.property
    def crowdstrike_region(self) -> CrowdStrikeCloud:
        '''
        :stability: experimental
        '''
        result = self._values.get("crowdstrike_region")
        assert result is not None, "Required property 'crowdstrike_region' is missing"
        return typing.cast(CrowdStrikeCloud, result)

    @builtins.property
    def download(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("download")
        assert result is not None, "Required property 'download' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def downloadhosted_zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("downloadhosted_zone")
        assert result is not None, "Required property 'downloadhosted_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def downloadhosted_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("downloadhosted_zone_name")
        assert result is not None, "Required property 'downloadhosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxy(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("proxy")
        assert result is not None, "Required property 'proxy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxyhosted_zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("proxyhosted_zone")
        assert result is not None, "Required property 'proxyhosted_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxyhosted_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("proxyhosted_zone_name")
        assert result is not None, "Required property 'proxyhosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routeresolver_endpoints(self) -> _R53Resolverendpoints_5d3b063e:
        '''
        :stability: experimental
        '''
        result = self._values.get("routeresolver_endpoints")
        assert result is not None, "Required property 'routeresolver_endpoints' is missing"
        return typing.cast(_R53Resolverendpoints_5d3b063e, result)

    @builtins.property
    def subnet_group_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_group_name")
        assert result is not None, "Required property 'subnet_group_name' is missing"
        return typing.cast(builtins.str, result)

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
        return "CrowdStrikeNLBProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CrowdStrikePrivateLink(
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.crowdstrike.CrowdStrikePrivateLink",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EU1")
    def EU1(cls) -> "CrowdStrikePrivateLink":
        '''
        :stability: experimental
        '''
        return typing.cast("CrowdStrikePrivateLink", jsii.sget(cls, "EU1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="US1")
    def US1(cls) -> "CrowdStrikePrivateLink":
        '''
        :stability: experimental
        '''
        return typing.cast("CrowdStrikePrivateLink", jsii.sget(cls, "US1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="US2")
    def US2(cls) -> "CrowdStrikePrivateLink":
        '''
        :stability: experimental
        '''
        return typing.cast("CrowdStrikePrivateLink", jsii.sget(cls, "US2"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> "CrowdStrikeServices":
        '''
        :stability: experimental
        '''
        return typing.cast("CrowdStrikeServices", jsii.get(self, "value"))


class CrowdStrikePrivateLinkEndpoint(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.crowdstrike.CrowdStrikePrivateLinkEndpoint",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        crowd_strike_cloud: CrowdStrikeCloud,
        subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        peeredwith_nlb: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param crowd_strike_cloud: 
        :param subnets: 
        :param vpc: (experimental) The EC2 Instance that will be udpated.
        :param peeredwith_nlb: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b87a4b8466e3b5c05d5057d01bf7de72238b154f6db6c4c5bcd5da87365ae53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrowdStrikePrivateLinkEndpointProps(
            crowd_strike_cloud=crowd_strike_cloud,
            subnets=subnets,
            vpc=vpc,
            peeredwith_nlb=peeredwith_nlb,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="download")
    def download(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "download"))

    @download.setter
    def download(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025278ee7968de6176be8fd3a5b46db52bac7d3f189f6dc828c65a15b2b6a815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "download", value)

    @builtins.property
    @jsii.member(jsii_name="downloadhostedZone")
    def downloadhosted_zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "downloadhostedZone"))

    @downloadhosted_zone.setter
    def downloadhosted_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18475e3ec120a2180a0e9549b0540e83d03c6ffd390b6894b6b67f5bbbcb034f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downloadhostedZone", value)

    @builtins.property
    @jsii.member(jsii_name="downloadhostedZoneName")
    def downloadhosted_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "downloadhostedZoneName"))

    @downloadhosted_zone_name.setter
    def downloadhosted_zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918c30f4bc8924820476fd3d5f3f6c696079cfc423eae7584cc72e009e4df6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downloadhostedZoneName", value)

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "proxy"))

    @proxy.setter
    def proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f637ea673ce2c556e14ba951f8050c698addacfe8329f5bfd581d351c2acf792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxy", value)

    @builtins.property
    @jsii.member(jsii_name="proxyhostedZone")
    def proxyhosted_zone(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "proxyhostedZone"))

    @proxyhosted_zone.setter
    def proxyhosted_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8bc0d12617220caed347f53c95585ecb3e97f8cef27bca52892d67712d69bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyhostedZone", value)

    @builtins.property
    @jsii.member(jsii_name="proxyhostedZoneName")
    def proxyhosted_zone_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "proxyhostedZoneName"))

    @proxyhosted_zone_name.setter
    def proxyhosted_zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168ecb49b2a288cce769bac40363cb02515170d6af49c6b79c2b70f4a0474152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyhostedZoneName", value)


@jsii.data_type(
    jsii_type="raindancers-network.crowdstrike.CrowdStrikePrivateLinkEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "crowd_strike_cloud": "crowdStrikeCloud",
        "subnets": "subnets",
        "vpc": "vpc",
        "peeredwith_nlb": "peeredwithNLB",
    },
)
class CrowdStrikePrivateLinkEndpointProps:
    def __init__(
        self,
        *,
        crowd_strike_cloud: CrowdStrikeCloud,
        subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        peeredwith_nlb: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param crowd_strike_cloud: 
        :param subnets: 
        :param vpc: (experimental) The EC2 Instance that will be udpated.
        :param peeredwith_nlb: 

        :stability: experimental
        '''
        if isinstance(subnets, dict):
            subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b3143e444bbe53e85b4eab676b8d8eb69dbd2e215a845dee1dd765d79206a2)
            check_type(argname="argument crowd_strike_cloud", value=crowd_strike_cloud, expected_type=type_hints["crowd_strike_cloud"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument peeredwith_nlb", value=peeredwith_nlb, expected_type=type_hints["peeredwith_nlb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crowd_strike_cloud": crowd_strike_cloud,
            "subnets": subnets,
            "vpc": vpc,
        }
        if peeredwith_nlb is not None:
            self._values["peeredwith_nlb"] = peeredwith_nlb

    @builtins.property
    def crowd_strike_cloud(self) -> CrowdStrikeCloud:
        '''
        :stability: experimental
        '''
        result = self._values.get("crowd_strike_cloud")
        assert result is not None, "Required property 'crowd_strike_cloud' is missing"
        return typing.cast(CrowdStrikeCloud, result)

    @builtins.property
    def subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''(experimental) The EC2 Instance that will be udpated.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc], result)

    @builtins.property
    def peeredwith_nlb(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("peeredwith_nlb")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrowdStrikePrivateLinkEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="raindancers-network.crowdstrike.CrowdStrikeRegion")
class CrowdStrikeRegion(enum.Enum):
    '''
    :stability: experimental
    '''

    US_WEST_1 = "US_WEST_1"
    '''
    :stability: experimental
    '''
    US_WEST_2 = "US_WEST_2"
    '''
    :stability: experimental
    '''
    EU_CENTRAL_1 = "EU_CENTRAL_1"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="raindancers-network.crowdstrike.CrowdStrikeServices",
    jsii_struct_bases=[],
    name_mapping={
        "aws_region": "awsRegion",
        "download_server": "downloadServer",
        "sensor_proxy": "sensorProxy",
    },
)
class CrowdStrikeServices:
    def __init__(
        self,
        *,
        aws_region: CrowdStrikeRegion,
        download_server: typing.Union["Endpoint", typing.Dict[builtins.str, typing.Any]],
        sensor_proxy: typing.Union["Endpoint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param aws_region: 
        :param download_server: 
        :param sensor_proxy: 

        :stability: experimental
        '''
        if isinstance(download_server, dict):
            download_server = Endpoint(**download_server)
        if isinstance(sensor_proxy, dict):
            sensor_proxy = Endpoint(**sensor_proxy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9d7cdd9089f2ffd7cfa858761027dba5f729a968f669e462e907eb817fb5e9)
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument download_server", value=download_server, expected_type=type_hints["download_server"])
            check_type(argname="argument sensor_proxy", value=sensor_proxy, expected_type=type_hints["sensor_proxy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_region": aws_region,
            "download_server": download_server,
            "sensor_proxy": sensor_proxy,
        }

    @builtins.property
    def aws_region(self) -> CrowdStrikeRegion:
        '''
        :stability: experimental
        '''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(CrowdStrikeRegion, result)

    @builtins.property
    def download_server(self) -> "Endpoint":
        '''
        :stability: experimental
        '''
        result = self._values.get("download_server")
        assert result is not None, "Required property 'download_server' is missing"
        return typing.cast("Endpoint", result)

    @builtins.property
    def sensor_proxy(self) -> "Endpoint":
        '''
        :stability: experimental
        '''
        result = self._values.get("sensor_proxy")
        assert result is not None, "Required property 'sensor_proxy' is missing"
        return typing.cast("Endpoint", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrowdStrikeServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.crowdstrike.Endpoint",
    jsii_struct_bases=[],
    name_mapping={"dns_name": "dnsName", "vpc_endpoint_name": "vpcEndpointName"},
)
class Endpoint:
    def __init__(
        self,
        *,
        dns_name: builtins.str,
        vpc_endpoint_name: builtins.str,
    ) -> None:
        '''
        :param dns_name: 
        :param vpc_endpoint_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e22ba1c2077d379e2fed49d74359e1adfc57dbfa4bdc8d7140a52e758675f89)
            check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
            check_type(argname="argument vpc_endpoint_name", value=vpc_endpoint_name, expected_type=type_hints["vpc_endpoint_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_name": dns_name,
            "vpc_endpoint_name": vpc_endpoint_name,
        }

    @builtins.property
    def dns_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("dns_name")
        assert result is not None, "Required property 'dns_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_endpoint_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc_endpoint_name")
        assert result is not None, "Required property 'vpc_endpoint_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Endpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.crowdstrike.VpcRegionId",
    jsii_struct_bases=[],
    name_mapping={
        "peering_vpc_id": "peeringVpcId",
        "peer_vpc_region": "peerVpcRegion",
    },
)
class VpcRegionId:
    def __init__(
        self,
        *,
        peering_vpc_id: builtins.str,
        peer_vpc_region: builtins.str,
    ) -> None:
        '''
        :param peering_vpc_id: 
        :param peer_vpc_region: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89712e9493e369f20a1a9d390768889d9774437046b9940c0ade3d8c185d1db)
            check_type(argname="argument peering_vpc_id", value=peering_vpc_id, expected_type=type_hints["peering_vpc_id"])
            check_type(argname="argument peer_vpc_region", value=peer_vpc_region, expected_type=type_hints["peer_vpc_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peering_vpc_id": peering_vpc_id,
            "peer_vpc_region": peer_vpc_region,
        }

    @builtins.property
    def peering_vpc_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("peering_vpc_id")
        assert result is not None, "Required property 'peering_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_vpc_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("peer_vpc_region")
        assert result is not None, "Required property 'peer_vpc_region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcRegionId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CrowdStrikeCloud",
    "CrowdStrikeExtendedEndpoint",
    "CrowdStrikeExtendedEndpointProps",
    "CrowdStrikeNLB",
    "CrowdStrikeNLBProps",
    "CrowdStrikePrivateLink",
    "CrowdStrikePrivateLinkEndpoint",
    "CrowdStrikePrivateLinkEndpointProps",
    "CrowdStrikeRegion",
    "CrowdStrikeServices",
    "Endpoint",
    "VpcRegionId",
]

publication.publish()

def _typecheckingstub__57ff544863099fe7ea4efc06cb7118e4451593edb21ee5d916921793ea6da24b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    crowdstrike_cloud: CrowdStrikeCloud,
    peering_vpc: typing.Optional[typing.Union[VpcRegionId, typing.Dict[builtins.str, typing.Any]]] = None,
    use_elb_in_peered_vpc: typing.Optional[builtins.bool] = None,
    vpccidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aa18b77860bc37384c047078ec7f28782acbc3d735bb812f5d6700bac5e671(
    *,
    crowdstrike_cloud: CrowdStrikeCloud,
    peering_vpc: typing.Optional[typing.Union[VpcRegionId, typing.Dict[builtins.str, typing.Any]]] = None,
    use_elb_in_peered_vpc: typing.Optional[builtins.bool] = None,
    vpccidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ebec4a9b78326a3d1168516dd8675cb18751b5623134c74652b9e6786d5613(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    crowdstrike_region: CrowdStrikeCloud,
    download: builtins.str,
    downloadhosted_zone: builtins.str,
    downloadhosted_zone_name: builtins.str,
    proxy: builtins.str,
    proxyhosted_zone: builtins.str,
    proxyhosted_zone_name: builtins.str,
    region: builtins.str,
    routeresolver_endpoints: _R53Resolverendpoints_5d3b063e,
    subnet_group_name: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d308ba88b22248f14a2ebf2b44beb884bdd3e50edb3e33ca8efcb6d7f99c9e9(
    *,
    crowdstrike_region: CrowdStrikeCloud,
    download: builtins.str,
    downloadhosted_zone: builtins.str,
    downloadhosted_zone_name: builtins.str,
    proxy: builtins.str,
    proxyhosted_zone: builtins.str,
    proxyhosted_zone_name: builtins.str,
    region: builtins.str,
    routeresolver_endpoints: _R53Resolverendpoints_5d3b063e,
    subnet_group_name: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b87a4b8466e3b5c05d5057d01bf7de72238b154f6db6c4c5bcd5da87365ae53(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    crowd_strike_cloud: CrowdStrikeCloud,
    subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    peeredwith_nlb: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025278ee7968de6176be8fd3a5b46db52bac7d3f189f6dc828c65a15b2b6a815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18475e3ec120a2180a0e9549b0540e83d03c6ffd390b6894b6b67f5bbbcb034f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918c30f4bc8924820476fd3d5f3f6c696079cfc423eae7584cc72e009e4df6af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f637ea673ce2c556e14ba951f8050c698addacfe8329f5bfd581d351c2acf792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8bc0d12617220caed347f53c95585ecb3e97f8cef27bca52892d67712d69bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168ecb49b2a288cce769bac40363cb02515170d6af49c6b79c2b70f4a0474152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b3143e444bbe53e85b4eab676b8d8eb69dbd2e215a845dee1dd765d79206a2(
    *,
    crowd_strike_cloud: CrowdStrikeCloud,
    subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    peeredwith_nlb: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9d7cdd9089f2ffd7cfa858761027dba5f729a968f669e462e907eb817fb5e9(
    *,
    aws_region: CrowdStrikeRegion,
    download_server: typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]],
    sensor_proxy: typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e22ba1c2077d379e2fed49d74359e1adfc57dbfa4bdc8d7140a52e758675f89(
    *,
    dns_name: builtins.str,
    vpc_endpoint_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89712e9493e369f20a1a9d390768889d9774437046b9940c0ade3d8c185d1db(
    *,
    peering_vpc_id: builtins.str,
    peer_vpc_region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
