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
