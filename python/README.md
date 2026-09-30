# harness-lab (Python)

## Setup

Needs [uv](https://docs.astral.sh/uv/).

```sh
cd python
uv sync
cp .env.example .env        # then add your TYPESAFE_API_KEY
uv run --env-file .env pytest
uv run ruff check .        # lint
uv run ruff format .       # format
uv run ty check            # type-check
```

## Layout

```
src/harness_lab/   the package
tests/             pytest
```
