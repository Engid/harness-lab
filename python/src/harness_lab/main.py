"""Rung 1: load a text file, ask Jev a few questions about it, print the answers.

Run from the python/ folder:

    uv run --env-file .env harness-lab data/sample.txt
"""

import sys
from pathlib import Path

from typesafe_sdk import (
    Choice,
    ChoiceAnswer,
    Noul,
    NoulAnswer,
    Score,
    ScoreAnswer,
    SystemOneResponse,
    TypeSafeClient,
    TypeSafeError,
)

# The questions we ask about every file. The names on the left are ours; the response uses the
# same names for the answers.
QUESTIONS = {
    # Noul: a yes/no question, answered with the probability of "yes".
    "asks_for_action": Noul(instructions="Does this text ask the reader to do something?"),
    # Choice: pick one label; the answer has a probability for every label.
    "tone": Choice(
        instructions="What is the tone of this text?",
        criteria={
            "positive": "Friendly, pleased or enthusiastic",
            "neutral": "Plain and matter-of-fact",
            "negative": "Upset, frustrated or hostile",
        },
    ),
    # Score: rate on ordered levels (0, 1, 2, ...); the answer is the expected level.
    "urgency": Score(
        instructions="How urgent is this text?",
        criteria=["Can wait", "Needs attention this week", "Needs attention today"],
    ),
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ask_jev(text: str) -> SystemOneResponse:
    # TypeSafeClient reads the key from the TYPESAFE_API_KEY environment variable.
    with TypeSafeClient() as client:
        return client.system_one(state={"text": text}, questions=QUESTIONS)


def print_answers(response: SystemOneResponse) -> None:
    print(f"model: {response.model}")
    
    for name, answer in response.answers.items():
        match answer:
            case NoulAnswer(noul=p):
                print(f"{name}: yes with probability {p:.2f}")

            case ChoiceAnswer(choice=choice, confidence=confidence, probabilities=probs):
                spread = ", ".join(f"{label} {p:.2f}" for label, p in probs.items())
                print(f"{name}: {choice} (confidence {confidence:.2f}; {spread})")

            case ScoreAnswer(score=score, confidence=confidence, legend=legend):
                nearest = legend[round(score)]
                print(f"{name}: {score:.2f} ~ {nearest!r} (confidence {confidence:.2f})")

    usage = response.usage
    print(f"tokens: {usage.input_tokens} in, {usage.output_tokens} out")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: harness-lab <file>")
    path = Path(sys.argv[1])
    if not path.is_file():
        sys.exit(f"not a file: {path}")

    text = load_text(path)
    try:
        response = ask_jev(text)
    except TypeSafeError as err:
        sys.exit(f"Jev call failed: {err}")
    print_answers(response)


if __name__ == "__main__":
    main()
