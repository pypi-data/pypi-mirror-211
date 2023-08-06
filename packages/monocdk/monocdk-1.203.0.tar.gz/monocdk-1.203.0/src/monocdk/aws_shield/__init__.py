'''
# AWS::Shield Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as shield
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Shield construct libraries](https://constructs.dev/search?q=shield)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Shield resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Shield.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Shield](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Shield.html).

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
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnDRTAccess(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_shield.CfnDRTAccess",
):
    '''A CloudFormation ``AWS::Shield::DRTAccess``.

    Provides permissions for the AWS Shield Advanced Shield response team (SRT) to access your account and your resource protections, to help you mitigate potential distributed denial of service (DDoS) attacks.
    .. epigraph::

       To configure this resource through AWS CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    :cloudformationResource: AWS::Shield::DRTAccess
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_shield as shield
        
        cfn_dRTAccess = shield.CfnDRTAccess(self, "MyCfnDRTAccess",
            role_arn="roleArn",
        
            # the properties below are optional
            log_bucket_list=["logBucketList"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        role_arn: builtins.str,
        log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Shield::DRTAccess``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role_arn: Authorizes the Shield Response Team (SRT) using the specified role, to access your AWS account to assist with DDoS attack mitigation during potential attacks. This enables the SRT to inspect your AWS WAF configuration and logs and to create or update AWS WAF rules and web ACLs. You can associate only one ``RoleArn`` with your subscription. If you submit this update for an account that already has an associated role, the new ``RoleArn`` will replace the existing ``RoleArn`` . This change requires the following: - You must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ . - You must have the ``iam:PassRole`` permission. For more information, see `Granting a user permissions to pass a role to an AWS service <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html>`_ . - The ``AWSShieldDRTAccessPolicy`` managed policy must be attached to the role that you specify in the request. You can access this policy in the IAM console at `AWSShieldDRTAccessPolicy <https://docs.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSShieldDRTAccessPolicy>`_ . For information, see `Adding and removing IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html>`_ . - The role must trust the service principal ``drt.shield.amazonaws.com`` . For information, see `IAM JSON policy elements: Principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`_ . The SRT will have access only to your AWS WAF and Shield resources. By submitting this request, you provide permissions to the SRT to inspect your AWS WAF and Shield configuration and logs, and to create and update AWS WAF rules and web ACLs on your behalf. The SRT takes these actions only if explicitly authorized by you.
        :param log_bucket_list: Authorizes the Shield Response Team (SRT) to access the specified Amazon S3 bucket containing log data such as Application Load Balancer access logs, CloudFront logs, or logs from third party sources. You can associate up to 10 Amazon S3 buckets with your subscription. Use this to share information with the SRT that's not available in AWS WAF logs. To use the services of the SRT, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0790387ac1e3d4d086236e24ad3be3a29fe52ed6e3430c2b02d1526dd73907a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDRTAccessProps(role_arn=role_arn, log_bucket_list=log_bucket_list)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3800aa24ccc3141595c0c8c90c36d936012bb9566dbd04e357288f612febb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0848f2af47f6d9ccdce99ca63f71696e29643936ad2655f3255620d657b6bacd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountId")
    def attr_account_id(self) -> builtins.str:
        '''The ID of the account that submitted the template.

        :cloudformationAttribute: AccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccountId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''Authorizes the Shield Response Team (SRT) using the specified role, to access your AWS account to assist with DDoS attack mitigation during potential attacks.

        This enables the SRT to inspect your AWS WAF configuration and logs and to create or update AWS WAF rules and web ACLs.

        You can associate only one ``RoleArn`` with your subscription. If you submit this update for an account that already has an associated role, the new ``RoleArn`` will replace the existing ``RoleArn`` .

        This change requires the following:

        - You must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .
        - You must have the ``iam:PassRole`` permission. For more information, see `Granting a user permissions to pass a role to an AWS service <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html>`_ .
        - The ``AWSShieldDRTAccessPolicy`` managed policy must be attached to the role that you specify in the request. You can access this policy in the IAM console at `AWSShieldDRTAccessPolicy <https://docs.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSShieldDRTAccessPolicy>`_ . For information, see `Adding and removing IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html>`_ .
        - The role must trust the service principal ``drt.shield.amazonaws.com`` . For information, see `IAM JSON policy elements: Principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`_ .

        The SRT will have access only to your AWS WAF and Shield resources. By submitting this request, you provide permissions to the SRT to inspect your AWS WAF and Shield configuration and logs, and to create and update AWS WAF rules and web ACLs on your behalf. The SRT takes these actions only if explicitly authorized by you.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html#cfn-shield-drtaccess-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a99a0799de23719ec1572626e3b17c0fce82b748f752f6d8c81cdae7c9341cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="logBucketList")
    def log_bucket_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Authorizes the Shield Response Team (SRT) to access the specified Amazon S3 bucket containing log data such as Application Load Balancer access logs, CloudFront logs, or logs from third party sources.

        You can associate up to 10 Amazon S3 buckets with your subscription.

        Use this to share information with the SRT that's not available in AWS WAF logs.

        To use the services of the SRT, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html#cfn-shield-drtaccess-logbucketlist
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logBucketList"))

    @log_bucket_list.setter
    def log_bucket_list(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d1510ad9417ca37ec327868eb91ec02bd3c6777773dc2124e82c6d3a0250d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBucketList", value)


@jsii.data_type(
    jsii_type="monocdk.aws_shield.CfnDRTAccessProps",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "log_bucket_list": "logBucketList"},
)
class CfnDRTAccessProps:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDRTAccess``.

        :param role_arn: Authorizes the Shield Response Team (SRT) using the specified role, to access your AWS account to assist with DDoS attack mitigation during potential attacks. This enables the SRT to inspect your AWS WAF configuration and logs and to create or update AWS WAF rules and web ACLs. You can associate only one ``RoleArn`` with your subscription. If you submit this update for an account that already has an associated role, the new ``RoleArn`` will replace the existing ``RoleArn`` . This change requires the following: - You must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ . - You must have the ``iam:PassRole`` permission. For more information, see `Granting a user permissions to pass a role to an AWS service <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html>`_ . - The ``AWSShieldDRTAccessPolicy`` managed policy must be attached to the role that you specify in the request. You can access this policy in the IAM console at `AWSShieldDRTAccessPolicy <https://docs.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSShieldDRTAccessPolicy>`_ . For information, see `Adding and removing IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html>`_ . - The role must trust the service principal ``drt.shield.amazonaws.com`` . For information, see `IAM JSON policy elements: Principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`_ . The SRT will have access only to your AWS WAF and Shield resources. By submitting this request, you provide permissions to the SRT to inspect your AWS WAF and Shield configuration and logs, and to create and update AWS WAF rules and web ACLs on your behalf. The SRT takes these actions only if explicitly authorized by you.
        :param log_bucket_list: Authorizes the Shield Response Team (SRT) to access the specified Amazon S3 bucket containing log data such as Application Load Balancer access logs, CloudFront logs, or logs from third party sources. You can associate up to 10 Amazon S3 buckets with your subscription. Use this to share information with the SRT that's not available in AWS WAF logs. To use the services of the SRT, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_shield as shield
            
            cfn_dRTAccess_props = shield.CfnDRTAccessProps(
                role_arn="roleArn",
            
                # the properties below are optional
                log_bucket_list=["logBucketList"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d339abc8a5991c44e2d98a0cd39384001e6102bc3cacc5d8ea159fcac03077ca)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument log_bucket_list", value=log_bucket_list, expected_type=type_hints["log_bucket_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
        }
        if log_bucket_list is not None:
            self._values["log_bucket_list"] = log_bucket_list

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Authorizes the Shield Response Team (SRT) using the specified role, to access your AWS account to assist with DDoS attack mitigation during potential attacks.

        This enables the SRT to inspect your AWS WAF configuration and logs and to create or update AWS WAF rules and web ACLs.

        You can associate only one ``RoleArn`` with your subscription. If you submit this update for an account that already has an associated role, the new ``RoleArn`` will replace the existing ``RoleArn`` .

        This change requires the following:

        - You must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .
        - You must have the ``iam:PassRole`` permission. For more information, see `Granting a user permissions to pass a role to an AWS service <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html>`_ .
        - The ``AWSShieldDRTAccessPolicy`` managed policy must be attached to the role that you specify in the request. You can access this policy in the IAM console at `AWSShieldDRTAccessPolicy <https://docs.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSShieldDRTAccessPolicy>`_ . For information, see `Adding and removing IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html>`_ .
        - The role must trust the service principal ``drt.shield.amazonaws.com`` . For information, see `IAM JSON policy elements: Principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html>`_ .

        The SRT will have access only to your AWS WAF and Shield resources. By submitting this request, you provide permissions to the SRT to inspect your AWS WAF and Shield configuration and logs, and to create and update AWS WAF rules and web ACLs on your behalf. The SRT takes these actions only if explicitly authorized by you.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html#cfn-shield-drtaccess-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_bucket_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Authorizes the Shield Response Team (SRT) to access the specified Amazon S3 bucket containing log data such as Application Load Balancer access logs, CloudFront logs, or logs from third party sources.

        You can associate up to 10 Amazon S3 buckets with your subscription.

        Use this to share information with the SRT that's not available in AWS WAF logs.

        To use the services of the SRT, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-drtaccess.html#cfn-shield-drtaccess-logbucketlist
        '''
        result = self._values.get("log_bucket_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDRTAccessProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProactiveEngagement(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_shield.CfnProactiveEngagement",
):
    '''A CloudFormation ``AWS::Shield::ProactiveEngagement``.

    Authorizes the Shield Response Team (SRT) to use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support.

    To enable proactive engagement, you must be subscribed to the `Business Support plan <https://docs.aws.amazon.com/premiumsupport/business-support/>`_ or the `Enterprise Support plan <https://docs.aws.amazon.com/premiumsupport/enterprise-support/>`_ .
    .. epigraph::

       To configure this resource through AWS CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    :cloudformationResource: AWS::Shield::ProactiveEngagement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_shield as shield
        
        cfn_proactive_engagement = shield.CfnProactiveEngagement(self, "MyCfnProactiveEngagement",
            emergency_contact_list=[shield.CfnProactiveEngagement.EmergencyContactProperty(
                email_address="emailAddress",
        
                # the properties below are optional
                contact_notes="contactNotes",
                phone_number="phoneNumber"
            )],
            proactive_engagement_status="proactiveEngagementStatus"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        emergency_contact_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        proactive_engagement_status: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Shield::ProactiveEngagement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param emergency_contact_list: The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes. To enable proactive engagement, the contact list must include at least one phone number. If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact. Example contact notes: - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call. - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.
        :param proactive_engagement_status: Specifies whether proactive engagement is enabled or disabled. Valid values: ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support. ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480237e65b7415ecf6d9bb7eedb9d3cf2ad947c5519fa730fdc6d6ee48d9be51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProactiveEngagementProps(
            emergency_contact_list=emergency_contact_list,
            proactive_engagement_status=proactive_engagement_status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41f47c01f36ad0c5952609367deffc2255e280523a7977a80cf07e564578657)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffcf05c2a901e0f822e167de660754bcf4cda2cb93e1835e3b9e43024ac721ed)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountId")
    def attr_account_id(self) -> builtins.str:
        '''The ID of the account that submitted the template.

        :cloudformationAttribute: AccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccountId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="emergencyContactList")
    def emergency_contact_list(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", _IResolvable_a771d0ef]]]:
        '''The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes.

        To enable proactive engagement, the contact list must include at least one phone number.

        If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact.

        Example contact notes:

        - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call.
        - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-emergencycontactlist
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", _IResolvable_a771d0ef]]], jsii.get(self, "emergencyContactList"))

    @emergency_contact_list.setter
    def emergency_contact_list(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe149817c79df97f2d5dad7fe8eb9a3195632dc53ae16d095b6bbfda7d0ce9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emergencyContactList", value)

    @builtins.property
    @jsii.member(jsii_name="proactiveEngagementStatus")
    def proactive_engagement_status(self) -> builtins.str:
        '''Specifies whether proactive engagement is enabled or disabled.

        Valid values:

        ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support.

        ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-proactiveengagementstatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "proactiveEngagementStatus"))

    @proactive_engagement_status.setter
    def proactive_engagement_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11404311f9b3e286060c2d3501e187b788cfb73aee8c4d310dd9d226c53475c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveEngagementStatus", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_shield.CfnProactiveEngagement.EmergencyContactProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_address": "emailAddress",
            "contact_notes": "contactNotes",
            "phone_number": "phoneNumber",
        },
    )
    class EmergencyContactProperty:
        def __init__(
            self,
            *,
            email_address: builtins.str,
            contact_notes: typing.Optional[builtins.str] = None,
            phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contact information that the SRT can use to contact you if you have proactive engagement enabled, for escalations to the SRT and to initiate proactive customer support.

            :param email_address: The email address for the contact.
            :param contact_notes: Additional notes regarding the contact.
            :param phone_number: The phone number for the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_shield as shield
                
                emergency_contact_property = shield.CfnProactiveEngagement.EmergencyContactProperty(
                    email_address="emailAddress",
                
                    # the properties below are optional
                    contact_notes="contactNotes",
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1917dd5b17510e9277af237e04f1f54173848e457b531eaf2131d95205f1f28)
                check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
                check_type(argname="argument contact_notes", value=contact_notes, expected_type=type_hints["contact_notes"])
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "email_address": email_address,
            }
            if contact_notes is not None:
                self._values["contact_notes"] = contact_notes
            if phone_number is not None:
                self._values["phone_number"] = phone_number

        @builtins.property
        def email_address(self) -> builtins.str:
            '''The email address for the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html#cfn-shield-proactiveengagement-emergencycontact-emailaddress
            '''
            result = self._values.get("email_address")
            assert result is not None, "Required property 'email_address' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def contact_notes(self) -> typing.Optional[builtins.str]:
            '''Additional notes regarding the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html#cfn-shield-proactiveengagement-emergencycontact-contactnotes
            '''
            result = self._values.get("contact_notes")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number for the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-proactiveengagement-emergencycontact.html#cfn-shield-proactiveengagement-emergencycontact-phonenumber
            '''
            result = self._values.get("phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmergencyContactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_shield.CfnProactiveEngagementProps",
    jsii_struct_bases=[],
    name_mapping={
        "emergency_contact_list": "emergencyContactList",
        "proactive_engagement_status": "proactiveEngagementStatus",
    },
)
class CfnProactiveEngagementProps:
    def __init__(
        self,
        *,
        emergency_contact_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        proactive_engagement_status: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnProactiveEngagement``.

        :param emergency_contact_list: The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes. To enable proactive engagement, the contact list must include at least one phone number. If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact. Example contact notes: - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call. - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.
        :param proactive_engagement_status: Specifies whether proactive engagement is enabled or disabled. Valid values: ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support. ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_shield as shield
            
            cfn_proactive_engagement_props = shield.CfnProactiveEngagementProps(
                emergency_contact_list=[shield.CfnProactiveEngagement.EmergencyContactProperty(
                    email_address="emailAddress",
            
                    # the properties below are optional
                    contact_notes="contactNotes",
                    phone_number="phoneNumber"
                )],
                proactive_engagement_status="proactiveEngagementStatus"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d42db9c35ea5811c0817fd9e77604a2dde941141619c9c92fbf126cb64b456c)
            check_type(argname="argument emergency_contact_list", value=emergency_contact_list, expected_type=type_hints["emergency_contact_list"])
            check_type(argname="argument proactive_engagement_status", value=proactive_engagement_status, expected_type=type_hints["proactive_engagement_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "emergency_contact_list": emergency_contact_list,
            "proactive_engagement_status": proactive_engagement_status,
        }

    @builtins.property
    def emergency_contact_list(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, _IResolvable_a771d0ef]]]:
        '''The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes.

        To enable proactive engagement, the contact list must include at least one phone number.

        If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact.

        Example contact notes:

        - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call.
        - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-emergencycontactlist
        '''
        result = self._values.get("emergency_contact_list")
        assert result is not None, "Required property 'emergency_contact_list' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def proactive_engagement_status(self) -> builtins.str:
        '''Specifies whether proactive engagement is enabled or disabled.

        Valid values:

        ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support.

        ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-proactiveengagementstatus
        '''
        result = self._values.get("proactive_engagement_status")
        assert result is not None, "Required property 'proactive_engagement_status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProactiveEngagementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProtection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_shield.CfnProtection",
):
    '''A CloudFormation ``AWS::Shield::Protection``.

    Enables AWS Shield Advanced for a specific AWS resource. The resource can be an Amazon CloudFront distribution, Amazon Route 53 hosted zone, AWS Global Accelerator standard accelerator, Elastic IP Address, Application Load Balancer, or a Classic Load Balancer. You can protect Amazon EC2 instances and Network Load Balancers by association with protected Amazon EC2 Elastic IP addresses.

    Use this to add protection to a single resource at a time. You can add protection to multiple resources at once through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ . For more information see `Getting Started with AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/getting-started-ddos.html>`_ and `Managing resource protections in AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-manage-protected-resources.html>`_ .
    .. epigraph::

       To configure this resource through AWS CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    :cloudformationResource: AWS::Shield::Protection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_shield as shield
        
        # block: Any
        # count: Any
        
        cfn_protection = shield.CfnProtection(self, "MyCfnProtection",
            name="name",
            resource_arn="resourceArn",
        
            # the properties below are optional
            application_layer_automatic_response_configuration=shield.CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty(
                action=shield.CfnProtection.ActionProperty(
                    block=block,
                    count=count
                ),
                status="status"
            ),
            health_check_arns=["healthCheckArns"],
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
        name: builtins.str,
        resource_arn: builtins.str,
        application_layer_automatic_response_configuration: typing.Optional[typing.Union[typing.Union["CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Shield::Protection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the protection. For example, ``My CloudFront distributions`` .
        :param resource_arn: The ARN (Amazon Resource Name) of the AWS resource that is protected.
        :param application_layer_automatic_response_configuration: The automatic application layer DDoS mitigation settings for the protection. This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.
        :param health_check_arns: The ARN (Amazon Resource Name) of the health check to associate with the protection. Health-based detection provides improved responsiveness and accuracy in attack detection and mitigation. You can use this option with any resource type except for Route 53 hosted zones. For more information, see `Configuring health-based detection using health checks <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html>`_ in the *AWS Shield Advanced Developer Guide* .
        :param tags: Key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource. .. epigraph:: To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00651b07456bfa3ef8d41fe0b70b21607444aeebe869f8c13fb76f760044eef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProtectionProps(
            name=name,
            resource_arn=resource_arn,
            application_layer_automatic_response_configuration=application_layer_automatic_response_configuration,
            health_check_arns=health_check_arns,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f887a4c34a29c78f6e750afbdf26e34c76f00691056818e2e120835d898bd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1c3f34ba1874f891f3e163e17551142bdcef577d8dcb110979a0f85daa0a85)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrProtectionArn")
    def attr_protection_arn(self) -> builtins.str:
        '''The ARN (Amazon Resource Name) of the new protection.

        :cloudformationAttribute: ProtectionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProtectionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProtectionId")
    def attr_protection_id(self) -> builtins.str:
        '''The ID of the new protection.

        :cloudformationAttribute: ProtectionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProtectionId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the protection.

        For example, ``My CloudFront distributions`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e235616864f5f4409382dd85ae4f9af9d9e8d2d260b7bd2c967108e7c1f3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''The ARN (Amazon Resource Name) of the AWS resource that is protected.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75d00c6e882d7c359df21a943947577598e367995006d37d3a7e61283b6e49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="applicationLayerAutomaticResponseConfiguration")
    def application_layer_automatic_response_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The automatic application layer DDoS mitigation settings for the protection.

        This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "applicationLayerAutomaticResponseConfiguration"))

    @application_layer_automatic_response_configuration.setter
    def application_layer_automatic_response_configuration(
        self,
        value: typing.Optional[typing.Union["CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b232a97cca39b6120c7f28d779cefe6312aebed545143844a61964410a28080c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationLayerAutomaticResponseConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckArns")
    def health_check_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN (Amazon Resource Name) of the health check to associate with the protection.

        Health-based detection provides improved responsiveness and accuracy in attack detection and mitigation.

        You can use this option with any resource type except for Route 53 hosted zones.

        For more information, see `Configuring health-based detection using health checks <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html>`_ in the *AWS Shield Advanced Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-healthcheckarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "healthCheckArns"))

    @health_check_arns.setter
    def health_check_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade7723e39d237ac5e18721450575ee6fb8feb0a90e251f3cfe61cce23b2e9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckArns", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_shield.CfnProtection.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"block": "block", "count": "count"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            block: typing.Any = None,
            count: typing.Any = None,
        ) -> None:
            '''Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks.

            You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.

            :param block: Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Block`` action. You must specify exactly one action, either ``Block`` or ``Count`` . Example JSON: ``{ "Block": {} }`` Example YAML: ``Block: {}``
            :param count: Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Count`` action. You must specify exactly one action, either ``Block`` or ``Count`` . Example JSON: ``{ "Count": {} }`` Example YAML: ``Count: {}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_shield as shield
                
                # block: Any
                # count: Any
                
                action_property = shield.CfnProtection.ActionProperty(
                    block=block,
                    count=count
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e78ade4c2a13a885260f039388b646fa94cfd007a1e60bf42406c3fcad6c6fa)
                check_type(argname="argument block", value=block, expected_type=type_hints["block"])
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block is not None:
                self._values["block"] = block
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def block(self) -> typing.Any:
            '''Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Block`` action.

            You must specify exactly one action, either ``Block`` or ``Count`` .

            Example JSON: ``{ "Block": {} }``

            Example YAML: ``Block: {}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-action.html#cfn-shield-protection-action-block
            '''
            result = self._values.get("block")
            return typing.cast(typing.Any, result)

        @builtins.property
        def count(self) -> typing.Any:
            '''Specifies that Shield Advanced should configure its AWS WAF rules with the AWS WAF ``Count`` action.

            You must specify exactly one action, either ``Block`` or ``Count`` .

            Example JSON: ``{ "Count": {} }``

            Example YAML: ``Count: {}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-action.html#cfn-shield-protection-action-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_shield.CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "status": "status"},
    )
    class ApplicationLayerAutomaticResponseConfigurationProperty:
        def __init__(
            self,
            *,
            action: typing.Union[typing.Union["CfnProtection.ActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            status: builtins.str,
        ) -> None:
            '''The automatic application layer DDoS mitigation settings for a ``Protection`` .

            This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

            :param action: Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks. You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.
            :param status: Indicates whether automatic application layer DDoS mitigation is enabled for the protection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_shield as shield
                
                # block: Any
                # count: Any
                
                application_layer_automatic_response_configuration_property = shield.CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty(
                    action=shield.CfnProtection.ActionProperty(
                        block=block,
                        count=count
                    ),
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5bafd7d29c4b021db7fd241420371fa154020820fae488c5c3d89ab79a3bdc1c)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "status": status,
            }

        @builtins.property
        def action(
            self,
        ) -> typing.Union["CfnProtection.ActionProperty", _IResolvable_a771d0ef]:
            '''Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks.

            You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union["CfnProtection.ActionProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def status(self) -> builtins.str:
            '''Indicates whether automatic application layer DDoS mitigation is enabled for the protection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLayerAutomaticResponseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnProtectionGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_shield.CfnProtectionGroup",
):
    '''A CloudFormation ``AWS::Shield::ProtectionGroup``.

    Creates a grouping of protected resources so they can be handled as a collective. This resource grouping improves the accuracy of detection and reduces false positives.
    .. epigraph::

       To configure this resource through AWS CloudFormation , you must be subscribed to AWS Shield Advanced . You can subscribe through the `Shield Advanced console <https://docs.aws.amazon.com/wafv2/shieldv2#/>`_ and through the APIs. For more information, see `Subscribe to AWS Shield Advanced <https://docs.aws.amazon.com/waf/latest/developerguide/enable-ddos-prem.html>`_ .

    :cloudformationResource: AWS::Shield::ProtectionGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_shield as shield
        
        cfn_protection_group = shield.CfnProtectionGroup(self, "MyCfnProtectionGroup",
            aggregation="aggregation",
            pattern="pattern",
            protection_group_id="protectionGroupId",
        
            # the properties below are optional
            members=["members"],
            resource_type="resourceType",
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
        aggregation: builtins.str,
        pattern: builtins.str,
        protection_group_id: builtins.str,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Shield::ProtectionGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param aggregation: Defines how AWS Shield combines resource data for the group in order to detect, mitigate, and report events. - Sum - Use the total traffic across the group. This is a good choice for most cases. Examples include Elastic IP addresses for EC2 instances that scale manually or automatically. - Mean - Use the average of the traffic across the group. This is a good choice for resources that share traffic uniformly. Examples include accelerators and load balancers. - Max - Use the highest traffic from each resource. This is useful for resources that don't share traffic and for resources that share that traffic in a non-uniform way. Examples include Amazon CloudFront distributions and origin resources for CloudFront distributions.
        :param pattern: The criteria to use to choose the protected resources for inclusion in the group. You can include all resources that have protections, provide a list of resource ARNs (Amazon Resource Names), or include all resources of a specified resource type.
        :param protection_group_id: The name of the protection group. You use this to identify the protection group in lists and to manage the protection group, for example to update, delete, or describe it.
        :param members: The ARNs (Amazon Resource Names) of the resources to include in the protection group. You must set this when you set ``Pattern`` to ``ARBITRARY`` and you must not set it for any other ``Pattern`` setting.
        :param resource_type: The resource type to include in the protection group. All protected resources of this type are included in the protection group. You must set this when you set ``Pattern`` to ``BY_RESOURCE_TYPE`` and you must not set it for any other ``Pattern`` setting.
        :param tags: Key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource. .. epigraph:: To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489dc05b172a21af0d39ee1ca2df90000fe0f6c4f9b6fd3c70fcf119e2b36b58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProtectionGroupProps(
            aggregation=aggregation,
            pattern=pattern,
            protection_group_id=protection_group_id,
            members=members,
            resource_type=resource_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d853e3b85667588a3c8f72c2fdf683b45d9d49088545a3694ab46b95dc34da0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd816df4d363552486eb19c8bf23e985dac7a4e2b1b85b2187cbc308be75c2a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrProtectionGroupArn")
    def attr_protection_group_arn(self) -> builtins.str:
        '''The ARN (Amazon Resource Name) of the new protection group.

        :cloudformationAttribute: ProtectionGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProtectionGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="aggregation")
    def aggregation(self) -> builtins.str:
        '''Defines how AWS Shield combines resource data for the group in order to detect, mitigate, and report events.

        - Sum - Use the total traffic across the group. This is a good choice for most cases. Examples include Elastic IP addresses for EC2 instances that scale manually or automatically.
        - Mean - Use the average of the traffic across the group. This is a good choice for resources that share traffic uniformly. Examples include accelerators and load balancers.
        - Max - Use the highest traffic from each resource. This is useful for resources that don't share traffic and for resources that share that traffic in a non-uniform way. Examples include Amazon CloudFront distributions and origin resources for CloudFront distributions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-aggregation
        '''
        return typing.cast(builtins.str, jsii.get(self, "aggregation"))

    @aggregation.setter
    def aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8153d62c88f7956c210b3d63ecb4d812845c1cd65a0672a82277aa3414eb6059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregation", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        '''The criteria to use to choose the protected resources for inclusion in the group.

        You can include all resources that have protections, provide a list of resource ARNs (Amazon Resource Names), or include all resources of a specified resource type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-pattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8456c71f8acd72bae7ec0286e65183671332b44afa9b09f2b031c6967adb8db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="protectionGroupId")
    def protection_group_id(self) -> builtins.str:
        '''The name of the protection group.

        You use this to identify the protection group in lists and to manage the protection group, for example to update, delete, or describe it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-protectiongroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "protectionGroupId"))

    @protection_group_id.setter
    def protection_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66489d54f7a50b05e018513e4a6a1b61ec987ee40c76ededd6f671a2a3a6ff5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectionGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs (Amazon Resource Names) of the resources to include in the protection group.

        You must set this when you set ``Pattern`` to ``ARBITRARY`` and you must not set it for any other ``Pattern`` setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-members
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "members"))

    @members.setter
    def members(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38abc4a4526848e0508652dd152033a9bed76f866c6f3eddabfe1504f01a872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "members", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type to include in the protection group.

        All protected resources of this type are included in the protection group. You must set this when you set ``Pattern`` to ``BY_RESOURCE_TYPE`` and you must not set it for any other ``Pattern`` setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-resourcetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f696dfe16b3da617fca28481e22f0be4bbfceb066a3ba0659ecb873734641b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)


@jsii.data_type(
    jsii_type="monocdk.aws_shield.CfnProtectionGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation": "aggregation",
        "pattern": "pattern",
        "protection_group_id": "protectionGroupId",
        "members": "members",
        "resource_type": "resourceType",
        "tags": "tags",
    },
)
class CfnProtectionGroupProps:
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        pattern: builtins.str,
        protection_group_id: builtins.str,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProtectionGroup``.

        :param aggregation: Defines how AWS Shield combines resource data for the group in order to detect, mitigate, and report events. - Sum - Use the total traffic across the group. This is a good choice for most cases. Examples include Elastic IP addresses for EC2 instances that scale manually or automatically. - Mean - Use the average of the traffic across the group. This is a good choice for resources that share traffic uniformly. Examples include accelerators and load balancers. - Max - Use the highest traffic from each resource. This is useful for resources that don't share traffic and for resources that share that traffic in a non-uniform way. Examples include Amazon CloudFront distributions and origin resources for CloudFront distributions.
        :param pattern: The criteria to use to choose the protected resources for inclusion in the group. You can include all resources that have protections, provide a list of resource ARNs (Amazon Resource Names), or include all resources of a specified resource type.
        :param protection_group_id: The name of the protection group. You use this to identify the protection group in lists and to manage the protection group, for example to update, delete, or describe it.
        :param members: The ARNs (Amazon Resource Names) of the resources to include in the protection group. You must set this when you set ``Pattern`` to ``ARBITRARY`` and you must not set it for any other ``Pattern`` setting.
        :param resource_type: The resource type to include in the protection group. All protected resources of this type are included in the protection group. You must set this when you set ``Pattern`` to ``BY_RESOURCE_TYPE`` and you must not set it for any other ``Pattern`` setting.
        :param tags: Key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource. .. epigraph:: To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_shield as shield
            
            cfn_protection_group_props = shield.CfnProtectionGroupProps(
                aggregation="aggregation",
                pattern="pattern",
                protection_group_id="protectionGroupId",
            
                # the properties below are optional
                members=["members"],
                resource_type="resourceType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af13204c848ade1e3504ab53bbbaa8be33142b099b2577d39f286e8a7e47591c)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument protection_group_id", value=protection_group_id, expected_type=type_hints["protection_group_id"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
            "pattern": pattern,
            "protection_group_id": protection_group_id,
        }
        if members is not None:
            self._values["members"] = members
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''Defines how AWS Shield combines resource data for the group in order to detect, mitigate, and report events.

        - Sum - Use the total traffic across the group. This is a good choice for most cases. Examples include Elastic IP addresses for EC2 instances that scale manually or automatically.
        - Mean - Use the average of the traffic across the group. This is a good choice for resources that share traffic uniformly. Examples include accelerators and load balancers.
        - Max - Use the highest traffic from each resource. This is useful for resources that don't share traffic and for resources that share that traffic in a non-uniform way. Examples include Amazon CloudFront distributions and origin resources for CloudFront distributions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-aggregation
        '''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The criteria to use to choose the protected resources for inclusion in the group.

        You can include all resources that have protections, provide a list of resource ARNs (Amazon Resource Names), or include all resources of a specified resource type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-pattern
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protection_group_id(self) -> builtins.str:
        '''The name of the protection group.

        You use this to identify the protection group in lists and to manage the protection group, for example to update, delete, or describe it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-protectiongroupid
        '''
        result = self._values.get("protection_group_id")
        assert result is not None, "Required property 'protection_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs (Amazon Resource Names) of the resources to include in the protection group.

        You must set this when you set ``Pattern`` to ``ARBITRARY`` and you must not set it for any other ``Pattern`` setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-members
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type to include in the protection group.

        All protected resources of this type are included in the protection group. You must set this when you set ``Pattern`` to ``BY_RESOURCE_TYPE`` and you must not set it for any other ``Pattern`` setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProtectionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_shield.CfnProtectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "resource_arn": "resourceArn",
        "application_layer_automatic_response_configuration": "applicationLayerAutomaticResponseConfiguration",
        "health_check_arns": "healthCheckArns",
        "tags": "tags",
    },
)
class CfnProtectionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_arn: builtins.str,
        application_layer_automatic_response_configuration: typing.Optional[typing.Union[typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProtection``.

        :param name: The name of the protection. For example, ``My CloudFront distributions`` .
        :param resource_arn: The ARN (Amazon Resource Name) of the AWS resource that is protected.
        :param application_layer_automatic_response_configuration: The automatic application layer DDoS mitigation settings for the protection. This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.
        :param health_check_arns: The ARN (Amazon Resource Name) of the health check to associate with the protection. Health-based detection provides improved responsiveness and accuracy in attack detection and mitigation. You can use this option with any resource type except for Route 53 hosted zones. For more information, see `Configuring health-based detection using health checks <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html>`_ in the *AWS Shield Advanced Developer Guide* .
        :param tags: Key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource. .. epigraph:: To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_shield as shield
            
            # block: Any
            # count: Any
            
            cfn_protection_props = shield.CfnProtectionProps(
                name="name",
                resource_arn="resourceArn",
            
                # the properties below are optional
                application_layer_automatic_response_configuration=shield.CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty(
                    action=shield.CfnProtection.ActionProperty(
                        block=block,
                        count=count
                    ),
                    status="status"
                ),
                health_check_arns=["healthCheckArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19ab939b4f69bed557a445c38d3066071f6d58d55e5a70844c5c9182ce7ef93)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument application_layer_automatic_response_configuration", value=application_layer_automatic_response_configuration, expected_type=type_hints["application_layer_automatic_response_configuration"])
            check_type(argname="argument health_check_arns", value=health_check_arns, expected_type=type_hints["health_check_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_arn": resource_arn,
        }
        if application_layer_automatic_response_configuration is not None:
            self._values["application_layer_automatic_response_configuration"] = application_layer_automatic_response_configuration
        if health_check_arns is not None:
            self._values["health_check_arns"] = health_check_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the protection.

        For example, ``My CloudFront distributions`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''The ARN (Amazon Resource Name) of the AWS resource that is protected.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_layer_automatic_response_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The automatic application layer DDoS mitigation settings for the protection.

        This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration
        '''
        result = self._values.get("application_layer_automatic_response_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def health_check_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN (Amazon Resource Name) of the health check to associate with the protection.

        Health-based detection provides improved responsiveness and accuracy in attack detection and mitigation.

        You can use this option with any resource type except for Route 53 hosted zones.

        For more information, see `Configuring health-based detection using health checks <https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html>`_ in the *AWS Shield Advanced Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-healthcheckarns
        '''
        result = self._values.get("health_check_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProtectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDRTAccess",
    "CfnDRTAccessProps",
    "CfnProactiveEngagement",
    "CfnProactiveEngagementProps",
    "CfnProtection",
    "CfnProtectionGroup",
    "CfnProtectionGroupProps",
    "CfnProtectionProps",
]

publication.publish()

def _typecheckingstub__0790387ac1e3d4d086236e24ad3be3a29fe52ed6e3430c2b02d1526dd73907a6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    role_arn: builtins.str,
    log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3800aa24ccc3141595c0c8c90c36d936012bb9566dbd04e357288f612febb4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0848f2af47f6d9ccdce99ca63f71696e29643936ad2655f3255620d657b6bacd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a99a0799de23719ec1572626e3b17c0fce82b748f752f6d8c81cdae7c9341cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d1510ad9417ca37ec327868eb91ec02bd3c6777773dc2124e82c6d3a0250d3(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d339abc8a5991c44e2d98a0cd39384001e6102bc3cacc5d8ea159fcac03077ca(
    *,
    role_arn: builtins.str,
    log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480237e65b7415ecf6d9bb7eedb9d3cf2ad947c5519fa730fdc6d6ee48d9be51(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    emergency_contact_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    proactive_engagement_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41f47c01f36ad0c5952609367deffc2255e280523a7977a80cf07e564578657(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcf05c2a901e0f822e167de660754bcf4cda2cb93e1835e3b9e43024ac721ed(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe149817c79df97f2d5dad7fe8eb9a3195632dc53ae16d095b6bbfda7d0ce9e(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11404311f9b3e286060c2d3501e187b788cfb73aee8c4d310dd9d226c53475c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1917dd5b17510e9277af237e04f1f54173848e457b531eaf2131d95205f1f28(
    *,
    email_address: builtins.str,
    contact_notes: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d42db9c35ea5811c0817fd9e77604a2dde941141619c9c92fbf126cb64b456c(
    *,
    emergency_contact_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    proactive_engagement_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00651b07456bfa3ef8d41fe0b70b21607444aeebe869f8c13fb76f760044eef(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    resource_arn: builtins.str,
    application_layer_automatic_response_configuration: typing.Optional[typing.Union[typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f887a4c34a29c78f6e750afbdf26e34c76f00691056818e2e120835d898bd5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1c3f34ba1874f891f3e163e17551142bdcef577d8dcb110979a0f85daa0a85(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e235616864f5f4409382dd85ae4f9af9d9e8d2d260b7bd2c967108e7c1f3f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75d00c6e882d7c359df21a943947577598e367995006d37d3a7e61283b6e49b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b232a97cca39b6120c7f28d779cefe6312aebed545143844a61964410a28080c(
    value: typing.Optional[typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade7723e39d237ac5e18721450575ee6fb8feb0a90e251f3cfe61cce23b2e9f7(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e78ade4c2a13a885260f039388b646fa94cfd007a1e60bf42406c3fcad6c6fa(
    *,
    block: typing.Any = None,
    count: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bafd7d29c4b021db7fd241420371fa154020820fae488c5c3d89ab79a3bdc1c(
    *,
    action: typing.Union[typing.Union[CfnProtection.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489dc05b172a21af0d39ee1ca2df90000fe0f6c4f9b6fd3c70fcf119e2b36b58(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    aggregation: builtins.str,
    pattern: builtins.str,
    protection_group_id: builtins.str,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d853e3b85667588a3c8f72c2fdf683b45d9d49088545a3694ab46b95dc34da0f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd816df4d363552486eb19c8bf23e985dac7a4e2b1b85b2187cbc308be75c2a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8153d62c88f7956c210b3d63ecb4d812845c1cd65a0672a82277aa3414eb6059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8456c71f8acd72bae7ec0286e65183671332b44afa9b09f2b031c6967adb8db5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66489d54f7a50b05e018513e4a6a1b61ec987ee40c76ededd6f671a2a3a6ff5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38abc4a4526848e0508652dd152033a9bed76f866c6f3eddabfe1504f01a872(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f696dfe16b3da617fca28481e22f0be4bbfceb066a3ba0659ecb873734641b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af13204c848ade1e3504ab53bbbaa8be33142b099b2577d39f286e8a7e47591c(
    *,
    aggregation: builtins.str,
    pattern: builtins.str,
    protection_group_id: builtins.str,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19ab939b4f69bed557a445c38d3066071f6d58d55e5a70844c5c9182ce7ef93(
    *,
    name: builtins.str,
    resource_arn: builtins.str,
    application_layer_automatic_response_configuration: typing.Optional[typing.Union[typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
