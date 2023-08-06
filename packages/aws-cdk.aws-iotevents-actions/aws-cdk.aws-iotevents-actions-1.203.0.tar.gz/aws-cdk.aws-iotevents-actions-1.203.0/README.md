# Actions for AWS::IoTEvents Detector Model

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library contains integration classes to specify actions of state events of Detector Model in `@aws-cdk/aws-iotevents`.
Instances of these classes should be passed to `State` defined in `@aws-cdk/aws-iotevents`
You can define built-in actions to use a timer or set a variable, or send data to other AWS resources.

This library contains integration classes to use a timer or set a variable, or send data to other AWS resources.
AWS IoT Events can trigger actions when it detects a specified event or transition event.

Currently supported are:

* Set variable to detector instanse
* Invoke a Lambda function

## Set variable to detector instanse

The code snippet below creates an Action that set variable to detector instanse
when it is triggered.

```python
# Example automatically generated from non-compiling source. May contain errors.
import aws_cdk.aws_iotevents as iotevents
import aws_cdk.aws_iotevents_actions as actions

# input: iotevents.IInput

state = iotevents.State(
    state_name="MyState",
    on_enter=[iotevents.Event(
        event_name="test-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions, [
            actions.SetVariableAction("MyVariable",
                iotevents.Expression.input_attribute(input, "payload.temperature"))
        ]
        ]
    )]
)
```

## Invoke a Lambda function

The code snippet below creates an Action that invoke a Lambda function
when it is triggered.

```python
import aws_cdk.aws_iotevents as iotevents
import aws_cdk.aws_iotevents_actions as actions
import aws_cdk.aws_lambda as lambda_

# input: iotevents.IInput
# func: lambda.IFunction

state = iotevents.State(
    state_name="MyState",
    on_enter=[iotevents.Event(
        event_name="test-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions.LambdaInvokeAction(func)]
    )]
)
```
