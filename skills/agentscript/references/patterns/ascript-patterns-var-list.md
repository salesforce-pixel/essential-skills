# Agent Script Pattern: Using List Variables

With list variables (also called collection variables), your agent can store and iterate over a collection of values. For example, you can create a list of questions that an interview agent must ask, or a list of objects to store an action's output. A list can store any supported type such as strings, booleans, numbers, or objects.

You can use a list item anywhere you use a regular variable. To reference an item in your list, use `[<item_numer>]`. List indexes start at 0, so the first item in your list is `@variables.YourVariable[0]`.

```sfdocs-code {"lang":"agentscript", "title": "Reference the THIRD item in the YourVariable list"}
@variables.YourVariable[2]
```

## Why Use This Pattern

Use list variables for:

- **Working through a sequence of items** one at a time, such as interview questions, checklist items, or search results.
- **Storing multiple outputs from an action**, such as a list of account records.
- **Tracking progress** through a collection by pairing a list with an index variable.

## Declare a List Variable

Declare a list variable in the `variables` block. Specify the list type in brackets `[]`. You can initialize an empty list with `=[]`, or set default values.

## Declare List Variables

```sfdocs-code {"lang":"agentscript", "title": "Declare List Variables"}
variables:
    # Declare a list of objects
    CandidateList: mutable list[object] = []
        description: "List of contacts returned from an action"
    CompetencyQuestions: mutable list[string] = ["Tell me about a time you disagreed with a coworker.", "Tell me about one of your favorite shifts.", "What are the most important qualities in a candidate?"]
        description: "List of questions to determine competency."
```

## Use a List Item in Reasoning Instructions

In this example, if question 3 is "Tell me about your work history", the prompt sent to the LLM is "Ask the candidate this question: Tell me about your work history".

```sfdocs-code {"lang":"agentscript", "title": "Ask the FIRST Question in Your List"}
    reasoning:
        instructions: ->
            |Ask the candidate this question: {!@variables.CompetencyQuestions[0]}
```

## Reference a List Item with a Variable

You can use a variable to reference a list item.

```sfdocs-code {"lang":"agentscript", "title": "Access a List Item by Index"}
reasoning:
    instructions: ->
        | Ask this question: {!@variables.questions[@variables.current_question]}
```

## Use a List Item in Reasoning Logic

You can use a list item in conditional expressions.

```sfdocs-code {"lang":"agentscript", "title": "End the Interview if the THIRD Answer is Wrong"}
# In the variables section, define a list of booleans
variables:
    areAnswersCorrect: mutable list[boolean]
        description: "True if the answer is correct, otherwise False"
....
# Later, as the user answers questions, record whether the answer was correct (not shown)
...

#  In a topic, if the THIRD answer is incorrect, end the interview
    reasoning:
        instructions: ->
            # remember that lists are zero-indexed ;-)
            if @variables.areAnswersCorrect[2] == "False":
                transition to @topic.end_interview
```

## Get the Length of a List

Use `len(@variables.MyList)` to get the number of items in a list. You can use `len(@variables.MyList)` in prompts, `available when` filters, and conditional expressions.

```sfdocs-code {"lang":"agentscript", "title": "Get the Length of a List"}
# For example, the agent might say "this is question 5 of 7"
reasoning:
    instructions: ->
        | This is question {!@variables.question_index + 1} of {!len(@variables.questions)}.
```

## Iterate Through a List

Agent Script doesn't have a `for` loop. Instead, iterate by incrementing the index variable after each turn.

This example asks each question in a list one at a time. After the agent records an answer, the index advances. When the index reaches the list length, the agent transitions to the next topic.

```sfdocs-code {"lang":"agentscript", "title": "Iterate Through a List"}
variables:
    questions: mutable list[object] = []
        description: "Questions to ask the candidate"
    question_index: mutable number = 0
        description: "Current index in the questions list"
    is_GetQuestions_run: mutable boolean = False
        description: "Whether the action Get_Questions has been run"

topic ask_questions:
    description: "Ask the candidate questions one at a time."

    reasoning:
        instructions: ->
            if @variables.is_GetQuestions_run == False:
                run @actions.Get_Questions
                    with JobScreeningRecordId=@variables.JobRecordID
                    set @variables.questions = @outputs.AllScreeningQuestions
                    set @variables.question_index = 0
                    set @variables.is_GetQuestions_run = True
            | Ask this question: {!@variables.questions[@variables.question_index]}
```

## Tips

- **Pair a list with an index variable** when you need to work through items one at a time.

## Related Topics

- Reference: [Variables](../reference/ascript-ref-variables.md)
