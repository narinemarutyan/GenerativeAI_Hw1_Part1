# Objective 

This AI assistant answers "What's the temperature outside now" or "What's the temperature in Tokio now" type 
of questions (location can be any big city). It asks for the location of the user if the location is not in the 
question.


## Set up
- Clone the repository
- Install the requirements with this command
- put the .env file in src directory. The .env should contain openai key and model.

```bash
poetry install
```

## How to use it

```bash
chainlit run src/chainlit.py -w
```

