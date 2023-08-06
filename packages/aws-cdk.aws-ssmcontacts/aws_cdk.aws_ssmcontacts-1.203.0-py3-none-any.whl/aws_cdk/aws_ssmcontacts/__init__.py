'''
# AWS::SSMContacts Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_ssmcontacts as ssmcontacts
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SSMContacts construct libraries](https://constructs.dev/search?q=ssmcontacts)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SSMContacts resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMContacts.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SSMContacts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMContacts.html).

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
class CfnContact(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact",
):
    '''A CloudFormation ``AWS::SSMContacts::Contact``.

    The ``AWS::SSMContacts::Contact`` resource specifies a contact or escalation plan. Incident Manager contacts are a subset of actions and data types that you can use for managing responder engagement and interaction.

    :cloudformationResource: AWS::SSMContacts::Contact
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ssmcontacts as ssmcontacts
        
        cfn_contact = ssmcontacts.CfnContact(self, "MyCfnContact",
            alias="alias",
            display_name="displayName",
            type="type",
        
            # the properties below are optional
            plan=[ssmcontacts.CfnContact.StageProperty(
                duration_in_minutes=123,
                rotation_ids=["rotationIds"],
                targets=[ssmcontacts.CfnContact.TargetsProperty(
                    channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )]
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        alias: builtins.str,
        display_name: builtins.str,
        type: builtins.str,
        plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnContact.StageProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SSMContacts::Contact``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alias: The unique and identifiable alias of the contact or escalation plan.
        :param display_name: The full name of the contact or escalation plan.
        :param type: Refers to the type of contact:. - ``PERSONAL`` : A single, individual contact. - ``ESCALATION`` : An escalation plan. - ``ONCALL_SCHEDULE`` : An on-call schedule.
        :param plan: A list of stages. A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6ca3ad36cfd3d6487f8dd1a8ac11bbf921386d1f05da32bbf84640646093d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactProps(
            alias=alias, display_name=display_name, type=type, plan=plan
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1230b668b68ef75e2be0ce9ce5bf14b7bd3b3b8b362785f62b8727c5094d5496)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc3a35478651edceaa8211ec1ec74ee20552b26c38b90ed6598a8f22b7a3324e)
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
        '''The Amazon Resource Name (ARN) of the ``Contact`` resource, such as ``arn:aws:ssm-contacts:us-west-2:123456789012:contact/contactalias`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        '''The unique and identifiable alias of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-alias
        '''
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e5a583902645e320f5f0d421b8847dd608990992c74ef2c375c9883591a4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''The full name of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-displayname
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634d931c33dc249f0a936122628bdb785fe509e48fda71d174f94247ec282c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Refers to the type of contact:.

        - ``PERSONAL`` : A single, individual contact.
        - ``ESCALATION`` : An escalation plan.
        - ``ONCALL_SCHEDULE`` : An on-call schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e692648e4215a1fe47c884b97b303f2d8f54f2325bc4e89fe8459ba378deceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnContact.StageProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of stages.

        A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-plan
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnContact.StageProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "plan"))

    @plan.setter
    def plan(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnContact.StageProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a5edb5d31e9dd3b301d72fb5451ca492b93ef830ef679d169226bba5835196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plan", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.ChannelTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_id": "channelId",
            "retry_interval_in_minutes": "retryIntervalInMinutes",
        },
    )
    class ChannelTargetInfoProperty:
        def __init__(
            self,
            *,
            channel_id: builtins.str,
            retry_interval_in_minutes: jsii.Number,
        ) -> None:
            '''Information about the contact channel that Incident Manager uses to engage the contact.

            :param channel_id: The Amazon Resource Name (ARN) of the contact channel.
            :param retry_interval_in_minutes: The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                channel_target_info_property = ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                    channel_id="channelId",
                    retry_interval_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1337d37b740eb0596a247fac45b9a6781be3af024b4c695bd779bac6c2fe61c)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument retry_interval_in_minutes", value=retry_interval_in_minutes, expected_type=type_hints["retry_interval_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "channel_id": channel_id,
                "retry_interval_in_minutes": retry_interval_in_minutes,
            }

        @builtins.property
        def channel_id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the contact channel.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html#cfn-ssmcontacts-contact-channeltargetinfo-channelid
            '''
            result = self._values.get("channel_id")
            assert result is not None, "Required property 'channel_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def retry_interval_in_minutes(self) -> jsii.Number:
            '''The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html#cfn-ssmcontacts-contact-channeltargetinfo-retryintervalinminutes
            '''
            result = self._values.get("retry_interval_in_minutes")
            assert result is not None, "Required property 'retry_interval_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.ContactTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_id": "contactId", "is_essential": "isEssential"},
    )
    class ContactTargetInfoProperty:
        def __init__(
            self,
            *,
            contact_id: builtins.str,
            is_essential: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''The contact that Incident Manager is engaging during an incident.

            :param contact_id: The Amazon Resource Name (ARN) of the contact.
            :param is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                contact_target_info_property = ssmcontacts.CfnContact.ContactTargetInfoProperty(
                    contact_id="contactId",
                    is_essential=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27bb2669b4d0ea3739dd8e91f180cb5a526768e1b96634822e01f2d4c19391fc)
                check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
                check_type(argname="argument is_essential", value=is_essential, expected_type=type_hints["is_essential"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_id": contact_id,
                "is_essential": is_essential,
            }

        @builtins.property
        def contact_id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html#cfn-ssmcontacts-contact-contacttargetinfo-contactid
            '''
            result = self._values.get("contact_id")
            assert result is not None, "Required property 'contact_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_essential(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html#cfn-ssmcontacts-contact-contacttargetinfo-isessential
            '''
            result = self._values.get("is_essential")
            assert result is not None, "Required property 'is_essential' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContactTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.StageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_in_minutes": "durationInMinutes",
            "rotation_ids": "rotationIds",
            "targets": "targets",
        },
    )
    class StageProperty:
        def __init__(
            self,
            *,
            duration_in_minutes: typing.Optional[jsii.Number] = None,
            rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContact.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``Stage`` property type specifies a set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.

            :param duration_in_minutes: The time to wait until beginning the next stage. The duration can only be set to 0 if a target is specified.
            :param rotation_ids: The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.
            :param targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                stage_property = ssmcontacts.CfnContact.StageProperty(
                    duration_in_minutes=123,
                    rotation_ids=["rotationIds"],
                    targets=[ssmcontacts.CfnContact.TargetsProperty(
                        channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcdcb9e705292433792b822f72adb7e277c0c72e3b60b4012c590d2ec0dc30bb)
                check_type(argname="argument duration_in_minutes", value=duration_in_minutes, expected_type=type_hints["duration_in_minutes"])
                check_type(argname="argument rotation_ids", value=rotation_ids, expected_type=type_hints["rotation_ids"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_minutes is not None:
                self._values["duration_in_minutes"] = duration_in_minutes
            if rotation_ids is not None:
                self._values["rotation_ids"] = rotation_ids
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def duration_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The time to wait until beginning the next stage.

            The duration can only be set to 0 if a target is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-durationinminutes
            '''
            result = self._values.get("duration_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rotation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-rotationids
            '''
            result = self._values.get("rotation_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.TargetsProperty"]]]]:
            '''The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.TargetsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnContact.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_target_info": "channelTargetInfo",
            "contact_target_info": "contactTargetInfo",
        },
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            channel_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContact.ChannelTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            contact_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContact.ContactTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The contact or contact channel that's being engaged.

            :param channel_target_info: Information about the contact channel that Incident Manager engages.
            :param contact_target_info: The contact that Incident Manager is engaging during an incident.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                targets_property = ssmcontacts.CfnContact.TargetsProperty(
                    channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11e07482c664cb3a3264fa1f4d90282c886057cd7f89e833f40db9e670e0d9e8)
                check_type(argname="argument channel_target_info", value=channel_target_info, expected_type=type_hints["channel_target_info"])
                check_type(argname="argument contact_target_info", value=contact_target_info, expected_type=type_hints["contact_target_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_target_info is not None:
                self._values["channel_target_info"] = channel_target_info
            if contact_target_info is not None:
                self._values["contact_target_info"] = contact_target_info

        @builtins.property
        def channel_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ChannelTargetInfoProperty"]]:
            '''Information about the contact channel that Incident Manager engages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html#cfn-ssmcontacts-contact-targets-channeltargetinfo
            '''
            result = self._values.get("channel_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ChannelTargetInfoProperty"]], result)

        @builtins.property
        def contact_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ContactTargetInfoProperty"]]:
            '''The contact that Incident Manager is engaging during an incident.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html#cfn-ssmcontacts-contact-targets-contacttargetinfo
            '''
            result = self._values.get("contact_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContact.ContactTargetInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnContactChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContactChannel",
):
    '''A CloudFormation ``AWS::SSMContacts::ContactChannel``.

    The ``AWS::SSMContacts::ContactChannel`` resource specifies a contact channel as the method that Incident Manager uses to engage your contact.

    :cloudformationResource: AWS::SSMContacts::ContactChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ssmcontacts as ssmcontacts
        
        cfn_contact_channel = ssmcontacts.CfnContactChannel(self, "MyCfnContactChannel",
            channel_address="channelAddress",
            channel_name="channelName",
            channel_type="channelType",
            contact_id="contactId",
        
            # the properties below are optional
            defer_activation=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        channel_address: builtins.str,
        channel_name: builtins.str,
        channel_type: builtins.str,
        contact_id: builtins.str,
        defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::SSMContacts::ContactChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_address: The details that Incident Manager uses when trying to engage the contact channel.
        :param channel_name: The name of the contact channel.
        :param channel_type: The type of the contact channel. Incident Manager supports three contact methods:. - SMS - VOICE - EMAIL
        :param contact_id: The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.
        :param defer_activation: If you want to activate the channel at a later time, you can choose to defer activation. Incident Manager can't engage your contact channel until it has been activated.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d584ba0b5aff43f1a9062084e38be6f778d720246269c38be2f7bef856655007)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactChannelProps(
            channel_address=channel_address,
            channel_name=channel_name,
            channel_type=channel_type,
            contact_id=contact_id,
            defer_activation=defer_activation,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53085b1f93febe9f9fa294dc08e8ac5dbf1eecc0515dfab3d618f15e61d6d6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0239a9c28f5fd7b8f3a42f37bb2f970b102231ca1d94ce3c54a587c498e7d72e)
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
        '''The Amazon Resource Name (ARN) of the ``ContactChannel`` resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="channelAddress")
    def channel_address(self) -> builtins.str:
        '''The details that Incident Manager uses when trying to engage the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeladdress
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelAddress"))

    @channel_address.setter
    def channel_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b669043cb87e273af0357e950e61da4c14c15610728d1560c4bcff3a8cff6d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelAddress", value)

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        '''The name of the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channelname
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d135ce0b08cf07ac49939b1eb041ef56facd3c38aed94f6d137f621b8dd8c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value)

    @builtins.property
    @jsii.member(jsii_name="channelType")
    def channel_type(self) -> builtins.str:
        '''The type of the contact channel. Incident Manager supports three contact methods:.

        - SMS
        - VOICE
        - EMAIL

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeltype
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelType"))

    @channel_type.setter
    def channel_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c7101bcf899d638eabab4a048401067920e2213afa7ea8c504273ec1512a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelType", value)

    @builtins.property
    @jsii.member(jsii_name="contactId")
    def contact_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-contactid
        '''
        return typing.cast(builtins.str, jsii.get(self, "contactId"))

    @contact_id.setter
    def contact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2eb9dd7b9c19d9ec61bf2a3b780b5e6e3c94ae1eaf258d88b66a150785f401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactId", value)

    @builtins.property
    @jsii.member(jsii_name="deferActivation")
    def defer_activation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''If you want to activate the channel at a later time, you can choose to defer activation.

        Incident Manager can't engage your contact channel until it has been activated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-deferactivation
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deferActivation"))

    @defer_activation.setter
    def defer_activation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8950bb0b7e2de2e25c77de7d5dbf6bdbaa3a77e7d3db453d8be0f3fe5203e062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deferActivation", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContactChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_address": "channelAddress",
        "channel_name": "channelName",
        "channel_type": "channelType",
        "contact_id": "contactId",
        "defer_activation": "deferActivation",
    },
)
class CfnContactChannelProps:
    def __init__(
        self,
        *,
        channel_address: builtins.str,
        channel_name: builtins.str,
        channel_type: builtins.str,
        contact_id: builtins.str,
        defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactChannel``.

        :param channel_address: The details that Incident Manager uses when trying to engage the contact channel.
        :param channel_name: The name of the contact channel.
        :param channel_type: The type of the contact channel. Incident Manager supports three contact methods:. - SMS - VOICE - EMAIL
        :param contact_id: The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.
        :param defer_activation: If you want to activate the channel at a later time, you can choose to defer activation. Incident Manager can't engage your contact channel until it has been activated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ssmcontacts as ssmcontacts
            
            cfn_contact_channel_props = ssmcontacts.CfnContactChannelProps(
                channel_address="channelAddress",
                channel_name="channelName",
                channel_type="channelType",
                contact_id="contactId",
            
                # the properties below are optional
                defer_activation=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb34361fd8f5369e85c8e58a72f8a65d8e00b9cdb5e0de7b51360435ba152dc1)
            check_type(argname="argument channel_address", value=channel_address, expected_type=type_hints["channel_address"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument channel_type", value=channel_type, expected_type=type_hints["channel_type"])
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
            check_type(argname="argument defer_activation", value=defer_activation, expected_type=type_hints["defer_activation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_address": channel_address,
            "channel_name": channel_name,
            "channel_type": channel_type,
            "contact_id": contact_id,
        }
        if defer_activation is not None:
            self._values["defer_activation"] = defer_activation

    @builtins.property
    def channel_address(self) -> builtins.str:
        '''The details that Incident Manager uses when trying to engage the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeladdress
        '''
        result = self._values.get("channel_address")
        assert result is not None, "Required property 'channel_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''The name of the contact channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channelname
        '''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_type(self) -> builtins.str:
        '''The type of the contact channel. Incident Manager supports three contact methods:.

        - SMS
        - VOICE
        - EMAIL

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeltype
        '''
        result = self._values.get("channel_type")
        assert result is not None, "Required property 'channel_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contact_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-contactid
        '''
        result = self._values.get("contact_id")
        assert result is not None, "Required property 'contact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def defer_activation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''If you want to activate the channel at a later time, you can choose to defer activation.

        Incident Manager can't engage your contact channel until it has been activated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-deferactivation
        '''
        result = self._values.get("defer_activation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnContactProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "display_name": "displayName",
        "type": "type",
        "plan": "plan",
    },
)
class CfnContactProps:
    def __init__(
        self,
        *,
        alias: builtins.str,
        display_name: builtins.str,
        type: builtins.str,
        plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnContact.StageProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContact``.

        :param alias: The unique and identifiable alias of the contact or escalation plan.
        :param display_name: The full name of the contact or escalation plan.
        :param type: Refers to the type of contact:. - ``PERSONAL`` : A single, individual contact. - ``ESCALATION`` : An escalation plan. - ``ONCALL_SCHEDULE`` : An on-call schedule.
        :param plan: A list of stages. A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ssmcontacts as ssmcontacts
            
            cfn_contact_props = ssmcontacts.CfnContactProps(
                alias="alias",
                display_name="displayName",
                type="type",
            
                # the properties below are optional
                plan=[ssmcontacts.CfnContact.StageProperty(
                    duration_in_minutes=123,
                    rotation_ids=["rotationIds"],
                    targets=[ssmcontacts.CfnContact.TargetsProperty(
                        channel_target_info=ssmcontacts.CfnContact.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts.CfnContact.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3cef560502ef946eae9a24a973123fbbe837d048d060e9dc0b6f9e02dfa28e)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
            "display_name": display_name,
            "type": type,
        }
        if plan is not None:
            self._values["plan"] = plan

    @builtins.property
    def alias(self) -> builtins.str:
        '''The unique and identifiable alias of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-alias
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The full name of the contact or escalation plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-displayname
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Refers to the type of contact:.

        - ``PERSONAL`` : A single, individual contact.
        - ``ESCALATION`` : An escalation plan.
        - ``ONCALL_SCHEDULE`` : An on-call schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnContact.StageProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of stages.

        A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-plan
        '''
        result = self._values.get("plan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnContact.StageProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPlan(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnPlan",
):
    '''A CloudFormation ``AWS::SSMContacts::Plan``.

    Information about the stages and on-call rotation teams associated with an escalation plan or engagement plan.

    :cloudformationResource: AWS::SSMContacts::Plan
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ssmcontacts as ssmcontacts
        
        cfn_plan = ssmcontacts.CfnPlan(self, "MyCfnPlan",
            contact_id="contactId",
        
            # the properties below are optional
            rotation_ids=["rotationIds"],
            stages=[ssmcontacts.CfnPlan.StageProperty(
                duration_in_minutes=123,
        
                # the properties below are optional
                targets=[ssmcontacts.CfnPlan.TargetsProperty(
                    channel_target_info=ssmcontacts.CfnPlan.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts.CfnPlan.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )]
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        contact_id: builtins.str,
        rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        stages: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPlan.StageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SSMContacts::Plan``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param contact_id: The Amazon Resource Name (ARN) of the contact.
        :param rotation_ids: The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.
        :param stages: A list of stages that the escalation plan or engagement plan uses to engage contacts and contact methods.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f7731ae7cadc465b8f6d1298b8174169efafdae7400753998a711f67b7b148)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPlanProps(
            contact_id=contact_id, rotation_ids=rotation_ids, stages=stages
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70ef7afd785c513ebad17f02656d0b36f5d73abf8d2886ad6b542e857c25d36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__484eb9cad9442d679f93f93e9e79eeebc22b8ed72378aff23c7c98e422e0d641)
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
        '''The Amazon Resource Name (ARN) of the ``Plan`` resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="contactId")
    def contact_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the contact.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-contactid
        '''
        return typing.cast(builtins.str, jsii.get(self, "contactId"))

    @contact_id.setter
    def contact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286a62d9068e521300c8f37b1d1651381c6c38263e851f19bd181fa7674755e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactId", value)

    @builtins.property
    @jsii.member(jsii_name="rotationIds")
    def rotation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-rotationids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rotationIds"))

    @rotation_ids.setter
    def rotation_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318e4c5ddeb085140d95f38d304534bac3da7cd53dd98cee43d9c4cd23e369c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationIds", value)

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.StageProperty"]]]]:
        '''A list of stages that the escalation plan or engagement plan uses to engage contacts and contact methods.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-stages
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.StageProperty"]]]], jsii.get(self, "stages"))

    @stages.setter
    def stages(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.StageProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a973d5c9db7666cd32b1d08d65eb520b24e3e41b97805b595be2d46f939abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stages", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnPlan.ChannelTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_id": "channelId",
            "retry_interval_in_minutes": "retryIntervalInMinutes",
        },
    )
    class ChannelTargetInfoProperty:
        def __init__(
            self,
            *,
            channel_id: builtins.str,
            retry_interval_in_minutes: jsii.Number,
        ) -> None:
            '''Information about the contact channel that Incident Manager uses to engage the contact.

            :param channel_id: The Amazon Resource Name (ARN) of the contact channel.
            :param retry_interval_in_minutes: The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-channeltargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                channel_target_info_property = ssmcontacts.CfnPlan.ChannelTargetInfoProperty(
                    channel_id="channelId",
                    retry_interval_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75bb223ed15862fee5e6c3274209a81f91d6a7db028ab2a02200fbb62e881d59)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument retry_interval_in_minutes", value=retry_interval_in_minutes, expected_type=type_hints["retry_interval_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "channel_id": channel_id,
                "retry_interval_in_minutes": retry_interval_in_minutes,
            }

        @builtins.property
        def channel_id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the contact channel.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-channeltargetinfo.html#cfn-ssmcontacts-plan-channeltargetinfo-channelid
            '''
            result = self._values.get("channel_id")
            assert result is not None, "Required property 'channel_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def retry_interval_in_minutes(self) -> jsii.Number:
            '''The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-channeltargetinfo.html#cfn-ssmcontacts-plan-channeltargetinfo-retryintervalinminutes
            '''
            result = self._values.get("retry_interval_in_minutes")
            assert result is not None, "Required property 'retry_interval_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnPlan.ContactTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_id": "contactId", "is_essential": "isEssential"},
    )
    class ContactTargetInfoProperty:
        def __init__(
            self,
            *,
            contact_id: builtins.str,
            is_essential: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''The contact that Incident Manager is engaging during an incident.

            :param contact_id: The Amazon Resource Name (ARN) of the contact.
            :param is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-contacttargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                contact_target_info_property = ssmcontacts.CfnPlan.ContactTargetInfoProperty(
                    contact_id="contactId",
                    is_essential=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15e73b2e8251d29683a70b350f18c7ddf5503aaccf1a13905fdb097ff640223d)
                check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
                check_type(argname="argument is_essential", value=is_essential, expected_type=type_hints["is_essential"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_id": contact_id,
                "is_essential": is_essential,
            }

        @builtins.property
        def contact_id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-contacttargetinfo.html#cfn-ssmcontacts-plan-contacttargetinfo-contactid
            '''
            result = self._values.get("contact_id")
            assert result is not None, "Required property 'contact_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_essential(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-contacttargetinfo.html#cfn-ssmcontacts-plan-contacttargetinfo-isessential
            '''
            result = self._values.get("is_essential")
            assert result is not None, "Required property 'is_essential' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContactTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnPlan.StageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_in_minutes": "durationInMinutes",
            "targets": "targets",
        },
    )
    class StageProperty:
        def __init__(
            self,
            *,
            duration_in_minutes: jsii.Number,
            targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPlan.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.

            :param duration_in_minutes: The time to wait until beginning the next stage. The duration can only be set to 0 if a target is specified.
            :param targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-stage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                stage_property = ssmcontacts.CfnPlan.StageProperty(
                    duration_in_minutes=123,
                
                    # the properties below are optional
                    targets=[ssmcontacts.CfnPlan.TargetsProperty(
                        channel_target_info=ssmcontacts.CfnPlan.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts.CfnPlan.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da2f7b35f9ac3c67e721a4f4e0b223a65696ee98e794de624db55c590cc6c3e2)
                check_type(argname="argument duration_in_minutes", value=duration_in_minutes, expected_type=type_hints["duration_in_minutes"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "duration_in_minutes": duration_in_minutes,
            }
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def duration_in_minutes(self) -> jsii.Number:
            '''The time to wait until beginning the next stage.

            The duration can only be set to 0 if a target is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-stage.html#cfn-ssmcontacts-plan-stage-durationinminutes
            '''
            result = self._values.get("duration_in_minutes")
            assert result is not None, "Required property 'duration_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.TargetsProperty"]]]]:
            '''The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-stage.html#cfn-ssmcontacts-plan-stage-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.TargetsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnPlan.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_target_info": "channelTargetInfo",
            "contact_target_info": "contactTargetInfo",
        },
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            channel_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPlan.ChannelTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            contact_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPlan.ContactTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The contact or contact channel that's being engaged.

            :param channel_target_info: Information about the contact channel that Incident Manager engages.
            :param contact_target_info: Information about the contact that Incident Manager engages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                targets_property = ssmcontacts.CfnPlan.TargetsProperty(
                    channel_target_info=ssmcontacts.CfnPlan.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts.CfnPlan.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9030e58d90766c29c2acb1bae4a1f458e8ac050fe474dc0a3e1ed2968774a35)
                check_type(argname="argument channel_target_info", value=channel_target_info, expected_type=type_hints["channel_target_info"])
                check_type(argname="argument contact_target_info", value=contact_target_info, expected_type=type_hints["contact_target_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_target_info is not None:
                self._values["channel_target_info"] = channel_target_info
            if contact_target_info is not None:
                self._values["contact_target_info"] = contact_target_info

        @builtins.property
        def channel_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.ChannelTargetInfoProperty"]]:
            '''Information about the contact channel that Incident Manager engages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-targets.html#cfn-ssmcontacts-plan-targets-channeltargetinfo
            '''
            result = self._values.get("channel_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.ChannelTargetInfoProperty"]], result)

        @builtins.property
        def contact_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.ContactTargetInfoProperty"]]:
            '''Information about the contact that Incident Manager engages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-targets.html#cfn-ssmcontacts-plan-targets-contacttargetinfo
            '''
            result = self._values.get("contact_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlan.ContactTargetInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnPlanProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_id": "contactId",
        "rotation_ids": "rotationIds",
        "stages": "stages",
    },
)
class CfnPlanProps:
    def __init__(
        self,
        *,
        contact_id: builtins.str,
        rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        stages: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlan.StageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPlan``.

        :param contact_id: The Amazon Resource Name (ARN) of the contact.
        :param rotation_ids: The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.
        :param stages: A list of stages that the escalation plan or engagement plan uses to engage contacts and contact methods.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ssmcontacts as ssmcontacts
            
            cfn_plan_props = ssmcontacts.CfnPlanProps(
                contact_id="contactId",
            
                # the properties below are optional
                rotation_ids=["rotationIds"],
                stages=[ssmcontacts.CfnPlan.StageProperty(
                    duration_in_minutes=123,
            
                    # the properties below are optional
                    targets=[ssmcontacts.CfnPlan.TargetsProperty(
                        channel_target_info=ssmcontacts.CfnPlan.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts.CfnPlan.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ff1d530a4cb5bf6c16887acac081ff7c7b379b92acea7a6b009133490ec573)
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
            check_type(argname="argument rotation_ids", value=rotation_ids, expected_type=type_hints["rotation_ids"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact_id": contact_id,
        }
        if rotation_ids is not None:
            self._values["rotation_ids"] = rotation_ids
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def contact_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the contact.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-contactid
        '''
        result = self._values.get("contact_id")
        assert result is not None, "Required property 'contact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rotation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-rotationids
        '''
        result = self._values.get("rotation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stages(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPlan.StageProperty]]]]:
        '''A list of stages that the escalation plan or engagement plan uses to engage contacts and contact methods.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-stages
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPlan.StageProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRotation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotation",
):
    '''A CloudFormation ``AWS::SSMContacts::Rotation``.

    Specifies a rotation in an on-call schedule.

    :cloudformationResource: AWS::SSMContacts::Rotation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ssmcontacts as ssmcontacts
        
        cfn_rotation = ssmcontacts.CfnRotation(self, "MyCfnRotation",
            contact_ids=["contactIds"],
            name="name",
            recurrence=ssmcontacts.CfnRotation.RecurrenceSettingsProperty(
                number_of_on_calls=123,
                recurrence_multiplier=123,
        
                # the properties below are optional
                daily_settings=["dailySettings"],
                monthly_settings=[ssmcontacts.CfnRotation.MonthlySettingProperty(
                    day_of_month=123,
                    hand_off_time="handOffTime"
                )],
                shift_coverages=[ssmcontacts.CfnRotation.ShiftCoverageProperty(
                    coverage_times=[ssmcontacts.CfnRotation.CoverageTimeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    day_of_week="dayOfWeek"
                )],
                weekly_settings=[ssmcontacts.CfnRotation.WeeklySettingProperty(
                    day_of_week="dayOfWeek",
                    hand_off_time="handOffTime"
                )]
            ),
            start_time="startTime",
            time_zone_id="timeZoneId",
        
            # the properties below are optional
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
        contact_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        recurrence: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRotation.RecurrenceSettingsProperty", typing.Dict[builtins.str, typing.Any]]],
        start_time: builtins.str,
        time_zone_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SSMContacts::Rotation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param contact_ids: The Amazon Resource Names (ARNs) of the contacts to add to the rotation. The order in which you list the contacts is their shift order in the rotation schedule.
        :param name: The name for the rotation.
        :param recurrence: Information about the rule that specifies when shift team members rotate.
        :param start_time: The date and time the rotation goes into effect.
        :param time_zone_id: The time zone to base the rotation’s activity on, in Internet Assigned Numbers Authority (IANA) format. For example: "America/Los_Angeles", "UTC", or "Asia/Seoul". For more information, see the `Time Zone Database <https://docs.aws.amazon.com/https://www.iana.org/time-zones>`_ on the IANA website.
        :param tags: Optional metadata to assign to the rotation. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For more information, see `Tagging Incident Manager resources <https://docs.aws.amazon.com/incident-manager/latest/userguide/tagging.html>`_ in the *Incident Manager User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854a2a987aacf65e19a3b8964bcb2c3adaa75c4a503d122ccc0650b92d35a922)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRotationProps(
            contact_ids=contact_ids,
            name=name,
            recurrence=recurrence,
            start_time=start_time,
            time_zone_id=time_zone_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e178ddbe4c03d18b0bbda9bdd03a7720738100a765314d1222a26d30c5577d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a0c80f70a27b3531dcad0f6e7ddb5b3da5193b31fc26e9985997e22330d1e07)
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
        '''The Amazon Resource Name (ARN) of the ``Rotation`` resource.

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
        '''Optional metadata to assign to the rotation.

        Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For more information, see `Tagging Incident Manager resources <https://docs.aws.amazon.com/incident-manager/latest/userguide/tagging.html>`_ in the *Incident Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="contactIds")
    def contact_ids(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the contacts to add to the rotation.

        The order in which you list the contacts is their shift order in the rotation schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-contactids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contactIds"))

    @contact_ids.setter
    def contact_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126cc3406b8f0aa565a5a5ccc2c7b656ed32ab644500a50d91dd1482dc75aa89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactIds", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for the rotation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8540a9e5401fe9cf21b9ff88ef4fa8a11afc97400fe204a95dad0e5778fa889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.RecurrenceSettingsProperty"]:
        '''Information about the rule that specifies when shift team members rotate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-recurrence
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.RecurrenceSettingsProperty"], jsii.get(self, "recurrence"))

    @recurrence.setter
    def recurrence(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.RecurrenceSettingsProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb211effa851617a8618a37315069a627691371db0ff0a8d42161c5431ce8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrence", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        '''The date and time the rotation goes into effect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-starttime
        '''
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad487ed52e9b6937b315e815fd0cd899ce2eaaebd14b3cec11a47b9f96fe80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="timeZoneId")
    def time_zone_id(self) -> builtins.str:
        '''The time zone to base the rotation’s activity on, in Internet Assigned Numbers Authority (IANA) format.

        For example: "America/Los_Angeles", "UTC", or "Asia/Seoul". For more information, see the `Time Zone Database <https://docs.aws.amazon.com/https://www.iana.org/time-zones>`_ on the IANA website.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-timezoneid
        '''
        return typing.cast(builtins.str, jsii.get(self, "timeZoneId"))

    @time_zone_id.setter
    def time_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4a24f32d54355c8dfce2dff6147cbd741aa5be5d0f85f5fc9b62de74487eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZoneId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotation.CoverageTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end_time": "endTime", "start_time": "startTime"},
    )
    class CoverageTimeProperty:
        def __init__(self, *, end_time: builtins.str, start_time: builtins.str) -> None:
            '''Information about when an on-call shift begins and ends.

            :param end_time: Information about when an on-call rotation shift ends.
            :param start_time: Information about when an on-call rotation shift begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-coveragetime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                coverage_time_property = ssmcontacts.CfnRotation.CoverageTimeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d82d4ceed0fa0711c70f213449e968ceaa203fd47b2b2ab28153398966025239)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end_time": end_time,
                "start_time": start_time,
            }

        @builtins.property
        def end_time(self) -> builtins.str:
            '''Information about when an on-call rotation shift ends.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-coveragetime.html#cfn-ssmcontacts-rotation-coveragetime-endtime
            '''
            result = self._values.get("end_time")
            assert result is not None, "Required property 'end_time' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start_time(self) -> builtins.str:
            '''Information about when an on-call rotation shift begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-coveragetime.html#cfn-ssmcontacts-rotation-coveragetime-starttime
            '''
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoverageTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotation.MonthlySettingProperty",
        jsii_struct_bases=[],
        name_mapping={"day_of_month": "dayOfMonth", "hand_off_time": "handOffTime"},
    )
    class MonthlySettingProperty:
        def __init__(
            self,
            *,
            day_of_month: jsii.Number,
            hand_off_time: builtins.str,
        ) -> None:
            '''Information about on-call rotations that recur monthly.

            :param day_of_month: The day of the month when monthly recurring on-call rotations begin.
            :param hand_off_time: The time of day when a monthly recurring on-call shift rotation begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-monthlysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                monthly_setting_property = ssmcontacts.CfnRotation.MonthlySettingProperty(
                    day_of_month=123,
                    hand_off_time="handOffTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e706dbc17ac33d517e892f70e9e2206fa3f89165a4605777328b0edaff991273)
                check_type(argname="argument day_of_month", value=day_of_month, expected_type=type_hints["day_of_month"])
                check_type(argname="argument hand_off_time", value=hand_off_time, expected_type=type_hints["hand_off_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "day_of_month": day_of_month,
                "hand_off_time": hand_off_time,
            }

        @builtins.property
        def day_of_month(self) -> jsii.Number:
            '''The day of the month when monthly recurring on-call rotations begin.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-monthlysetting.html#cfn-ssmcontacts-rotation-monthlysetting-dayofmonth
            '''
            result = self._values.get("day_of_month")
            assert result is not None, "Required property 'day_of_month' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def hand_off_time(self) -> builtins.str:
            '''The time of day when a monthly recurring on-call shift rotation begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-monthlysetting.html#cfn-ssmcontacts-rotation-monthlysetting-handofftime
            '''
            result = self._values.get("hand_off_time")
            assert result is not None, "Required property 'hand_off_time' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonthlySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotation.RecurrenceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "number_of_on_calls": "numberOfOnCalls",
            "recurrence_multiplier": "recurrenceMultiplier",
            "daily_settings": "dailySettings",
            "monthly_settings": "monthlySettings",
            "shift_coverages": "shiftCoverages",
            "weekly_settings": "weeklySettings",
        },
    )
    class RecurrenceSettingsProperty:
        def __init__(
            self,
            *,
            number_of_on_calls: jsii.Number,
            recurrence_multiplier: jsii.Number,
            daily_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
            monthly_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRotation.MonthlySettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            shift_coverages: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRotation.ShiftCoverageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            weekly_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRotation.WeeklySettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about when an on-call rotation is in effect and how long the rotation period lasts.

            :param number_of_on_calls: The number of contacts, or shift team members designated to be on call concurrently during a shift. For example, in an on-call schedule that contains ten contacts, a value of ``2`` designates that two of them are on call at any given time.
            :param recurrence_multiplier: The number of days, weeks, or months a single rotation lasts.
            :param daily_settings: Information about on-call rotations that recur daily.
            :param monthly_settings: Information about on-call rotations that recur monthly.
            :param shift_coverages: Information about the days of the week included in on-call rotation coverage.
            :param weekly_settings: Information about on-call rotations that recur weekly.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                recurrence_settings_property = ssmcontacts.CfnRotation.RecurrenceSettingsProperty(
                    number_of_on_calls=123,
                    recurrence_multiplier=123,
                
                    # the properties below are optional
                    daily_settings=["dailySettings"],
                    monthly_settings=[ssmcontacts.CfnRotation.MonthlySettingProperty(
                        day_of_month=123,
                        hand_off_time="handOffTime"
                    )],
                    shift_coverages=[ssmcontacts.CfnRotation.ShiftCoverageProperty(
                        coverage_times=[ssmcontacts.CfnRotation.CoverageTimeProperty(
                            end_time="endTime",
                            start_time="startTime"
                        )],
                        day_of_week="dayOfWeek"
                    )],
                    weekly_settings=[ssmcontacts.CfnRotation.WeeklySettingProperty(
                        day_of_week="dayOfWeek",
                        hand_off_time="handOffTime"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a907f9e11211f8c4a295ab0d8511cbed36d986fe0d88aa47d9850dbc1b815ab7)
                check_type(argname="argument number_of_on_calls", value=number_of_on_calls, expected_type=type_hints["number_of_on_calls"])
                check_type(argname="argument recurrence_multiplier", value=recurrence_multiplier, expected_type=type_hints["recurrence_multiplier"])
                check_type(argname="argument daily_settings", value=daily_settings, expected_type=type_hints["daily_settings"])
                check_type(argname="argument monthly_settings", value=monthly_settings, expected_type=type_hints["monthly_settings"])
                check_type(argname="argument shift_coverages", value=shift_coverages, expected_type=type_hints["shift_coverages"])
                check_type(argname="argument weekly_settings", value=weekly_settings, expected_type=type_hints["weekly_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "number_of_on_calls": number_of_on_calls,
                "recurrence_multiplier": recurrence_multiplier,
            }
            if daily_settings is not None:
                self._values["daily_settings"] = daily_settings
            if monthly_settings is not None:
                self._values["monthly_settings"] = monthly_settings
            if shift_coverages is not None:
                self._values["shift_coverages"] = shift_coverages
            if weekly_settings is not None:
                self._values["weekly_settings"] = weekly_settings

        @builtins.property
        def number_of_on_calls(self) -> jsii.Number:
            '''The number of contacts, or shift team members designated to be on call concurrently during a shift.

            For example, in an on-call schedule that contains ten contacts, a value of ``2`` designates that two of them are on call at any given time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-numberofoncalls
            '''
            result = self._values.get("number_of_on_calls")
            assert result is not None, "Required property 'number_of_on_calls' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def recurrence_multiplier(self) -> jsii.Number:
            '''The number of days, weeks, or months a single rotation lasts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-recurrencemultiplier
            '''
            result = self._values.get("recurrence_multiplier")
            assert result is not None, "Required property 'recurrence_multiplier' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def daily_settings(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Information about on-call rotations that recur daily.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-dailysettings
            '''
            result = self._values.get("daily_settings")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def monthly_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.MonthlySettingProperty"]]]]:
            '''Information about on-call rotations that recur monthly.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-monthlysettings
            '''
            result = self._values.get("monthly_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.MonthlySettingProperty"]]]], result)

        @builtins.property
        def shift_coverages(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.ShiftCoverageProperty"]]]]:
            '''Information about the days of the week included in on-call rotation coverage.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-shiftcoverages
            '''
            result = self._values.get("shift_coverages")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.ShiftCoverageProperty"]]]], result)

        @builtins.property
        def weekly_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.WeeklySettingProperty"]]]]:
            '''Information about on-call rotations that recur weekly.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-weeklysettings
            '''
            result = self._values.get("weekly_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.WeeklySettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecurrenceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotation.ShiftCoverageProperty",
        jsii_struct_bases=[],
        name_mapping={"coverage_times": "coverageTimes", "day_of_week": "dayOfWeek"},
    )
    class ShiftCoverageProperty:
        def __init__(
            self,
            *,
            coverage_times: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRotation.CoverageTimeProperty", typing.Dict[builtins.str, typing.Any]]]]],
            day_of_week: builtins.str,
        ) -> None:
            '''Information about the days of the week that the on-call rotation coverage includes.

            :param coverage_times: The start and end times of the shift.
            :param day_of_week: A list of days on which the schedule is active.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-shiftcoverage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                shift_coverage_property = ssmcontacts.CfnRotation.ShiftCoverageProperty(
                    coverage_times=[ssmcontacts.CfnRotation.CoverageTimeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    day_of_week="dayOfWeek"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be5d4bf370bdcdaaa6bd91f810c3cf1e50bdce02f6472d385a832e7ebe9aca42)
                check_type(argname="argument coverage_times", value=coverage_times, expected_type=type_hints["coverage_times"])
                check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "coverage_times": coverage_times,
                "day_of_week": day_of_week,
            }

        @builtins.property
        def coverage_times(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.CoverageTimeProperty"]]]:
            '''The start and end times of the shift.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-shiftcoverage.html#cfn-ssmcontacts-rotation-shiftcoverage-coveragetimes
            '''
            result = self._values.get("coverage_times")
            assert result is not None, "Required property 'coverage_times' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRotation.CoverageTimeProperty"]]], result)

        @builtins.property
        def day_of_week(self) -> builtins.str:
            '''A list of days on which the schedule is active.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-shiftcoverage.html#cfn-ssmcontacts-rotation-shiftcoverage-dayofweek
            '''
            result = self._values.get("day_of_week")
            assert result is not None, "Required property 'day_of_week' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShiftCoverageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotation.WeeklySettingProperty",
        jsii_struct_bases=[],
        name_mapping={"day_of_week": "dayOfWeek", "hand_off_time": "handOffTime"},
    )
    class WeeklySettingProperty:
        def __init__(
            self,
            *,
            day_of_week: builtins.str,
            hand_off_time: builtins.str,
        ) -> None:
            '''Information about rotations that recur weekly.

            :param day_of_week: The day of the week when weekly recurring on-call shift rotations begins.
            :param hand_off_time: The time of day when a weekly recurring on-call shift rotation begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-weeklysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ssmcontacts as ssmcontacts
                
                weekly_setting_property = ssmcontacts.CfnRotation.WeeklySettingProperty(
                    day_of_week="dayOfWeek",
                    hand_off_time="handOffTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea18eca665906c9ba9a89e04616774ceda2ff1ec61c808b3d7e3cfbb0b9df8ed)
                check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
                check_type(argname="argument hand_off_time", value=hand_off_time, expected_type=type_hints["hand_off_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "day_of_week": day_of_week,
                "hand_off_time": hand_off_time,
            }

        @builtins.property
        def day_of_week(self) -> builtins.str:
            '''The day of the week when weekly recurring on-call shift rotations begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-weeklysetting.html#cfn-ssmcontacts-rotation-weeklysetting-dayofweek
            '''
            result = self._values.get("day_of_week")
            assert result is not None, "Required property 'day_of_week' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hand_off_time(self) -> builtins.str:
            '''The time of day when a weekly recurring on-call shift rotation begins.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-weeklysetting.html#cfn-ssmcontacts-rotation-weeklysetting-handofftime
            '''
            result = self._values.get("hand_off_time")
            assert result is not None, "Required property 'hand_off_time' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeeklySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssmcontacts.CfnRotationProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_ids": "contactIds",
        "name": "name",
        "recurrence": "recurrence",
        "start_time": "startTime",
        "time_zone_id": "timeZoneId",
        "tags": "tags",
    },
)
class CfnRotationProps:
    def __init__(
        self,
        *,
        contact_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        recurrence: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.RecurrenceSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
        start_time: builtins.str,
        time_zone_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRotation``.

        :param contact_ids: The Amazon Resource Names (ARNs) of the contacts to add to the rotation. The order in which you list the contacts is their shift order in the rotation schedule.
        :param name: The name for the rotation.
        :param recurrence: Information about the rule that specifies when shift team members rotate.
        :param start_time: The date and time the rotation goes into effect.
        :param time_zone_id: The time zone to base the rotation’s activity on, in Internet Assigned Numbers Authority (IANA) format. For example: "America/Los_Angeles", "UTC", or "Asia/Seoul". For more information, see the `Time Zone Database <https://docs.aws.amazon.com/https://www.iana.org/time-zones>`_ on the IANA website.
        :param tags: Optional metadata to assign to the rotation. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For more information, see `Tagging Incident Manager resources <https://docs.aws.amazon.com/incident-manager/latest/userguide/tagging.html>`_ in the *Incident Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ssmcontacts as ssmcontacts
            
            cfn_rotation_props = ssmcontacts.CfnRotationProps(
                contact_ids=["contactIds"],
                name="name",
                recurrence=ssmcontacts.CfnRotation.RecurrenceSettingsProperty(
                    number_of_on_calls=123,
                    recurrence_multiplier=123,
            
                    # the properties below are optional
                    daily_settings=["dailySettings"],
                    monthly_settings=[ssmcontacts.CfnRotation.MonthlySettingProperty(
                        day_of_month=123,
                        hand_off_time="handOffTime"
                    )],
                    shift_coverages=[ssmcontacts.CfnRotation.ShiftCoverageProperty(
                        coverage_times=[ssmcontacts.CfnRotation.CoverageTimeProperty(
                            end_time="endTime",
                            start_time="startTime"
                        )],
                        day_of_week="dayOfWeek"
                    )],
                    weekly_settings=[ssmcontacts.CfnRotation.WeeklySettingProperty(
                        day_of_week="dayOfWeek",
                        hand_off_time="handOffTime"
                    )]
                ),
                start_time="startTime",
                time_zone_id="timeZoneId",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1051125233a1a1a57dd75114e97ca708fc78079afab3ccdce36eb558aad742f9)
            check_type(argname="argument contact_ids", value=contact_ids, expected_type=type_hints["contact_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument time_zone_id", value=time_zone_id, expected_type=type_hints["time_zone_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact_ids": contact_ids,
            "name": name,
            "recurrence": recurrence,
            "start_time": start_time,
            "time_zone_id": time_zone_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def contact_ids(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the contacts to add to the rotation.

        The order in which you list the contacts is their shift order in the rotation schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-contactids
        '''
        result = self._values.get("contact_ids")
        assert result is not None, "Required property 'contact_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for the rotation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRotation.RecurrenceSettingsProperty]:
        '''Information about the rule that specifies when shift team members rotate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-recurrence
        '''
        result = self._values.get("recurrence")
        assert result is not None, "Required property 'recurrence' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRotation.RecurrenceSettingsProperty], result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''The date and time the rotation goes into effect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-starttime
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone_id(self) -> builtins.str:
        '''The time zone to base the rotation’s activity on, in Internet Assigned Numbers Authority (IANA) format.

        For example: "America/Los_Angeles", "UTC", or "Asia/Seoul". For more information, see the `Time Zone Database <https://docs.aws.amazon.com/https://www.iana.org/time-zones>`_ on the IANA website.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-timezoneid
        '''
        result = self._values.get("time_zone_id")
        assert result is not None, "Required property 'time_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Optional metadata to assign to the rotation.

        Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For more information, see `Tagging Incident Manager resources <https://docs.aws.amazon.com/incident-manager/latest/userguide/tagging.html>`_ in the *Incident Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRotationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnContact",
    "CfnContactChannel",
    "CfnContactChannelProps",
    "CfnContactProps",
    "CfnPlan",
    "CfnPlanProps",
    "CfnRotation",
    "CfnRotationProps",
]

publication.publish()

def _typecheckingstub__1a6ca3ad36cfd3d6487f8dd1a8ac11bbf921386d1f05da32bbf84640646093d1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    alias: builtins.str,
    display_name: builtins.str,
    type: builtins.str,
    plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnContact.StageProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1230b668b68ef75e2be0ce9ce5bf14b7bd3b3b8b362785f62b8727c5094d5496(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3a35478651edceaa8211ec1ec74ee20552b26c38b90ed6598a8f22b7a3324e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e5a583902645e320f5f0d421b8847dd608990992c74ef2c375c9883591a4e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634d931c33dc249f0a936122628bdb785fe509e48fda71d174f94247ec282c98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e692648e4215a1fe47c884b97b303f2d8f54f2325bc4e89fe8459ba378deceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a5edb5d31e9dd3b301d72fb5451ca492b93ef830ef679d169226bba5835196(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnContact.StageProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1337d37b740eb0596a247fac45b9a6781be3af024b4c695bd779bac6c2fe61c(
    *,
    channel_id: builtins.str,
    retry_interval_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bb2669b4d0ea3739dd8e91f180cb5a526768e1b96634822e01f2d4c19391fc(
    *,
    contact_id: builtins.str,
    is_essential: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdcb9e705292433792b822f72adb7e277c0c72e3b60b4012c590d2ec0dc30bb(
    *,
    duration_in_minutes: typing.Optional[jsii.Number] = None,
    rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContact.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e07482c664cb3a3264fa1f4d90282c886057cd7f89e833f40db9e670e0d9e8(
    *,
    channel_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContact.ChannelTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contact_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContact.ContactTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d584ba0b5aff43f1a9062084e38be6f778d720246269c38be2f7bef856655007(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    channel_address: builtins.str,
    channel_name: builtins.str,
    channel_type: builtins.str,
    contact_id: builtins.str,
    defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53085b1f93febe9f9fa294dc08e8ac5dbf1eecc0515dfab3d618f15e61d6d6a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0239a9c28f5fd7b8f3a42f37bb2f970b102231ca1d94ce3c54a587c498e7d72e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669043cb87e273af0357e950e61da4c14c15610728d1560c4bcff3a8cff6d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d135ce0b08cf07ac49939b1eb041ef56facd3c38aed94f6d137f621b8dd8c5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c7101bcf899d638eabab4a048401067920e2213afa7ea8c504273ec1512a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2eb9dd7b9c19d9ec61bf2a3b780b5e6e3c94ae1eaf258d88b66a150785f401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8950bb0b7e2de2e25c77de7d5dbf6bdbaa3a77e7d3db453d8be0f3fe5203e062(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb34361fd8f5369e85c8e58a72f8a65d8e00b9cdb5e0de7b51360435ba152dc1(
    *,
    channel_address: builtins.str,
    channel_name: builtins.str,
    channel_type: builtins.str,
    contact_id: builtins.str,
    defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3cef560502ef946eae9a24a973123fbbe837d048d060e9dc0b6f9e02dfa28e(
    *,
    alias: builtins.str,
    display_name: builtins.str,
    type: builtins.str,
    plan: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnContact.StageProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f7731ae7cadc465b8f6d1298b8174169efafdae7400753998a711f67b7b148(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    contact_id: builtins.str,
    rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    stages: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlan.StageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70ef7afd785c513ebad17f02656d0b36f5d73abf8d2886ad6b542e857c25d36(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484eb9cad9442d679f93f93e9e79eeebc22b8ed72378aff23c7c98e422e0d641(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286a62d9068e521300c8f37b1d1651381c6c38263e851f19bd181fa7674755e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318e4c5ddeb085140d95f38d304534bac3da7cd53dd98cee43d9c4cd23e369c5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a973d5c9db7666cd32b1d08d65eb520b24e3e41b97805b595be2d46f939abd(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPlan.StageProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bb223ed15862fee5e6c3274209a81f91d6a7db028ab2a02200fbb62e881d59(
    *,
    channel_id: builtins.str,
    retry_interval_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e73b2e8251d29683a70b350f18c7ddf5503aaccf1a13905fdb097ff640223d(
    *,
    contact_id: builtins.str,
    is_essential: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2f7b35f9ac3c67e721a4f4e0b223a65696ee98e794de624db55c590cc6c3e2(
    *,
    duration_in_minutes: jsii.Number,
    targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlan.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9030e58d90766c29c2acb1bae4a1f458e8ac050fe474dc0a3e1ed2968774a35(
    *,
    channel_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlan.ChannelTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contact_target_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlan.ContactTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ff1d530a4cb5bf6c16887acac081ff7c7b379b92acea7a6b009133490ec573(
    *,
    contact_id: builtins.str,
    rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    stages: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlan.StageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854a2a987aacf65e19a3b8964bcb2c3adaa75c4a503d122ccc0650b92d35a922(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    contact_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    recurrence: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.RecurrenceSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
    start_time: builtins.str,
    time_zone_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e178ddbe4c03d18b0bbda9bdd03a7720738100a765314d1222a26d30c5577d8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0c80f70a27b3531dcad0f6e7ddb5b3da5193b31fc26e9985997e22330d1e07(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126cc3406b8f0aa565a5a5ccc2c7b656ed32ab644500a50d91dd1482dc75aa89(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8540a9e5401fe9cf21b9ff88ef4fa8a11afc97400fe204a95dad0e5778fa889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb211effa851617a8618a37315069a627691371db0ff0a8d42161c5431ce8ee(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRotation.RecurrenceSettingsProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad487ed52e9b6937b315e815fd0cd899ce2eaaebd14b3cec11a47b9f96fe80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4a24f32d54355c8dfce2dff6147cbd741aa5be5d0f85f5fc9b62de74487eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82d4ceed0fa0711c70f213449e968ceaa203fd47b2b2ab28153398966025239(
    *,
    end_time: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e706dbc17ac33d517e892f70e9e2206fa3f89165a4605777328b0edaff991273(
    *,
    day_of_month: jsii.Number,
    hand_off_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a907f9e11211f8c4a295ab0d8511cbed36d986fe0d88aa47d9850dbc1b815ab7(
    *,
    number_of_on_calls: jsii.Number,
    recurrence_multiplier: jsii.Number,
    daily_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
    monthly_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.MonthlySettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    shift_coverages: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.ShiftCoverageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    weekly_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.WeeklySettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5d4bf370bdcdaaa6bd91f810c3cf1e50bdce02f6472d385a832e7ebe9aca42(
    *,
    coverage_times: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.CoverageTimeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    day_of_week: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea18eca665906c9ba9a89e04616774ceda2ff1ec61c808b3d7e3cfbb0b9df8ed(
    *,
    day_of_week: builtins.str,
    hand_off_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1051125233a1a1a57dd75114e97ca708fc78079afab3ccdce36eb558aad742f9(
    *,
    contact_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    recurrence: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRotation.RecurrenceSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
    start_time: builtins.str,
    time_zone_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
