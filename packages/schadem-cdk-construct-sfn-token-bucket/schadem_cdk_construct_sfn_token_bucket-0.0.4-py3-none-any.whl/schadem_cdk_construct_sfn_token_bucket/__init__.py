'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions
import constructs


class StepFunctionsTPSTokenBucket(
    aws_cdk.aws_stepfunctions.StateMachineFragment,
    metaclass=jsii.JSIIMeta,
    jsii_type="schadem-cdk-construct-sfn-token-bucket.StepFunctionsTPSTokenBucket",
):
    def __init__(
        self,
        parent: constructs.Construct,
        id: builtins.str,
        *,
        token_limit: jsii.Number,
        sqs_queue: typing.Optional[aws_cdk.aws_sqs.IQueue] = None,
        token_bucket_ddb_table_id: typing.Optional[builtins.str] = None,
        token_bucket_ddb_table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param token_limit: 
        :param sqs_queue: queue to use for the task token requests - allows for distribution of tokens across different workflows. Queue and DDB table should obviously be the same if spreading
        :param token_bucket_ddb_table_id: 
        :param token_bucket_ddb_table_name: 
        '''
        props = StepFunctionsTPSTokenBucketProps(
            token_limit=token_limit,
            sqs_queue=sqs_queue,
            token_bucket_ddb_table_id=token_bucket_ddb_table_id,
            token_bucket_ddb_table_name=token_bucket_ddb_table_name,
        )

        jsii.create(self.__class__, self, [parent, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[aws_cdk.aws_stepfunctions.INextable]:
        '''The states to chain onto if this fragment is used.'''
        return typing.cast(typing.List[aws_cdk.aws_stepfunctions.INextable], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> aws_cdk.aws_stepfunctions.State:
        '''The start state of this state machine fragment.'''
        return typing.cast(aws_cdk.aws_stepfunctions.State, jsii.get(self, "startState"))


@jsii.data_type(
    jsii_type="schadem-cdk-construct-sfn-token-bucket.StepFunctionsTPSTokenBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "token_limit": "tokenLimit",
        "sqs_queue": "sqsQueue",
        "token_bucket_ddb_table_id": "tokenBucketDDBTableID",
        "token_bucket_ddb_table_name": "tokenBucketDDBTableName",
    },
)
class StepFunctionsTPSTokenBucketProps:
    def __init__(
        self,
        *,
        token_limit: jsii.Number,
        sqs_queue: typing.Optional[aws_cdk.aws_sqs.IQueue] = None,
        token_bucket_ddb_table_id: typing.Optional[builtins.str] = None,
        token_bucket_ddb_table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token_limit: 
        :param sqs_queue: queue to use for the task token requests - allows for distribution of tokens across different workflows. Queue and DDB table should obviously be the same if spreading
        :param token_bucket_ddb_table_id: 
        :param token_bucket_ddb_table_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "token_limit": token_limit,
        }
        if sqs_queue is not None:
            self._values["sqs_queue"] = sqs_queue
        if token_bucket_ddb_table_id is not None:
            self._values["token_bucket_ddb_table_id"] = token_bucket_ddb_table_id
        if token_bucket_ddb_table_name is not None:
            self._values["token_bucket_ddb_table_name"] = token_bucket_ddb_table_name

    @builtins.property
    def token_limit(self) -> jsii.Number:
        result = self._values.get("token_limit")
        assert result is not None, "Required property 'token_limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sqs_queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        '''queue to use for the task token requests - allows for distribution of tokens across different workflows.

        Queue and DDB table should obviously be the same if spreading
        '''
        result = self._values.get("sqs_queue")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.IQueue], result)

    @builtins.property
    def token_bucket_ddb_table_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token_bucket_ddb_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_bucket_ddb_table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token_bucket_ddb_table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepFunctionsTPSTokenBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StepFunctionsTPSTokenBucket",
    "StepFunctionsTPSTokenBucketProps",
]

publication.publish()
