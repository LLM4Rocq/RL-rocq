import dataclasses
from data import TheoremData
from openai.types.chat import ChatCompletionMessageParam as Message

SYSTEM_PROMPT = """
Respond in the following format:
<think>
...
</think>
<proof>
...
</proof>
"""

USER_PROMPT = """
You are in the middle of the proof of {name}:

<code>
{code}
</code>

Ready? Here is the current goal:
<goal>
{goal}
</goal>

Write the whole proof of the theorem.
"""

def make_prompt(data: TheoremData) -> list[Message]:
    """ Make a prompt from theorem information. """
    return [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': USER_PROMPT.format(**dataclasses.asdict(data))}
    ]

def extract_name(prompt: str) -> str:
    """ Extract the name of the theorem from the user prompt. """
    prompt_beginning = prompt.split(":", maxsplit=1)[0]
    name = prompt_beginning.rsplit(" ", 1)[1]
    return name.strip()

def extract_code(prompt: str) -> str:
    """ Extract the theorem code from the user prompt. """
    prompt_end = prompt.split("<code>", maxsplit=1)[1]
    code = prompt_end.split("</code>", maxsplit=1)[0]
    return code.strip()

def extract_goal(prompt: str) -> str:
    """ Extract the goal of the theorem from the user prompt. """
    prompt_end = prompt.split("<goal>", maxsplit=1)[1]
    goal = prompt_end.split("</goal>", maxsplit=1)[0]
    return goal.strip()

def extract_data(prompt: str) -> TheoremData:
    """ Extract the theorem information from the user prompt. """
    return TheoremData(
        name = extract_name(prompt),
        code = extract_code(prompt),
        goal = extract_goal(prompt)
    )
