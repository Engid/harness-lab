# harness-lab (TypeScript)

## Setup

Needs [Bun](https://bun.sh).

```sh
cd typescript
bun install
cp .env.example .env              # then add your TYPESAFE_API_KEY
bun run src/main.ts data/sample.txt
bun run typecheck
```

Bun reads `.env` on its own, so there's no `--env-file` flag.
