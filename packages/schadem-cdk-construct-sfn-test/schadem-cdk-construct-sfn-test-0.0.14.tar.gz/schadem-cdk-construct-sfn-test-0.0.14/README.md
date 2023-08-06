TL;DR:

This Construct allows calling Amazon Textract as part of a AWS Step Function Workflow.
Still work-in-process, so interfaces may (most likely will) change.
But a good starting point imho and happy to hear feedback.

Build using [https://projen.io/](projen) - GitHub at: [https://github.com/projen/projen](GitHub-projen)

# Usage

Atm deployed as NPM package for use in TypeScript and as a PyPI package for use in Python based CDK stacks.

The Step Function flow expects a message with information about the location of the file to process:

```javascript
{
  "s3_bucket": "<somebucket>",
  "s3_key": "someprefix/someobject.somesuffix"
}
```

The object can either be a supported document type (PDF, PNG, JPEG, TIFF) for the default flow, which calls the [https://docs.aws.amazon.com/textract/latest/dg/API_Operations.html] (DetectDocumentText) for single page or [https://docs.aws.amazon.com/textract/latest/dg/API_Operations.html](StartDocumentTextDetection) for multi page documents.

The output is in the following format

```javascript
{
  "TextractOutputJsonPath": "s3://somebucket/someoutputprefix/randomuuid/inputfilename.json"
}
```

and includes the full JSON returned from Textract. It already combines paginated results into one JSON file.

To call other functionality like the Forms, Tables, Queries, AnalyzeID or AnalyzeExpense there are 2 ways:

1. Pass in "EXPENSE" or "IDENTITY" as the defaultClassification when creating the TextractStepFunctionsStartExecution, which will then change the default from the Detect API to the Expense or Identity one.
2. Upload a manifest file

The format of the manifest file is defined as:

```javascript
{
    "S3Path": "s3://sdx-textract-us-east-1/employeeapp20210510.png",
    "TextractFeatures": [
        "FORMS",
        "TABLES",
        "QUERIES"
    ],
    "QueriesConfig": [{
        "Text": "What is the applicant full name?",
        "Alias": "FULL_NAME",
        "Pages": ["*"]
    }],
    "Classification":"SOMECLASSIFICATION"
}
```

for the AnalyzeDocument API at least one TextractFeature and the S3Path is required.
To execute the Expense API the Classification has to be set to "EXPENSE".

For the Identity API the following format is required:

```javascript
{
    "DocumentPages": ["s3://sdx-textract-us-east-1/driverlicense.png"],
    "Classification":"IDENTITY"
}
```

For Identity, 2 document pages can be passed in.

## TypeScript sample

sample GitHub project that uses the Textract Construct: https://github.com/schadem/schadem-cdk-stack-test

To use, add as dependency

```json
  "dependencies": {
    "schadem-cdk-construct-sfn-test": "0.0.12"
  },
```

```javascript
const textract_task = new tstep.TextractStepFunctionsStartExecution(this, 'textract-task', {
    s3OutputBucket: documentBucket.bucketName,
    s3OutputPrefix: textractS3OutputPrefix,
    s3TempOutputPrefix: textractTemporaryS3OutputPrefix,
});
const workflow_chain = sfn.Chain.start(textract_task)
const stateMachine = new sfn.StateMachine(this, 'IDPWorkflow', {
    definition: workflow_chain,
    timeout: Duration.minutes(240),
});
```

## Python sample

sample GitHub project with Stack that uses the Textract Construct: https://github.com/schadem/schadem-cdk-idp-stack-python-sample

package name: schadem-cdk-construct-sfn-test

```python
textract_task = sfctc.TextractStepFunctionsStartExecution(
    self,
    "textract-task",
    s3_output_bucket=document_bucket.bucket_name,
    s3_temp_output_prefix=s3_temp_prefix,
    s3_output_prefix=s3_output_prefix)
workflow_chain = sfn.Chain.start(textract_task)

state_machine = sfn.StateMachine(self,
                                'IDPWorkflowPython',
                                definition=workflow_chain)
```

The Construct implements the sfn.TaskStateBase similar to the StepFunctionsStartExecution and therefore is used as a part of a Step Function workflow. See the stack for a usage sample.

# Development

At the moment essentially just do

```
npx projen build
```

to generate the packages.

When pushing/merging to mainline branch onto GitHub it kicks off a pipeline which increases the version number and deploys the packages to PyPI and NPM atm (nugen and maven can be added).

That package I reference in a script in the stack (install_construct_and_deploy.s) - which atm has hardcoded references to locations of the packages on my local system.
Obviously that will change when we push the packages out
