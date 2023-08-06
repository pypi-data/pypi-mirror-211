'''
# AWS::Shield Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_shield as shield
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDRTAccess(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-shield.CfnDRTAccess",
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
        import aws_cdk.aws_shield as shield
        
        cfn_dRTAccess = shield.CfnDRTAccess(self, "MyCfnDRTAccess",
            role_arn="roleArn",
        
            # the properties below are optional
            log_bucket_list=["logBucketList"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eed0c86e2e4aeede571691b88c0c62f09992da10a5e489b117a43982842e5f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDRTAccessProps(role_arn=role_arn, log_bucket_list=log_bucket_list)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839a523386caaf4e93d472b777285746e254c99b01cb16f27b0cbabf91024c99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__619318a93bd8ead44f06d6e4c3806687da2f01fcf2e535631239a215a3d35c98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b30c3958c61c747fc0e1933573cb644f7867ca7cc595746c984c0111cccfa8b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84a5a3484b0d2361dc0b24d21e0428694614c87727b5b2a2503847a7124075b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBucketList", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-shield.CfnDRTAccessProps",
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
            import aws_cdk.aws_shield as shield
            
            cfn_dRTAccess_props = shield.CfnDRTAccessProps(
                role_arn="roleArn",
            
                # the properties below are optional
                log_bucket_list=["logBucketList"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f2561d197727f3b09ed0dcf726257ea6b43adcd9b8d7cd09fb4be70429dc13)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnProactiveEngagement(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-shield.CfnProactiveEngagement",
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
        import aws_cdk.aws_shield as shield
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        emergency_contact_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        proactive_engagement_status: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Shield::ProactiveEngagement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param emergency_contact_list: The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes. To enable proactive engagement, the contact list must include at least one phone number. If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact. Example contact notes: - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call. - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.
        :param proactive_engagement_status: Specifies whether proactive engagement is enabled or disabled. Valid values: ``ENABLED`` - The Shield Response Team (SRT) will use email and phone to notify contacts about escalations to the SRT and to initiate proactive customer support. ``DISABLED`` - The SRT will not proactively notify contacts about escalations or to initiate proactive customer support.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11655acd31240c3d4fefd87531d75c4688b6b554017e3f52d776c9f0883d3c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProactiveEngagementProps(
            emergency_contact_list=emergency_contact_list,
            proactive_engagement_status=proactive_engagement_status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2242c3c71a07330486b2956d3ff2eda4cbe9975e2a3c0b79a87d5b39eb7a4b00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c9620df267121a8aeef3262436edfea984809096101998360544b8991cc50b)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The list of email addresses and phone numbers that the Shield Response Team (SRT) can use to contact you for escalations to the SRT and to initiate proactive customer support, plus any relevant notes.

        To enable proactive engagement, the contact list must include at least one phone number.

        If you provide more than one contact, in the notes, indicate the circumstances under which each contact should be used. Include primary and secondary contact designations, and provide the hours of availability and time zones for each contact.

        Example contact notes:

        - This is a hotline that's staffed 24x7x365. Please work with the responding analyst and they will get the appropriate person on the call.
        - Please contact the secondary phone number if the hotline doesn't respond within 5 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-proactiveengagement.html#cfn-shield-proactiveengagement-emergencycontactlist
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", _aws_cdk_core_f4b25747.IResolvable]]], jsii.get(self, "emergencyContactList"))

    @emergency_contact_list.setter
    def emergency_contact_list(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnProactiveEngagement.EmergencyContactProperty", _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0969a162a980764b18afb3a43e2fa485811d9986a71214d38a2718d23862dcc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e6c8bf05fed3b16cbb9d3b415b976681c55a759da764e4ac7a90077704fae54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveEngagementStatus", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-shield.CfnProactiveEngagement.EmergencyContactProperty",
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
                import aws_cdk.aws_shield as shield
                
                emergency_contact_property = shield.CfnProactiveEngagement.EmergencyContactProperty(
                    email_address="emailAddress",
                
                    # the properties below are optional
                    contact_notes="contactNotes",
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72ee39d1cba3e3d13c0b77d8e484cab71de78c5e7b5d284ce044b18f06ab76f6)
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
    jsii_type="@aws-cdk/aws-shield.CfnProactiveEngagementProps",
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
        emergency_contact_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
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
            import aws_cdk.aws_shield as shield
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__114a8ac1f4baaf53e877bd631387c9cc4bf1991f8bb20873fb9ae6aa70e5ffa1)
            check_type(argname="argument emergency_contact_list", value=emergency_contact_list, expected_type=type_hints["emergency_contact_list"])
            check_type(argname="argument proactive_engagement_status", value=proactive_engagement_status, expected_type=type_hints["proactive_engagement_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "emergency_contact_list": emergency_contact_list,
            "proactive_engagement_status": proactive_engagement_status,
        }

    @builtins.property
    def emergency_contact_list(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, _aws_cdk_core_f4b25747.IResolvable]]]:
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
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, _aws_cdk_core_f4b25747.IResolvable]]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnProtection(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-shield.CfnProtection",
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
        import aws_cdk.aws_shield as shield
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        resource_arn: builtins.str,
        application_layer_automatic_response_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaf27cfe14963ffc1caf9c5bd0fe9ee376b3c2537196b3cd753468db09f93ebe)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811a60e1ffd9b27468978e663d31354b0199acc4908f5840c830716cf05f04fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68b4d976d3ddabb24a527d91cd3714efc4aa3b976c89d7d6f83d0687da85914a)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__733226b618aed40ba31612cb299e7f22734aebcdab605dd515cfb73d48814478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26aa9e01ac86fdf84fd2682eef289bbd788d9de4cdef23486464de52d9b11443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="applicationLayerAutomaticResponseConfiguration")
    def application_layer_automatic_response_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty"]]:
        '''The automatic application layer DDoS mitigation settings for the protection.

        This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty"]], jsii.get(self, "applicationLayerAutomaticResponseConfiguration"))

    @application_layer_automatic_response_configuration.setter
    def application_layer_automatic_response_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864d7f01d46ba5ffb09ae08f8fe59e66ce10a9162cb5e2f2e97ce4dc61369dce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f6f43f8d2e85b0967de9703877afc011c9da2ab0072e388cb7bef0a8c2210e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckArns", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-shield.CfnProtection.ActionProperty",
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
                import aws_cdk.aws_shield as shield
                
                # block: Any
                # count: Any
                
                action_property = shield.CfnProtection.ActionProperty(
                    block=block,
                    count=count
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8781c01ece1da8a440395af2fd8e885dca2770376c6b5fde81c985c4a119c555)
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
        jsii_type="@aws-cdk/aws-shield.CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "status": "status"},
    )
    class ApplicationLayerAutomaticResponseConfigurationProperty:
        def __init__(
            self,
            *,
            action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnProtection.ActionProperty", typing.Dict[builtins.str, typing.Any]]],
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
                import aws_cdk.aws_shield as shield
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__5e1db6bb869eba0178332ea23fc2bb92c91eb5636c5890dd42406673f24e6f1a)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "status": status,
            }

        @builtins.property
        def action(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProtection.ActionProperty"]:
            '''Specifies the action setting that Shield Advanced should use in the AWS WAF rules that it creates on behalf of the protected resource in response to DDoS attacks.

            You specify this as part of the configuration for the automatic application layer DDoS mitigation feature, when you enable or update automatic mitigation. Shield Advanced creates the AWS WAF rules in a Shield Advanced-managed rule group, inside the web ACL that you have associated with the resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-shield-protection-applicationlayerautomaticresponseconfiguration.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProtection.ActionProperty"], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnProtectionGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-shield.CfnProtectionGroup",
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
        import aws_cdk.aws_shield as shield
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        aggregation: builtins.str,
        pattern: builtins.str,
        protection_group_id: builtins.str,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c3b616dbf2a256624be915398ee89bb71a8bf7159a92165f76ad8b84538673)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247c9e532762b855da49d5ff7233c1f8feea48fe289dc5cdf8e6b0d6f907f5a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3bbdab4f8f5399a0bdf239277670d6f2bfa696852143642fa1c36c3f2e40501)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__686cec704ec6ff55909a4d46ee3958a8dfe70023fabbc353e37d58e9be32329e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc34a839481a5655b032bdee0f18f2f576c36389af062e0060f3c8ce67bfdbf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad14a60bfcd65b38a5bc5ef3ccd43f6fcca3db070dd1d03e8039d87dc8838e7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c08002a5f3bc60c3f6a0dae37f0618c83af98bcafedf5e21ce0d08a26200e408)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34b3cb5199067ee7d81f3e33911aced95b29790c4d85390fa715b9c2efe5f8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-shield.CfnProtectionGroupProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_shield as shield
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__f111880f6bedb11da51d1d775958c42aee1c9e6b611f9e78581d712c00488eb7)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protectiongroup.html#cfn-shield-protectiongroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProtectionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-shield.CfnProtectionProps",
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
        application_layer_automatic_response_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_shield as shield
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa6bece3966ecd4009455a247537fc7038e7ca482e7813e235f92de047c22166)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty]]:
        '''The automatic application layer DDoS mitigation settings for the protection.

        This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-applicationlayerautomaticresponseconfiguration
        '''
        result = self._values.get("application_layer_automatic_response_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty]], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        .. epigraph::

           To modify tags on existing resources, use the AWS Shield Advanced APIs or command line interface. With AWS CloudFormation , you can only add tags to resources during resource creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-shield-protection.html#cfn-shield-protection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

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

def _typecheckingstub__7eed0c86e2e4aeede571691b88c0c62f09992da10a5e489b117a43982842e5f6(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    role_arn: builtins.str,
    log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839a523386caaf4e93d472b777285746e254c99b01cb16f27b0cbabf91024c99(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619318a93bd8ead44f06d6e4c3806687da2f01fcf2e535631239a215a3d35c98(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30c3958c61c747fc0e1933573cb644f7867ca7cc595746c984c0111cccfa8b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84a5a3484b0d2361dc0b24d21e0428694614c87727b5b2a2503847a7124075b(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f2561d197727f3b09ed0dcf726257ea6b43adcd9b8d7cd09fb4be70429dc13(
    *,
    role_arn: builtins.str,
    log_bucket_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11655acd31240c3d4fefd87531d75c4688b6b554017e3f52d776c9f0883d3c7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    emergency_contact_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    proactive_engagement_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2242c3c71a07330486b2956d3ff2eda4cbe9975e2a3c0b79a87d5b39eb7a4b00(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c9620df267121a8aeef3262436edfea984809096101998360544b8991cc50b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0969a162a980764b18afb3a43e2fa485811d9986a71214d38a2718d23862dcc8(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6c8bf05fed3b16cbb9d3b415b976681c55a759da764e4ac7a90077704fae54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ee39d1cba3e3d13c0b77d8e484cab71de78c5e7b5d284ce044b18f06ab76f6(
    *,
    email_address: builtins.str,
    contact_notes: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114a8ac1f4baaf53e877bd631387c9cc4bf1991f8bb20873fb9ae6aa70e5ffa1(
    *,
    emergency_contact_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnProactiveEngagement.EmergencyContactProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    proactive_engagement_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf27cfe14963ffc1caf9c5bd0fe9ee376b3c2537196b3cd753468db09f93ebe(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    resource_arn: builtins.str,
    application_layer_automatic_response_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811a60e1ffd9b27468978e663d31354b0199acc4908f5840c830716cf05f04fb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b4d976d3ddabb24a527d91cd3714efc4aa3b976c89d7d6f83d0687da85914a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733226b618aed40ba31612cb299e7f22734aebcdab605dd515cfb73d48814478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26aa9e01ac86fdf84fd2682eef289bbd788d9de4cdef23486464de52d9b11443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864d7f01d46ba5ffb09ae08f8fe59e66ce10a9162cb5e2f2e97ce4dc61369dce(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f6f43f8d2e85b0967de9703877afc011c9da2ab0072e388cb7bef0a8c2210e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8781c01ece1da8a440395af2fd8e885dca2770376c6b5fde81c985c4a119c555(
    *,
    block: typing.Any = None,
    count: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1db6bb869eba0178332ea23fc2bb92c91eb5636c5890dd42406673f24e6f1a(
    *,
    action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProtection.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c3b616dbf2a256624be915398ee89bb71a8bf7159a92165f76ad8b84538673(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    aggregation: builtins.str,
    pattern: builtins.str,
    protection_group_id: builtins.str,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247c9e532762b855da49d5ff7233c1f8feea48fe289dc5cdf8e6b0d6f907f5a0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bbdab4f8f5399a0bdf239277670d6f2bfa696852143642fa1c36c3f2e40501(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686cec704ec6ff55909a4d46ee3958a8dfe70023fabbc353e37d58e9be32329e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc34a839481a5655b032bdee0f18f2f576c36389af062e0060f3c8ce67bfdbf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad14a60bfcd65b38a5bc5ef3ccd43f6fcca3db070dd1d03e8039d87dc8838e7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08002a5f3bc60c3f6a0dae37f0618c83af98bcafedf5e21ce0d08a26200e408(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b3cb5199067ee7d81f3e33911aced95b29790c4d85390fa715b9c2efe5f8d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f111880f6bedb11da51d1d775958c42aee1c9e6b611f9e78581d712c00488eb7(
    *,
    aggregation: builtins.str,
    pattern: builtins.str,
    protection_group_id: builtins.str,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6bece3966ecd4009455a247537fc7038e7ca482e7813e235f92de047c22166(
    *,
    name: builtins.str,
    resource_arn: builtins.str,
    application_layer_automatic_response_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProtection.ApplicationLayerAutomaticResponseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
