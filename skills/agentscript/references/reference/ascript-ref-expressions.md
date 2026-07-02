# Agent Script Reference: Conditional Expressions

`if` and `else` conditions deterministically specify what actions to take or which prompts to include. To specify complex conditions, use parentheses `()` to group `and` and `or` operators within a condition.

For example, you can check a variable's value and then run an action based on the result:

```sfdocs-code {"lang":"agentscript", "title": "Example: Conditionally Run an Action"}
# If the tracking number (represented as a string) isn't empty and is not None, get the tracking updates
if @variables.tracking_number is not None and @variables.tracking_number != "":
    run @actions.Get_Tracking_Updates
else:
    run @actions.Ask_Tracking_Number
```

If you need to nest `and` and `or`operators, you can use parentheses `()`. In this example, the grouped condition `(@variables.HasSalesInterest == True or @variables.WantsMeeting == True)` is evaluated first. The condition evaluates as true if either one of `HasSalesInterest` or `WantsMeeting` is true.

```sfdocs-code {"lang":"agentscript", "title": "Example: Use Grouped Operators to Determine When a Subagent is Available"}
    reasoning:
        instructions: ->
            | Select the best tool to call based on conversation history and user's intent.
        actions:
            go_to_Qualify: @utils.transition to @subagent.Qualify
                available when @variables.customerType == "Valued" and @variables.QualificationEnabled == True and (@variables.HasSalesInterest == True or @variables.WantsMeeting == True) and @variables.QualificationFlowStep != "COMPLETE"
```

You can also check a variable in order to set other variables.

```sfdocs-code {"lang":"agentscript", "title": "Example: Conditionally Set a Variable"}
if @variables.order_number == "" and @variables.customer_email == "":
    set @variables.order_found = False
    set @variables.customer_verified = False
```

You can use a conditional expression to determine which natural-language prompt to include.

```sfdocs-code {"lang":"agentscript", "title": "Example: Conditionally Add a Prompt"}
if @variables.is_late == True:
    | Apologize to the customer for the delay in receiving their order.
else:
    | Tell the customer their order is arriving as scheduled.
```

You can use `if` and `else` inside reasoning instructions to conditionally include different prompt lines for the LLM.

```sfdocs-code {"lang":"agentscript", "title": "Example: if/else Inside Reasoning Instructions"}
reasoning:
    instructions: ->
        | Your job is solely to help with issues and answer questions by searching knowledge articles.
        if @variables.support_tier == "premium":
            | This is a premium customer. Prioritize their request and offer proactive suggestions.
        else:
            | This is a standard customer. Answer their questions helpfully and suggest upgrading for faster support.
        | If the customer's question is too vague, ask for more details.
```

You can check whether a variable has a value.

```sfdocs-code {"lang":"agentscript", "title": "Check Whether a Variable Has a Value"}
# Note this example demonstrates correct syntax, NOT how to design a production agent
reasoning:
    instructions: ->
      if @variables.account_id is None:
        | What's the account ID for this order?
      if @variables.is_premium_user is not None:
        | This customer's premium status is set to {!@variables.is_premium_user}.
      if @variables.order_lines != None:
        | Order lines on this order: {!@variables.order_lines}.
      if @variables.scheduled_date is None:
        | When would you like to schedule this appointment?
```

:::note
Currently, Agent Script supports `if` and `else` logic, but it doesn't support `else if` logic after an `if` statement.
:::

**Related Topics**

- [Reasoning Instructions](ascript-ref-instructions.md)
- [Supported Operators](ascript-ref-operators.md)
