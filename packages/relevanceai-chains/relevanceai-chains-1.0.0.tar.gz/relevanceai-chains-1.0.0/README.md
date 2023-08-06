# Relevance AI

# A simple chain
## 1. Install and login
Install:
```
pip install relevanceai
```
Log in and create a project and api key:
```
import relevanceai as rai
rai.login()
```
or if you are in an automated environment, set these environment variables:
```
RELEVANCE_API_KEY=XXXX
```

## 2. Getting started
```
chain = rai.create(
    name = "My chain",
    description = "The greatest chain"
)
```

## 3. Add steps to the chain
Create a step for the chain
```
step = PromptCompletion(
    prompt="Hello world",
)
```
You can run and test the individual step.
```
step.run()
```
Once you are comfortable with the step you can add it by
```
chain.add(step)
```

## 4. Run and test the chain
Run the chain
```
chain.run()
```

## 5. Configuring output
By default it'll return the full state and all outputs from each step. You can control it by:
```
chain.set_output(["answer"])
```

# A chain with flexible inputs
## 1. Give your chain flexible inputs
Add input parameters
```
chain = rai.create(
    name = "My chain",
    description = "The greatest chain"
    parameters = {
        "name" : {"type" : "string"}
    }
)
```

## 2. Define the parameters inside a step
```
step = PromptCompletion(
    prompt="Hello world my name is ${name}",
)
```