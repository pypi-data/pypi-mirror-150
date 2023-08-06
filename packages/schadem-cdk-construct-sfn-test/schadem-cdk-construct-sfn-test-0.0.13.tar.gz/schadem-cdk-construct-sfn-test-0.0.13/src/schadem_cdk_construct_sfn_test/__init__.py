'''
TL;DR:

This Construct hides the complexity of calling Textract.

Build using [https://projen.io/](projen) - GitHub at: [https://github.com/projen/projen](GitHub-projen)

# Usage

Lambda functions are in Python encapsulated as Docker Containers. Picked containers as they are more generic across platforms and when using binary dependencies don't fail on different OS (Windows, MacOS)

The Construct implements the sfn.TaskStateBase similar to the StepFunctionsStartExecution and therefore is used as a part of a Step Function workflow. See the stack for a usage sample.

# Deployment

At the moment essentially just do

```
npx projen build
```

to generate the packages.

When pushing/merging to mainline branch onto GitHub it kicks off a pipeline which increases the version number and deploys the packages to PyPI and NPM atm (nugen and maven can be added).

That package I reference in a script in the stack (install_construct_and_deploy.s) - which atm has hardcoded references to locations of the packages on my local system.
Obviously that will change when we push the packages out
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

import aws_cdk
import aws_cdk.aws_iam
import aws_cdk.aws_stepfunctions
import aws_cdk.aws_stepfunctions_tasks
import constructs


class TextractStepFunctionsStartExecution(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="schadem-cdk-construct-sfn-test.TextractStepFunctionsStartExecution",
):
    '''A Step Functions Task to call Textract. Requires.

    It supports three service integration patterns: REQUEST_RESPONSE, RUN_JOB, and WAIT_FOR_TASK_TOKEN.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        s3_output_bucket: builtins.str,
        s3_output_prefix: builtins.str,
        s3_temp_output_prefix: builtins.str,
        associate_with_parent: typing.Optional[builtins.bool] = None,
        concurrency_table_name: typing.Optional[builtins.str] = None,
        custom_function: typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke] = None,
        default_classification: typing.Optional[builtins.str] = None,
        enable_dashboard: typing.Optional[builtins.bool] = None,
        enable_monitoring: typing.Optional[builtins.bool] = None,
        input: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        lambda_log_level: typing.Optional[builtins.str] = None,
        max_concurrency_table_name: typing.Optional[builtins.str] = None,
        max_number_open_jobs: typing.Optional[jsii.Number] = None,
        max_tps_analyze_document_api_calls: typing.Optional[jsii.Number] = None,
        max_tps_analyze_expense: typing.Optional[jsii.Number] = None,
        max_tps_analyze_id: typing.Optional[jsii.Number] = None,
        max_tps_document_text_api_calls: typing.Optional[jsii.Number] = None,
        max_tps_start_analyze_document_api_calls: typing.Optional[jsii.Number] = None,
        max_tps_start_document_text_api_calls: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        task_token_table: typing.Optional[builtins.str] = None,
        workflow_timeout_duration_in_minutes: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        result_selector: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param s3_output_bucket: The prefix to use for the output files.
        :param s3_output_prefix: The prefix to use for the output files.
        :param s3_temp_output_prefix: The prefix to use for the temporary output files (e. g. output from async process before stiching together)
        :param associate_with_parent: Pass the execution ID from the context object to the execution input. This allows the Step Functions UI to link child executions from parent executions, making it easier to trace execution flow across state machines. If you set this property to ``true``, the ``input`` property must be an object (provided by ``sfn.TaskInput.fromObject``) or omitted entirely. Default: - false
        :param concurrency_table_name: taskToken table for async processing.
        :param custom_function: not implemented yet.
        :param default_classification: default classification, if a specific document types e. g. ID documents or expenses or invoices should be processed vs generic
        :param enable_dashboard: not implemented yet.
        :param enable_monitoring: not implemented yet.
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - The state input (JSON path '$')
        :param lambda_log_level: Log Level for all Lambda functions.
        :param max_concurrency_table_name: not implemented yet.
        :param max_number_open_jobs: not implemented yet.
        :param max_tps_analyze_document_api_calls: not implemented yet.
        :param max_tps_analyze_expense: not implemented yet.
        :param max_tps_analyze_id: not implemented yet.
        :param max_tps_document_text_api_calls: not implemented yet.
        :param max_tps_start_analyze_document_api_calls: not implemented yet.
        :param max_tps_start_document_text_api_calls: not implemented yet.
        :param name: The name of the execution, same as that of StartExecution. Default: - None
        :param task_token_table: taskToken table for async processing.
        :param workflow_timeout_duration_in_minutes: timeout for getting the results.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: - ``IntegrationPattern.REQUEST_RESPONSE`` for most tasks. ``IntegrationPattern.RUN_JOB`` for the following exceptions: ``BatchSubmitJob``, ``EmrAddStep``, ``EmrCreateCluster``, ``EmrTerminationCluster``, and ``EmrContainersStartJobRun``.
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param result_selector: The JSON that will replace the state's raw result and become the effective result before ResultPath is applied. You can use ResultSelector to create a payload with values that are static or selected from the state's raw result. Default: - None
        :param timeout: Timeout for the state machine. Default: - None
        '''
        props = TextractStepFunctionsStartExecutionProps(
            s3_output_bucket=s3_output_bucket,
            s3_output_prefix=s3_output_prefix,
            s3_temp_output_prefix=s3_temp_output_prefix,
            associate_with_parent=associate_with_parent,
            concurrency_table_name=concurrency_table_name,
            custom_function=custom_function,
            default_classification=default_classification,
            enable_dashboard=enable_dashboard,
            enable_monitoring=enable_monitoring,
            input=input,
            lambda_log_level=lambda_log_level,
            max_concurrency_table_name=max_concurrency_table_name,
            max_number_open_jobs=max_number_open_jobs,
            max_tps_analyze_document_api_calls=max_tps_analyze_document_api_calls,
            max_tps_analyze_expense=max_tps_analyze_expense,
            max_tps_analyze_id=max_tps_analyze_id,
            max_tps_document_text_api_calls=max_tps_document_text_api_calls,
            max_tps_start_analyze_document_api_calls=max_tps_start_analyze_document_api_calls,
            max_tps_start_document_text_api_calls=max_tps_start_document_text_api_calls,
            name=name,
            task_token_table=task_token_table,
            workflow_timeout_duration_in_minutes=workflow_timeout_duration_in_minutes,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            result_selector=result_selector,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig], jsii.get(self, "taskMetrics"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]], jsii.get(self, "taskPolicies"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachine")
    def state_machine(self) -> aws_cdk.aws_stepfunctions.StateMachine:
        return typing.cast(aws_cdk.aws_stepfunctions.StateMachine, jsii.get(self, "stateMachine"))

    @state_machine.setter
    def state_machine(self, value: aws_cdk.aws_stepfunctions.StateMachine) -> None:
        jsii.set(self, "stateMachine", value)


@jsii.data_type(
    jsii_type="schadem-cdk-construct-sfn-test.TextractStepFunctionsStartExecutionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "result_selector": "resultSelector",
        "timeout": "timeout",
        "s3_output_bucket": "s3OutputBucket",
        "s3_output_prefix": "s3OutputPrefix",
        "s3_temp_output_prefix": "s3TempOutputPrefix",
        "associate_with_parent": "associateWithParent",
        "concurrency_table_name": "concurrencyTableName",
        "custom_function": "customFunction",
        "default_classification": "defaultClassification",
        "enable_dashboard": "enableDashboard",
        "enable_monitoring": "enableMonitoring",
        "input": "input",
        "lambda_log_level": "lambdaLogLevel",
        "max_concurrency_table_name": "maxConcurrencyTableName",
        "max_number_open_jobs": "maxNumberOpenJobs",
        "max_tps_analyze_document_api_calls": "maxTPSAnalyzeDocumentAPICalls",
        "max_tps_analyze_expense": "maxTPSAnalyzeExpense",
        "max_tps_analyze_id": "maxTPSAnalyzeID",
        "max_tps_document_text_api_calls": "maxTPSDocumentTextAPICalls",
        "max_tps_start_analyze_document_api_calls": "maxTPSStartAnalyzeDocumentAPICalls",
        "max_tps_start_document_text_api_calls": "maxTPSStartDocumentTextAPICalls",
        "name": "name",
        "task_token_table": "taskTokenTable",
        "workflow_timeout_duration_in_minutes": "workflowTimeoutDurationInMinutes",
    },
)
class TextractStepFunctionsStartExecutionProps(
    aws_cdk.aws_stepfunctions.TaskStateBaseProps,
):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        result_selector: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        s3_output_bucket: builtins.str,
        s3_output_prefix: builtins.str,
        s3_temp_output_prefix: builtins.str,
        associate_with_parent: typing.Optional[builtins.bool] = None,
        concurrency_table_name: typing.Optional[builtins.str] = None,
        custom_function: typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke] = None,
        default_classification: typing.Optional[builtins.str] = None,
        enable_dashboard: typing.Optional[builtins.bool] = None,
        enable_monitoring: typing.Optional[builtins.bool] = None,
        input: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        lambda_log_level: typing.Optional[builtins.str] = None,
        max_concurrency_table_name: typing.Optional[builtins.str] = None,
        max_number_open_jobs: typing.Optional[jsii.Number] = None,
        max_tps_analyze_document_api_calls: typing.Optional[jsii.Number] = None,
        max_tps_analyze_expense: typing.Optional[jsii.Number] = None,
        max_tps_analyze_id: typing.Optional[jsii.Number] = None,
        max_tps_document_text_api_calls: typing.Optional[jsii.Number] = None,
        max_tps_start_analyze_document_api_calls: typing.Optional[jsii.Number] = None,
        max_tps_start_document_text_api_calls: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        task_token_table: typing.Optional[builtins.str] = None,
        workflow_timeout_duration_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for StartExecution.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: - ``IntegrationPattern.REQUEST_RESPONSE`` for most tasks. ``IntegrationPattern.RUN_JOB`` for the following exceptions: ``BatchSubmitJob``, ``EmrAddStep``, ``EmrCreateCluster``, ``EmrTerminationCluster``, and ``EmrContainersStartJobRun``.
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param result_selector: The JSON that will replace the state's raw result and become the effective result before ResultPath is applied. You can use ResultSelector to create a payload with values that are static or selected from the state's raw result. Default: - None
        :param timeout: Timeout for the state machine. Default: - None
        :param s3_output_bucket: The prefix to use for the output files.
        :param s3_output_prefix: The prefix to use for the output files.
        :param s3_temp_output_prefix: The prefix to use for the temporary output files (e. g. output from async process before stiching together)
        :param associate_with_parent: Pass the execution ID from the context object to the execution input. This allows the Step Functions UI to link child executions from parent executions, making it easier to trace execution flow across state machines. If you set this property to ``true``, the ``input`` property must be an object (provided by ``sfn.TaskInput.fromObject``) or omitted entirely. Default: - false
        :param concurrency_table_name: taskToken table for async processing.
        :param custom_function: not implemented yet.
        :param default_classification: default classification, if a specific document types e. g. ID documents or expenses or invoices should be processed vs generic
        :param enable_dashboard: not implemented yet.
        :param enable_monitoring: not implemented yet.
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - The state input (JSON path '$')
        :param lambda_log_level: Log Level for all Lambda functions.
        :param max_concurrency_table_name: not implemented yet.
        :param max_number_open_jobs: not implemented yet.
        :param max_tps_analyze_document_api_calls: not implemented yet.
        :param max_tps_analyze_expense: not implemented yet.
        :param max_tps_analyze_id: not implemented yet.
        :param max_tps_document_text_api_calls: not implemented yet.
        :param max_tps_start_analyze_document_api_calls: not implemented yet.
        :param max_tps_start_document_text_api_calls: not implemented yet.
        :param name: The name of the execution, same as that of StartExecution. Default: - None
        :param task_token_table: taskToken table for async processing.
        :param workflow_timeout_duration_in_minutes: timeout for getting the results.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "s3_output_bucket": s3_output_bucket,
            "s3_output_prefix": s3_output_prefix,
            "s3_temp_output_prefix": s3_temp_output_prefix,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if result_selector is not None:
            self._values["result_selector"] = result_selector
        if timeout is not None:
            self._values["timeout"] = timeout
        if associate_with_parent is not None:
            self._values["associate_with_parent"] = associate_with_parent
        if concurrency_table_name is not None:
            self._values["concurrency_table_name"] = concurrency_table_name
        if custom_function is not None:
            self._values["custom_function"] = custom_function
        if default_classification is not None:
            self._values["default_classification"] = default_classification
        if enable_dashboard is not None:
            self._values["enable_dashboard"] = enable_dashboard
        if enable_monitoring is not None:
            self._values["enable_monitoring"] = enable_monitoring
        if input is not None:
            self._values["input"] = input
        if lambda_log_level is not None:
            self._values["lambda_log_level"] = lambda_log_level
        if max_concurrency_table_name is not None:
            self._values["max_concurrency_table_name"] = max_concurrency_table_name
        if max_number_open_jobs is not None:
            self._values["max_number_open_jobs"] = max_number_open_jobs
        if max_tps_analyze_document_api_calls is not None:
            self._values["max_tps_analyze_document_api_calls"] = max_tps_analyze_document_api_calls
        if max_tps_analyze_expense is not None:
            self._values["max_tps_analyze_expense"] = max_tps_analyze_expense
        if max_tps_analyze_id is not None:
            self._values["max_tps_analyze_id"] = max_tps_analyze_id
        if max_tps_document_text_api_calls is not None:
            self._values["max_tps_document_text_api_calls"] = max_tps_document_text_api_calls
        if max_tps_start_analyze_document_api_calls is not None:
            self._values["max_tps_start_analyze_document_api_calls"] = max_tps_start_analyze_document_api_calls
        if max_tps_start_document_text_api_calls is not None:
            self._values["max_tps_start_document_text_api_calls"] = max_tps_start_document_text_api_calls
        if name is not None:
            self._values["name"] = name
        if task_token_table is not None:
            self._values["task_token_table"] = task_token_table
        if workflow_timeout_duration_in_minutes is not None:
            self._values["workflow_timeout_duration_in_minutes"] = workflow_timeout_duration_in_minutes

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''An optional description for this state.

        :default: - No comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.Duration]:
        '''Timeout for the heartbeat.

        :default: - None
        '''
        result = self._values.get("heartbeat")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        '''AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default:

        - ``IntegrationPattern.REQUEST_RESPONSE`` for most tasks.
        ``IntegrationPattern.RUN_JOB`` for the following exceptions:
        ``BatchSubmitJob``, ``EmrAddStep``, ``EmrCreateCluster``, ``EmrTerminationCluster``, and ``EmrContainersStartJobRun``.

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        '''
        result = self._values.get("integration_pattern")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''The JSON that will replace the state's raw result and become the effective result before ResultPath is applied.

        You can use ResultSelector to create a payload with values that are static
        or selected from the state's raw result.

        :default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-resultselector
        '''
        result = self._values.get("result_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''Timeout for the state machine.

        :default: - None
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def s3_output_bucket(self) -> builtins.str:
        '''The prefix to use for the output files.'''
        result = self._values.get("s3_output_bucket")
        assert result is not None, "Required property 's3_output_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_output_prefix(self) -> builtins.str:
        '''The prefix to use for the output files.'''
        result = self._values.get("s3_output_prefix")
        assert result is not None, "Required property 's3_output_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_temp_output_prefix(self) -> builtins.str:
        '''The prefix to use for the temporary output files (e.

        g. output from async process before stiching together)
        '''
        result = self._values.get("s3_temp_output_prefix")
        assert result is not None, "Required property 's3_temp_output_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associate_with_parent(self) -> typing.Optional[builtins.bool]:
        '''Pass the execution ID from the context object to the execution input.

        This allows the Step Functions UI to link child executions from parent executions, making it easier to trace execution flow across state machines.

        If you set this property to ``true``, the ``input`` property must be an object (provided by ``sfn.TaskInput.fromObject``) or omitted entirely.

        :default: - false

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html#nested-execution-startid
        '''
        result = self._values.get("associate_with_parent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def concurrency_table_name(self) -> typing.Optional[builtins.str]:
        '''taskToken table for async processing.'''
        result = self._values.get("concurrency_table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_function(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke]:
        '''not implemented yet.'''
        result = self._values.get("custom_function")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions_tasks.LambdaInvoke], result)

    @builtins.property
    def default_classification(self) -> typing.Optional[builtins.str]:
        '''default classification, if a specific document types e.

        g. ID documents or expenses or invoices should be processed vs generic
        '''
        result = self._values.get("default_classification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dashboard(self) -> typing.Optional[builtins.bool]:
        '''not implemented yet.'''
        result = self._values.get("enable_dashboard")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_monitoring(self) -> typing.Optional[builtins.bool]:
        '''not implemented yet.'''
        result = self._values.get("enable_monitoring")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def input(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        '''The JSON input for the execution, same as that of StartExecution.

        :default: - The state input (JSON path '$')

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[aws_cdk.aws_stepfunctions.TaskInput], result)

    @builtins.property
    def lambda_log_level(self) -> typing.Optional[builtins.str]:
        '''Log Level for all Lambda functions.'''
        result = self._values.get("lambda_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency_table_name(self) -> typing.Optional[builtins.str]:
        '''not implemented yet.'''
        result = self._values.get("max_concurrency_table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_number_open_jobs(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_number_open_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tps_analyze_document_api_calls(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_tps_analyze_document_api_calls")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tps_analyze_expense(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_tps_analyze_expense")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tps_analyze_id(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_tps_analyze_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tps_document_text_api_calls(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_tps_document_text_api_calls")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tps_start_analyze_document_api_calls(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_tps_start_analyze_document_api_calls")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tps_start_document_text_api_calls(self) -> typing.Optional[jsii.Number]:
        '''not implemented yet.'''
        result = self._values.get("max_tps_start_document_text_api_calls")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the execution, same as that of StartExecution.

        :default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_token_table(self) -> typing.Optional[builtins.str]:
        '''taskToken table for async processing.'''
        result = self._values.get("task_token_table")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_timeout_duration_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''timeout for getting the results.'''
        result = self._values.get("workflow_timeout_duration_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextractStepFunctionsStartExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TextractStepFunctionsStartExecution",
    "TextractStepFunctionsStartExecutionProps",
]

publication.publish()
