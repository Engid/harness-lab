# Plan

harness-lab is a homemade agent harness built on [Jev](https://typesafe.ai), TypeSafe's System
One model, as a way to learn how harnesses work by building one.

## The method: continuous upgrade

From Henrik Kniberg's skateboard → scooter → bicycle → car picture
([Making sense of MVP](https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp)):
don't build car parts that only work once the car is finished. Build something that gets you
somewhere at every step, then upgrade it.

- **Every rung runs.** Each one ends with something usable from the terminal, and a commit.
- **Rough is fine.** This is learning code. Plain functions, no framework, until a rung needs one.
- **Architecture comes last.** Refactor once the shape of the loop is known from using it.
- **Small chunks.** A little during the week, mostly weekends.
- **Two languages.** Python ([python/](python/)) and TypeScript on [Bun](https://bun.sh)
  (`typescript/`, not started). Any rung can be done in either, or both, to compare.

## The ladder

### 1. Rollerblades: one Jev call

- [ ] Set up the SDK and API key
- [ ] Ask one Jev question about some data; pick something interesting to verify
- [ ] Print the answer and its probability

Learn: the SDK, latency, what a reading looks like.

### 2. Skateboard: more questions, more data

- [ ] Several questions (a Noul, a Choice, a Score) over a batch of items
- [ ] Save every answer to a file (e.g. JSONL), with latency per call
- [ ] Reword a question and compare the results

Learn: scoring many items; how much wording matters. A labeled dataset such as the
[SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) makes answers
easy to check.

### 3. Scooter: act on the answers

- [ ] Do something with the results: have an LLM write a summary of the decisions, write a
      report file, or send an email

Learn: readings driving a next step; the first LLM call.

### 4. Kick bike: a chat REPL

- [ ] A terminal chat loop wired to an LLM API
- [ ] Conversation history kept in memory

Learn: the LLM SDK, streaming or not, the shape of a turn.

### 5. Bicycle: Jev in the loop

- [ ] Each message gets a Jev check before the LLM sees it
- [ ] Show the reading as a trace line
- [ ] Code picks what happens from the reading: reply, ask to clarify, or refuse

Learn: the core loop of a Jev harness: Jev decides, code routes, the LLM generates.

### 6. Cargo bike: remember things

- [ ] Save turns and readings to SQLite
- [ ] Resume a session after restarting

Learn: an append-only log as the harness's memory. (Could come earlier.)

### 7. Moped: one tool

- [ ] One read-only tool: `read_file`
- [ ] The tool loop: model → tool call → result → model, until it answers

Learn: what actually makes it a harness.

### 8. Small car: more tools, with Jev as a gate

- [ ] `search`, then `write` with a confirmation step
- [ ] A Jev check before a request goes to the LLM
- [ ] A Jev check on tool calls before they run

Learn: Jev as a gate and a verifier.

### 9. Tune-up: refactor

- [ ] Re-architect around what the loop turned out to need: a pure `decide` step that turns
      inputs into events, an `apply` step that updates state, and a driver that runs commands
- [ ] Add structure (retries, timeouts, maybe Effect in TypeScript) only where it hurts

Learn: architecture grounded in something that works.

## Side road (optional)

After rung 3, a detour into data classification:

- [ ] Sweep thresholds over saved answers, no new Jev calls: how many items pass, and how many of
      those are right against the labels
- [ ] A small web page with a slider per question, re-sorting saved answers live
- [ ] Click an item to see why it landed where it did
