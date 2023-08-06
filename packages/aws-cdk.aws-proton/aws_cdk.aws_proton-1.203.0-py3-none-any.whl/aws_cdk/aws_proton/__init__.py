'''
# AWS::Proton Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_proton as proton
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Proton construct libraries](https://constructs.dev/search?q=proton)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Proton resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Proton.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Proton](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Proton.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEnvironmentAccountConnection(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-proton.CfnEnvironmentAccountConnection",
):
    '''A CloudFormation ``AWS::Proton::EnvironmentAccountConnection``.

    Detailed data of an AWS Proton environment account connection resource.

    :cloudformationResource: AWS::Proton::EnvironmentAccountConnection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_proton as proton
        
        cfn_environment_account_connection = proton.CfnEnvironmentAccountConnection(self, "MyCfnEnvironmentAccountConnection",
            codebuild_role_arn="codebuildRoleArn",
            component_role_arn="componentRoleArn",
            environment_account_id="environmentAccountId",
            environment_name="environmentName",
            management_account_id="managementAccountId",
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        codebuild_role_arn: typing.Optional[builtins.str] = None,
        component_role_arn: typing.Optional[builtins.str] = None,
        environment_account_id: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        management_account_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Proton::EnvironmentAccountConnection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param codebuild_role_arn: The Amazon Resource Name (ARN) of an IAM service role in the environment account. AWS Proton uses this role to provision infrastructure resources using CodeBuild-based provisioning in the associated environment account.
        :param component_role_arn: The Amazon Resource Name (ARN) of the IAM service role that AWS Proton uses when provisioning directly defined components in the associated environment account. It determines the scope of infrastructure that a component can provision in the account. The environment account connection must have a ``componentRoleArn`` to allow directly defined components to be associated with any environments running in the account. For more information about components, see `AWS Proton components <https://docs.aws.amazon.com/proton/latest/userguide/ag-components.html>`_ in the *AWS Proton User Guide* .
        :param environment_account_id: The environment account that's connected to the environment account connection.
        :param environment_name: The name of the environment that's associated with the environment account connection.
        :param management_account_id: The ID of the management account that's connected to the environment account connection.
        :param role_arn: The IAM service role that's associated with the environment account connection.
        :param tags: An optional list of metadata items that you can associate with the AWS Proton environment account connection. A tag is a key-value pair. For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a6d4c6671b56ecc04d7197eb1e38698fda11c9e65177518f342026548913d7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentAccountConnectionProps(
            codebuild_role_arn=codebuild_role_arn,
            component_role_arn=component_role_arn,
            environment_account_id=environment_account_id,
            environment_name=environment_name,
            management_account_id=management_account_id,
            role_arn=role_arn,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8aff6e0039ef7f232880d92644d865e4dfb91a6fb1f1239cd727468aff27e10)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c41497d2eac9a295e048a45b61675336bc9c66c74cc075107abf82d5110fef)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''Returns the environment account connection ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Returns the environment account connection ID.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Returns the environment account connection status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An optional list of metadata items that you can associate with the AWS Proton environment account connection.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="codebuildRoleArn")
    def codebuild_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM service role in the environment account.

        AWS Proton uses this role to provision infrastructure resources using CodeBuild-based provisioning in the associated environment account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-codebuildrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codebuildRoleArn"))

    @codebuild_role_arn.setter
    def codebuild_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0611ac8430da9e4684bfaab74b6ffc5e244bf7726fffe5afbba3632c2ee02fe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codebuildRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="componentRoleArn")
    def component_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM service role that AWS Proton uses when provisioning directly defined components in the associated environment account.

        It determines the scope of infrastructure that a component can provision in the account.

        The environment account connection must have a ``componentRoleArn`` to allow directly defined components to be associated with any environments running in the account.

        For more information about components, see `AWS Proton components <https://docs.aws.amazon.com/proton/latest/userguide/ag-components.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-componentrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentRoleArn"))

    @component_role_arn.setter
    def component_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465bacf93a19e18487079f186a5705fb112f97af5ef46c7d61440dec4b9a4a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="environmentAccountId")
    def environment_account_id(self) -> typing.Optional[builtins.str]:
        '''The environment account that's connected to the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-environmentaccountid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentAccountId"))

    @environment_account_id.setter
    def environment_account_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8210b2aa7ffc0309b5f143cdac879fdaa49b7643118f685fa6acddd892c812a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment that's associated with the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-environmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentName"))

    @environment_name.setter
    def environment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0991f065c3842a294181694e544a26479b79c47d51aaf0a477fb867b26da1ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentName", value)

    @builtins.property
    @jsii.member(jsii_name="managementAccountId")
    def management_account_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the management account that's connected to the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-managementaccountid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementAccountId"))

    @management_account_id.setter
    def management_account_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e996a42f88d6266e6f5af308c2740c765d0c26d4a3abd5bd5cfd7d34c12829c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM service role that's associated with the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982f9a3f2d88375edf627b04f5cbf151563061d7b9936f66ae456978e4da83fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-proton.CfnEnvironmentAccountConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "codebuild_role_arn": "codebuildRoleArn",
        "component_role_arn": "componentRoleArn",
        "environment_account_id": "environmentAccountId",
        "environment_name": "environmentName",
        "management_account_id": "managementAccountId",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnEnvironmentAccountConnectionProps:
    def __init__(
        self,
        *,
        codebuild_role_arn: typing.Optional[builtins.str] = None,
        component_role_arn: typing.Optional[builtins.str] = None,
        environment_account_id: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        management_account_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironmentAccountConnection``.

        :param codebuild_role_arn: The Amazon Resource Name (ARN) of an IAM service role in the environment account. AWS Proton uses this role to provision infrastructure resources using CodeBuild-based provisioning in the associated environment account.
        :param component_role_arn: The Amazon Resource Name (ARN) of the IAM service role that AWS Proton uses when provisioning directly defined components in the associated environment account. It determines the scope of infrastructure that a component can provision in the account. The environment account connection must have a ``componentRoleArn`` to allow directly defined components to be associated with any environments running in the account. For more information about components, see `AWS Proton components <https://docs.aws.amazon.com/proton/latest/userguide/ag-components.html>`_ in the *AWS Proton User Guide* .
        :param environment_account_id: The environment account that's connected to the environment account connection.
        :param environment_name: The name of the environment that's associated with the environment account connection.
        :param management_account_id: The ID of the management account that's connected to the environment account connection.
        :param role_arn: The IAM service role that's associated with the environment account connection.
        :param tags: An optional list of metadata items that you can associate with the AWS Proton environment account connection. A tag is a key-value pair. For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_proton as proton
            
            cfn_environment_account_connection_props = proton.CfnEnvironmentAccountConnectionProps(
                codebuild_role_arn="codebuildRoleArn",
                component_role_arn="componentRoleArn",
                environment_account_id="environmentAccountId",
                environment_name="environmentName",
                management_account_id="managementAccountId",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee8ad0e08a5a4c87e2d2a02b491da89e26c4f51b70ccf5fc7f705b439be7f51)
            check_type(argname="argument codebuild_role_arn", value=codebuild_role_arn, expected_type=type_hints["codebuild_role_arn"])
            check_type(argname="argument component_role_arn", value=component_role_arn, expected_type=type_hints["component_role_arn"])
            check_type(argname="argument environment_account_id", value=environment_account_id, expected_type=type_hints["environment_account_id"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument management_account_id", value=management_account_id, expected_type=type_hints["management_account_id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if codebuild_role_arn is not None:
            self._values["codebuild_role_arn"] = codebuild_role_arn
        if component_role_arn is not None:
            self._values["component_role_arn"] = component_role_arn
        if environment_account_id is not None:
            self._values["environment_account_id"] = environment_account_id
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if management_account_id is not None:
            self._values["management_account_id"] = management_account_id
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def codebuild_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM service role in the environment account.

        AWS Proton uses this role to provision infrastructure resources using CodeBuild-based provisioning in the associated environment account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-codebuildrolearn
        '''
        result = self._values.get("codebuild_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM service role that AWS Proton uses when provisioning directly defined components in the associated environment account.

        It determines the scope of infrastructure that a component can provision in the account.

        The environment account connection must have a ``componentRoleArn`` to allow directly defined components to be associated with any environments running in the account.

        For more information about components, see `AWS Proton components <https://docs.aws.amazon.com/proton/latest/userguide/ag-components.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-componentrolearn
        '''
        result = self._values.get("component_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_account_id(self) -> typing.Optional[builtins.str]:
        '''The environment account that's connected to the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-environmentaccountid
        '''
        result = self._values.get("environment_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment that's associated with the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management_account_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the management account that's connected to the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-managementaccountid
        '''
        result = self._values.get("management_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM service role that's associated with the environment account connection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An optional list of metadata items that you can associate with the AWS Proton environment account connection.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentAccountConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEnvironmentTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-proton.CfnEnvironmentTemplate",
):
    '''A CloudFormation ``AWS::Proton::EnvironmentTemplate``.

    Create an environment template for AWS Proton . For more information, see `Environment Templates <https://docs.aws.amazon.com/proton/latest/userguide/ag-templates.html>`_ in the *AWS Proton User Guide* .

    You can create an environment template in one of the two following ways:

    - Register and publish a *standard* environment template that instructs AWS Proton to deploy and manage environment infrastructure.
    - Register and publish a *customer managed* environment template that connects AWS Proton to your existing provisioned infrastructure that you manage. AWS Proton *doesn't* manage your existing provisioned infrastructure. To create an environment template for customer provisioned and managed infrastructure, include the ``provisioning`` parameter and set the value to ``CUSTOMER_MANAGED`` . For more information, see `Register and publish an environment template <https://docs.aws.amazon.com/proton/latest/userguide/template-create.html>`_ in the *AWS Proton User Guide* .

    :cloudformationResource: AWS::Proton::EnvironmentTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_proton as proton
        
        cfn_environment_template = proton.CfnEnvironmentTemplate(self, "MyCfnEnvironmentTemplate",
            description="description",
            display_name="displayName",
            encryption_key="encryptionKey",
            name="name",
            provisioning="provisioning",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Proton::EnvironmentTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the environment template.
        :param display_name: The name of the environment template as displayed in the developer interface.
        :param encryption_key: The customer provided encryption key for the environment template.
        :param name: The name of the environment template.
        :param provisioning: When included, indicates that the environment template is for customer provisioned and managed infrastructure.
        :param tags: An optional list of metadata items that you can associate with the AWS Proton environment template. A tag is a key-value pair. For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81a66f89340ad61489b1bac1205b85ba23f29b3850852be2d8134c7fa0d89d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentTemplateProps(
            description=description,
            display_name=display_name,
            encryption_key=encryption_key,
            name=name,
            provisioning=provisioning,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c238f806002158a5dc2f901c5987579b4a26fe6150761c69821f9ac0a095ca)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444e8195d72ab2ec569395826e5f2e6abde3cbb004851ea7f7b123f46c7ec23a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''Returns the ARN of the environment template.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An optional list of metadata items that you can associate with the AWS Proton environment template.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdbf9e7a89857749ff2393ed208f597564b9fc197fb8155847b4ac696aeab31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment template as displayed in the developer interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2d120d698d52933fefedb8c4666eeac114557dd876a34d399c1e8a0f24933e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer provided encryption key for the environment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-encryptionkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50eb083721a0248e9e114aaf10dfdf8dc923bc03f08aca101c837fa8b2b6e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa11a20b5786e9679cd51e3382a01ad54378c7e90818224732ba3d63c3c0bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="provisioning")
    def provisioning(self) -> typing.Optional[builtins.str]:
        '''When included, indicates that the environment template is for customer provisioned and managed infrastructure.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-provisioning
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisioning"))

    @provisioning.setter
    def provisioning(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3feeffdc8867b80a1e1218bdfe4d3d1aed78c8bdef111992963aede869f188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioning", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-proton.CfnEnvironmentTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "encryption_key": "encryptionKey",
        "name": "name",
        "provisioning": "provisioning",
        "tags": "tags",
    },
)
class CfnEnvironmentTemplateProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironmentTemplate``.

        :param description: A description of the environment template.
        :param display_name: The name of the environment template as displayed in the developer interface.
        :param encryption_key: The customer provided encryption key for the environment template.
        :param name: The name of the environment template.
        :param provisioning: When included, indicates that the environment template is for customer provisioned and managed infrastructure.
        :param tags: An optional list of metadata items that you can associate with the AWS Proton environment template. A tag is a key-value pair. For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_proton as proton
            
            cfn_environment_template_props = proton.CfnEnvironmentTemplateProps(
                description="description",
                display_name="displayName",
                encryption_key="encryptionKey",
                name="name",
                provisioning="provisioning",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1d07fbe9ee56cbebad284b4849e9a774fc74ee84fcdb8784ee0484560f8f5b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provisioning", value=provisioning, expected_type=type_hints["provisioning"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if name is not None:
            self._values["name"] = name
        if provisioning is not None:
            self._values["provisioning"] = provisioning
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment template as displayed in the developer interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer provided encryption key for the environment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning(self) -> typing.Optional[builtins.str]:
        '''When included, indicates that the environment template is for customer provisioned and managed infrastructure.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-provisioning
        '''
        result = self._values.get("provisioning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An optional list of metadata items that you can associate with the AWS Proton environment template.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnServiceTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-proton.CfnServiceTemplate",
):
    '''A CloudFormation ``AWS::Proton::ServiceTemplate``.

    Create a service template. The administrator creates a service template to define standardized infrastructure and an optional CI/CD service pipeline. Developers, in turn, select the service template from AWS Proton . If the selected service template includes a service pipeline definition, they provide a link to their source code repository. AWS Proton then deploys and manages the infrastructure defined by the selected service template. For more information, see `AWS Proton templates <https://docs.aws.amazon.com/proton/latest/userguide/ag-templates.html>`_ in the *AWS Proton User Guide* .

    :cloudformationResource: AWS::Proton::ServiceTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_proton as proton
        
        cfn_service_template = proton.CfnServiceTemplate(self, "MyCfnServiceTemplate",
            description="description",
            display_name="displayName",
            encryption_key="encryptionKey",
            name="name",
            pipeline_provisioning="pipelineProvisioning",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pipeline_provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Proton::ServiceTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the service template.
        :param display_name: The service template name as displayed in the developer interface.
        :param encryption_key: The customer provided service template encryption key that's used to encrypt data.
        :param name: The name of the service template.
        :param pipeline_provisioning: If ``pipelineProvisioning`` is ``true`` , a service pipeline is included in the service template. Otherwise, a service pipeline *isn't* included in the service template.
        :param tags: An object that includes the template bundle S3 bucket path and name for the new version of a service template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32a56ae45b722ff52f4acd0824b8be6d4c299bf230d333d4f5a3509de5b1a7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceTemplateProps(
            description=description,
            display_name=display_name,
            encryption_key=encryption_key,
            name=name,
            pipeline_provisioning=pipeline_provisioning,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d7c383043af20f76ff8bbf00419d46dda60ce55d54c928c6d261a02075fac3)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf2b3d66dc1f05dbab2255bba7a4000a4efc23b4104df9aa8da3fae51bebd75)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''Returns the service template ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3714233ac1b0d424ba636215d5a1e296a640b0020c8012a6a3f557f1534cb588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The service template name as displayed in the developer interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c107e58fcf7465fdfb94e7617db1e2f0a457d646b49206fc6f1b0f76695e279e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer provided service template encryption key that's used to encrypt data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-encryptionkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5e3838ca63a5f70d2bf6f67074c84b0945f8f80011a3567db1535534df30c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585f56b7aae23a0b9dab004e3ffa0d14ef46fcc0e55fffeb62ea3d2582074bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineProvisioning")
    def pipeline_provisioning(self) -> typing.Optional[builtins.str]:
        '''If ``pipelineProvisioning`` is ``true`` , a service pipeline is included in the service template.

        Otherwise, a service pipeline *isn't* included in the service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-pipelineprovisioning
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipelineProvisioning"))

    @pipeline_provisioning.setter
    def pipeline_provisioning(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc743068ffb392dbfa9aa0d1a7dadd2db9aa5b5ae1145dd8b00ce173daaa1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineProvisioning", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-proton.CfnServiceTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "encryption_key": "encryptionKey",
        "name": "name",
        "pipeline_provisioning": "pipelineProvisioning",
        "tags": "tags",
    },
)
class CfnServiceTemplateProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pipeline_provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceTemplate``.

        :param description: A description of the service template.
        :param display_name: The service template name as displayed in the developer interface.
        :param encryption_key: The customer provided service template encryption key that's used to encrypt data.
        :param name: The name of the service template.
        :param pipeline_provisioning: If ``pipelineProvisioning`` is ``true`` , a service pipeline is included in the service template. Otherwise, a service pipeline *isn't* included in the service template.
        :param tags: An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_proton as proton
            
            cfn_service_template_props = proton.CfnServiceTemplateProps(
                description="description",
                display_name="displayName",
                encryption_key="encryptionKey",
                name="name",
                pipeline_provisioning="pipelineProvisioning",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e11956eb0827b1043f5c20e858117b4596079164b595fb6e03b4c83de894b0f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pipeline_provisioning", value=pipeline_provisioning, expected_type=type_hints["pipeline_provisioning"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if name is not None:
            self._values["name"] = name
        if pipeline_provisioning is not None:
            self._values["pipeline_provisioning"] = pipeline_provisioning
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The service template name as displayed in the developer interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer provided service template encryption key that's used to encrypt data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_provisioning(self) -> typing.Optional[builtins.str]:
        '''If ``pipelineProvisioning`` is ``true`` , a service pipeline is included in the service template.

        Otherwise, a service pipeline *isn't* included in the service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-pipelineprovisioning
        '''
        result = self._values.get("pipeline_provisioning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnEnvironmentAccountConnection",
    "CfnEnvironmentAccountConnectionProps",
    "CfnEnvironmentTemplate",
    "CfnEnvironmentTemplateProps",
    "CfnServiceTemplate",
    "CfnServiceTemplateProps",
]

publication.publish()

def _typecheckingstub__93a6d4c6671b56ecc04d7197eb1e38698fda11c9e65177518f342026548913d7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    codebuild_role_arn: typing.Optional[builtins.str] = None,
    component_role_arn: typing.Optional[builtins.str] = None,
    environment_account_id: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    management_account_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8aff6e0039ef7f232880d92644d865e4dfb91a6fb1f1239cd727468aff27e10(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c41497d2eac9a295e048a45b61675336bc9c66c74cc075107abf82d5110fef(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0611ac8430da9e4684bfaab74b6ffc5e244bf7726fffe5afbba3632c2ee02fe9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465bacf93a19e18487079f186a5705fb112f97af5ef46c7d61440dec4b9a4a44(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8210b2aa7ffc0309b5f143cdac879fdaa49b7643118f685fa6acddd892c812a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0991f065c3842a294181694e544a26479b79c47d51aaf0a477fb867b26da1ccd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e996a42f88d6266e6f5af308c2740c765d0c26d4a3abd5bd5cfd7d34c12829c9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982f9a3f2d88375edf627b04f5cbf151563061d7b9936f66ae456978e4da83fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee8ad0e08a5a4c87e2d2a02b491da89e26c4f51b70ccf5fc7f705b439be7f51(
    *,
    codebuild_role_arn: typing.Optional[builtins.str] = None,
    component_role_arn: typing.Optional[builtins.str] = None,
    environment_account_id: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    management_account_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81a66f89340ad61489b1bac1205b85ba23f29b3850852be2d8134c7fa0d89d9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c238f806002158a5dc2f901c5987579b4a26fe6150761c69821f9ac0a095ca(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444e8195d72ab2ec569395826e5f2e6abde3cbb004851ea7f7b123f46c7ec23a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdbf9e7a89857749ff2393ed208f597564b9fc197fb8155847b4ac696aeab31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2d120d698d52933fefedb8c4666eeac114557dd876a34d399c1e8a0f24933e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50eb083721a0248e9e114aaf10dfdf8dc923bc03f08aca101c837fa8b2b6e30(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa11a20b5786e9679cd51e3382a01ad54378c7e90818224732ba3d63c3c0bdc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3feeffdc8867b80a1e1218bdfe4d3d1aed78c8bdef111992963aede869f188(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1d07fbe9ee56cbebad284b4849e9a774fc74ee84fcdb8784ee0484560f8f5b(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32a56ae45b722ff52f4acd0824b8be6d4c299bf230d333d4f5a3509de5b1a7d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pipeline_provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d7c383043af20f76ff8bbf00419d46dda60ce55d54c928c6d261a02075fac3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf2b3d66dc1f05dbab2255bba7a4000a4efc23b4104df9aa8da3fae51bebd75(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3714233ac1b0d424ba636215d5a1e296a640b0020c8012a6a3f557f1534cb588(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c107e58fcf7465fdfb94e7617db1e2f0a457d646b49206fc6f1b0f76695e279e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5e3838ca63a5f70d2bf6f67074c84b0945f8f80011a3567db1535534df30c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585f56b7aae23a0b9dab004e3ffa0d14ef46fcc0e55fffeb62ea3d2582074bd6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc743068ffb392dbfa9aa0d1a7dadd2db9aa5b5ae1145dd8b00ce173daaa1cc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e11956eb0827b1043f5c20e858117b4596079164b595fb6e03b4c83de894b0f(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pipeline_provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
