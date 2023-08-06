'''
# AWS::Proton Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as proton
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnEnvironmentAccountConnection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_proton.CfnEnvironmentAccountConnection",
):
    '''A CloudFormation ``AWS::Proton::EnvironmentAccountConnection``.

    Detailed data of an AWS Proton environment account connection resource.

    :cloudformationResource: AWS::Proton::EnvironmentAccountConnection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_proton as proton
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        codebuild_role_arn: typing.Optional[builtins.str] = None,
        component_role_arn: typing.Optional[builtins.str] = None,
        environment_account_id: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        management_account_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d0e1bbabfb831ee8218e9c9439329eb479e52d16bb543f1e48047460fe568f2)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e740c9c3c1acf3fa1f1d3dd6b41c2b4b38a990766f5fb7577fddbff76d52b05b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__010edc2053d1882911ece27afe48cd6b01b7ddbecfc939838733a5f9fea9f1ae)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An optional list of metadata items that you can associate with the AWS Proton environment account connection.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c2ff159f18ededa0548e9501c8799e1086fa1866437ea644c57e066fd5075a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63a7d2d8a83dbe1ee2506e11f853fb94f6119d624d00121a6398c8b1c2d02cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb8c2e8d8d5f46d4607ebe69bccfe7bf3008e679bdbd03c4b85ac5a625730708)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f394b071c64b4c0329a14a9ba3c3b8967f74102df930be4551ffa5057cc044f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f3dc7cea215c5b781f73493a3c2bf0b620e302b2d2454f84323522615e36801)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9881878eb3238b97e9b37446318f7168761cdc9e31f47a5f3d840a4ba7e22ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_proton.CfnEnvironmentAccountConnectionProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_proton as proton
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4db46f1f31ab6a5ba31dfe2582f40073d2e86afc0e1354d305fc89a69465b1d)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An optional list of metadata items that you can associate with the AWS Proton environment account connection.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentAccountConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEnvironmentTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_proton.CfnEnvironmentTemplate",
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
        from monocdk import aws_proton as proton
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__96a890573a8b0d9672209f81214b2107b7a537bc959a958c1e2e9a88953856fd)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91291a3fa6f830d402e52891a074a7c3091fbe45912c77d8df6ddaca32658b6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0781110631a440bd54dd988aa23e7b281ac6b6f1d93339b37a14c309ca165679)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An optional list of metadata items that you can associate with the AWS Proton environment template.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5dd6bf2c9a98b429f5cfdeaabce7e8fa5b2bfae0c14cfc9cd28b85d0d1911119)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea09ecbfb991c1f462ad16ed01c7fd49394bc27c41b11c63c21c42d1d10f64e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e532fa4869d019a8be81d948e2231d1bce024415cc42652060b996cdaa4d677)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ba77bc60f04d06f37e50889d024faa0dd7f9bc6ab58576ea7d2e56657c49256)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4ec04d545ad21d7ca1c5f40418ee3946900a66035e0842bd6b56109879ee2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioning", value)


@jsii.data_type(
    jsii_type="monocdk.aws_proton.CfnEnvironmentTemplateProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_proton as proton
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d651f3d5180c0dbbe3c5d1c713b9c48db80dc908c8981d4e0044fb4092599a6)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An optional list of metadata items that you can associate with the AWS Proton environment template.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_proton.CfnServiceTemplate",
):
    '''A CloudFormation ``AWS::Proton::ServiceTemplate``.

    Create a service template. The administrator creates a service template to define standardized infrastructure and an optional CI/CD service pipeline. Developers, in turn, select the service template from AWS Proton . If the selected service template includes a service pipeline definition, they provide a link to their source code repository. AWS Proton then deploys and manages the infrastructure defined by the selected service template. For more information, see `AWS Proton templates <https://docs.aws.amazon.com/proton/latest/userguide/ag-templates.html>`_ in the *AWS Proton User Guide* .

    :cloudformationResource: AWS::Proton::ServiceTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_proton as proton
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pipeline_provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cd89ec5ad2f177e2f0fac204d0b4bb3479f195cfdc7293f0d8007612fe46349)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305fce3574880a595bc252a8d57bb0b3be1ea6aca6b953b4f4f3b9329c48b3e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6c8a08294e61600f0153154587be0cbbfaf40dfe70e93f5f6dd58ab383a811a)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a03e52c8b1fba9d820d54607c8c7f4f291b364d065fdc49fc53a12f4f29ae17b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b5dac0a8c2971be2dff116d0bc79e14dbff01803c3082bf221b4d1c539db53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3f1a6c5623f87e088c0851e166ef7d80bda173a54606c5c8f8241e56129461b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff9bc40d02c0ff5b23409cd05e8295a0727dbfc8ab1f55e9066322f70686d29a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35130a5369ab7e99898fe982561b46077625020ee71fe2f79cb8fb004412321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineProvisioning", value)


@jsii.data_type(
    jsii_type="monocdk.aws_proton.CfnServiceTemplateProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_proton as proton
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__02e713885ceaae6780b30c40b0b6c34d53af6f6fc9b65882a486b060d81b27f5)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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

def _typecheckingstub__6d0e1bbabfb831ee8218e9c9439329eb479e52d16bb543f1e48047460fe568f2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    codebuild_role_arn: typing.Optional[builtins.str] = None,
    component_role_arn: typing.Optional[builtins.str] = None,
    environment_account_id: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    management_account_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e740c9c3c1acf3fa1f1d3dd6b41c2b4b38a990766f5fb7577fddbff76d52b05b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010edc2053d1882911ece27afe48cd6b01b7ddbecfc939838733a5f9fea9f1ae(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c2ff159f18ededa0548e9501c8799e1086fa1866437ea644c57e066fd5075a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63a7d2d8a83dbe1ee2506e11f853fb94f6119d624d00121a6398c8b1c2d02cd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8c2e8d8d5f46d4607ebe69bccfe7bf3008e679bdbd03c4b85ac5a625730708(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f394b071c64b4c0329a14a9ba3c3b8967f74102df930be4551ffa5057cc044f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3dc7cea215c5b781f73493a3c2bf0b620e302b2d2454f84323522615e36801(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9881878eb3238b97e9b37446318f7168761cdc9e31f47a5f3d840a4ba7e22ac3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4db46f1f31ab6a5ba31dfe2582f40073d2e86afc0e1354d305fc89a69465b1d(
    *,
    codebuild_role_arn: typing.Optional[builtins.str] = None,
    component_role_arn: typing.Optional[builtins.str] = None,
    environment_account_id: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    management_account_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a890573a8b0d9672209f81214b2107b7a537bc959a958c1e2e9a88953856fd(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91291a3fa6f830d402e52891a074a7c3091fbe45912c77d8df6ddaca32658b6e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0781110631a440bd54dd988aa23e7b281ac6b6f1d93339b37a14c309ca165679(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd6bf2c9a98b429f5cfdeaabce7e8fa5b2bfae0c14cfc9cd28b85d0d1911119(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea09ecbfb991c1f462ad16ed01c7fd49394bc27c41b11c63c21c42d1d10f64e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e532fa4869d019a8be81d948e2231d1bce024415cc42652060b996cdaa4d677(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba77bc60f04d06f37e50889d024faa0dd7f9bc6ab58576ea7d2e56657c49256(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ec04d545ad21d7ca1c5f40418ee3946900a66035e0842bd6b56109879ee2ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d651f3d5180c0dbbe3c5d1c713b9c48db80dc908c8981d4e0044fb4092599a6(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd89ec5ad2f177e2f0fac204d0b4bb3479f195cfdc7293f0d8007612fe46349(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pipeline_provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305fce3574880a595bc252a8d57bb0b3be1ea6aca6b953b4f4f3b9329c48b3e3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c8a08294e61600f0153154587be0cbbfaf40dfe70e93f5f6dd58ab383a811a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03e52c8b1fba9d820d54607c8c7f4f291b364d065fdc49fc53a12f4f29ae17b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b5dac0a8c2971be2dff116d0bc79e14dbff01803c3082bf221b4d1c539db53(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f1a6c5623f87e088c0851e166ef7d80bda173a54606c5c8f8241e56129461b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9bc40d02c0ff5b23409cd05e8295a0727dbfc8ab1f55e9066322f70686d29a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35130a5369ab7e99898fe982561b46077625020ee71fe2f79cb8fb004412321(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e713885ceaae6780b30c40b0b6c34d53af6f6fc9b65882a486b060d81b27f5(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pipeline_provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
