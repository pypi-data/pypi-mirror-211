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
import aws_cdk.aws_redshift_alpha as _aws_cdk_aws_redshift_alpha_9727f5af
import constructs as _constructs_77d1e7e8


class PrivateRedshiftCluster(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.redshift.PrivateRedshiftCluster",
):
    '''(experimental) * Creates a PrivateRedShiftCluster.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster_name: builtins.str,
        defaultrole: _aws_cdk_aws_iam_ceddda9d.Role,
        logging: typing.Union[_aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties, typing.Dict[builtins.str, typing.Any]],
        master_user: builtins.str,
        subnet_group: _aws_cdk_aws_redshift_alpha_9727f5af.ClusterSubnetGroup,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        default_db_name: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[jsii.Number] = None,
        node_type: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.NodeType] = None,
        parameter_group: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_name: 
        :param defaultrole: 
        :param logging: 
        :param master_user: 
        :param subnet_group: 
        :param vpc: 
        :param default_db_name: 
        :param nodes: 
        :param node_type: 
        :param parameter_group: 
        :param preferred_maintenance_window: 
        :param removal_policy: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ac953f6cac26733ac8098073d9ba550685a37793a2bfa436c053a6b172c17c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RedshiftClusterProps(
            cluster_name=cluster_name,
            defaultrole=defaultrole,
            logging=logging,
            master_user=master_user,
            subnet_group=subnet_group,
            vpc=vpc,
            default_db_name=default_db_name,
            nodes=nodes,
            node_type=node_type,
            parameter_group=parameter_group,
            preferred_maintenance_window=preferred_maintenance_window,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDatabase")
    def add_database(self, database_name: builtins.str) -> "RedShiftDatabase":
        '''
        :param database_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02889c587a80f1d7acc414c8feceba5a6a848dc4fc0b5d9b5edd8472889f9129)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
        return typing.cast("RedShiftDatabase", jsii.invoke(self, "addDatabase", [database_name]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_redshift_alpha_9727f5af.Cluster:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_redshift_alpha_9727f5af.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="clusterParameters")
    def cluster_parameters(
        self,
    ) -> _aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup, jsii.get(self, "clusterParameters"))

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroup")
    def cluster_security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.SecurityGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SecurityGroup, jsii.get(self, "clusterSecurityGroup"))


class RedShiftDatabase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="raindancers-network.redshift.RedShiftDatabase",
):
    '''(experimental) Create a Database in a Redshift Cluster.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_redshift_alpha_9727f5af.Cluster,
        database_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: (experimental) which cluster will the database be created in.
        :param database_name: (experimental) A name for the database.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a47f9f4de95e424a394e8e81b002b7f1fb3b54478ee832788d8e7dd1938aa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RedShiftDatabaseProps(cluster=cluster, database_name=database_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="executeSQLStatement")
    def execute_sql_statement(
        self,
        statement_name: builtins.str,
        sql: builtins.str,
    ) -> None:
        '''
        :param statement_name: -
        :param sql: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85d19186e3c9878e1c2fd3c63119e427764a7808eb2aadf6e1213904389344d)
            check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast(None, jsii.invoke(self, "executeSQLStatement", [statement_name, sql]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_redshift_alpha_9727f5af.Cluster:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_redshift_alpha_9727f5af.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))


@jsii.data_type(
    jsii_type="raindancers-network.redshift.RedShiftDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "database_name": "databaseName"},
)
class RedShiftDatabaseProps:
    def __init__(
        self,
        *,
        cluster: _aws_cdk_aws_redshift_alpha_9727f5af.Cluster,
        database_name: builtins.str,
    ) -> None:
        '''
        :param cluster: (experimental) which cluster will the database be created in.
        :param database_name: (experimental) A name for the database.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570c45d60030ff7d727ecf365725bfecee60260dc435cd679af1851756bdd9f7)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "database_name": database_name,
        }

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_redshift_alpha_9727f5af.Cluster:
        '''(experimental) which cluster will the database be created in.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_redshift_alpha_9727f5af.Cluster, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''(experimental) A name for the database.

        :stability: experimental
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedShiftDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="raindancers-network.redshift.RedshiftClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "defaultrole": "defaultrole",
        "logging": "logging",
        "master_user": "masterUser",
        "subnet_group": "subnetGroup",
        "vpc": "vpc",
        "default_db_name": "defaultDBName",
        "nodes": "nodes",
        "node_type": "nodeType",
        "parameter_group": "parameterGroup",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "removal_policy": "removalPolicy",
    },
)
class RedshiftClusterProps:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        defaultrole: _aws_cdk_aws_iam_ceddda9d.Role,
        logging: typing.Union[_aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties, typing.Dict[builtins.str, typing.Any]],
        master_user: builtins.str,
        subnet_group: _aws_cdk_aws_redshift_alpha_9727f5af.ClusterSubnetGroup,
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
        default_db_name: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[jsii.Number] = None,
        node_type: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.NodeType] = None,
        parameter_group: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param cluster_name: 
        :param defaultrole: 
        :param logging: 
        :param master_user: 
        :param subnet_group: 
        :param vpc: 
        :param default_db_name: 
        :param nodes: 
        :param node_type: 
        :param parameter_group: 
        :param preferred_maintenance_window: 
        :param removal_policy: 

        :stability: experimental
        '''
        if isinstance(logging, dict):
            logging = _aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cfa0c1d830edeb8ac8ce13fec9f2408dd79ffea3610725945fc2dbd8872a276)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument defaultrole", value=defaultrole, expected_type=type_hints["defaultrole"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument master_user", value=master_user, expected_type=type_hints["master_user"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument default_db_name", value=default_db_name, expected_type=type_hints["default_db_name"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument parameter_group", value=parameter_group, expected_type=type_hints["parameter_group"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "defaultrole": defaultrole,
            "logging": logging,
            "master_user": master_user,
            "subnet_group": subnet_group,
            "vpc": vpc,
        }
        if default_db_name is not None:
            self._values["default_db_name"] = default_db_name
        if nodes is not None:
            self._values["nodes"] = nodes
        if node_type is not None:
            self._values["node_type"] = node_type
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def defaultrole(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaultrole")
        assert result is not None, "Required property 'defaultrole' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, result)

    @builtins.property
    def logging(self) -> _aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties:
        '''
        :stability: experimental
        '''
        result = self._values.get("logging")
        assert result is not None, "Required property 'logging' is missing"
        return typing.cast(_aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties, result)

    @builtins.property
    def master_user(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("master_user")
        assert result is not None, "Required property 'master_user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_group(self) -> _aws_cdk_aws_redshift_alpha_9727f5af.ClusterSubnetGroup:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        assert result is not None, "Required property 'subnet_group' is missing"
        return typing.cast(_aws_cdk_aws_redshift_alpha_9727f5af.ClusterSubnetGroup, result)

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
    def default_db_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nodes(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.NodeType]:
        '''
        :stability: experimental
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.NodeType], result)

    @builtins.property
    def parameter_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup]:
        '''
        :stability: experimental
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''
        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedshiftClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PrivateRedshiftCluster",
    "RedShiftDatabase",
    "RedShiftDatabaseProps",
    "RedshiftClusterProps",
]

publication.publish()

def _typecheckingstub__09ac953f6cac26733ac8098073d9ba550685a37793a2bfa436c053a6b172c17c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster_name: builtins.str,
    defaultrole: _aws_cdk_aws_iam_ceddda9d.Role,
    logging: typing.Union[_aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties, typing.Dict[builtins.str, typing.Any]],
    master_user: builtins.str,
    subnet_group: _aws_cdk_aws_redshift_alpha_9727f5af.ClusterSubnetGroup,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    default_db_name: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[jsii.Number] = None,
    node_type: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.NodeType] = None,
    parameter_group: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02889c587a80f1d7acc414c8feceba5a6a848dc4fc0b5d9b5edd8472889f9129(
    database_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a47f9f4de95e424a394e8e81b002b7f1fb3b54478ee832788d8e7dd1938aa1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_redshift_alpha_9727f5af.Cluster,
    database_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85d19186e3c9878e1c2fd3c63119e427764a7808eb2aadf6e1213904389344d(
    statement_name: builtins.str,
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570c45d60030ff7d727ecf365725bfecee60260dc435cd679af1851756bdd9f7(
    *,
    cluster: _aws_cdk_aws_redshift_alpha_9727f5af.Cluster,
    database_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cfa0c1d830edeb8ac8ce13fec9f2408dd79ffea3610725945fc2dbd8872a276(
    *,
    cluster_name: builtins.str,
    defaultrole: _aws_cdk_aws_iam_ceddda9d.Role,
    logging: typing.Union[_aws_cdk_aws_redshift_alpha_9727f5af.LoggingProperties, typing.Dict[builtins.str, typing.Any]],
    master_user: builtins.str,
    subnet_group: _aws_cdk_aws_redshift_alpha_9727f5af.ClusterSubnetGroup,
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IVpc, _aws_cdk_aws_ec2_ceddda9d.Vpc],
    default_db_name: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[jsii.Number] = None,
    node_type: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.NodeType] = None,
    parameter_group: typing.Optional[_aws_cdk_aws_redshift_alpha_9727f5af.ClusterParameterGroup] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass
