# integ-tests

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Usage

Suppose you have a simple stack, that only encapsulates a Lambda function with a
certain handler:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )
```

You may want to test this stack under different conditions. For example, we want
this stack to be deployed correctly, regardless of the architecture we choose
for the Lambda function. In particular, it should work for both `ARM_64` and
`X86_64`. So you can create an `IntegTestCase` that exercises both scenarios:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )

# Beginning of the test suite
app = App()

stack = Stack(app, "stack")

different_archs_case = IntegTestCase(stack, "DifferentArchitectures",
    stacks=[
        StackUnderTest(app, "Stack1",
            architecture=lambda_.Architecture.ARM_64
        ),
        StackUnderTest(app, "Stack2",
            architecture=lambda_.Architecture.X86_64
        )
    ]
)

# There must be exactly one instance of TestCase per file
IntegTest(app, "integ-test",

    # Register as many test cases as you want here
    test_cases=[different_archs_case]
)
```

This is all the instruction you need for the integration test runner to know
which stacks to synthesize, deploy and destroy. But you may also need to
customize the behavior of the runner by changing its parameters. For example:

```python
app = App()

stack_under_test = Stack(app, "StackUnderTest")

stack = Stack(app, "stack")

test_case = IntegTestCase(stack, "CustomizedDeploymentWorkflow",
    stacks=[stack_under_test],
    diff_assets=True,
    stack_update_workflow=True,
    cdk_command_options=CdkCommands(
        deploy=DeployCommand(
            args=DeployOptions(
                require_approval=RequireApproval.NEVER,
                json=True
            )
        ),
        destroy=DestroyCommand(
            args=DestroyOptions(
                force=True
            )
        )
    )
)

IntegTest(app, "integ-test",
    test_cases=[test_case]
)
```
