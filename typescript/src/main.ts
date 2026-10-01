/**
 * Rung 1: load a text file, ask Jev a few questions about it, print the answers.
 *
 * Run from the typescript/ folder:
 *
 *     bun run src/main.ts data/sample.txt
 */

import { choice, noul, score, TypeSafeClient, TypeSafeError } from "@typesafe-ai/sdk";

// The questions we ask about every file. The names on the left are ours; the response uses the
// same names for the answers, and their types are inferred from these definitions.
const QUESTIONS = {
  // Noul: a yes/no question, answered with the probability of "yes".
  asks_for_action: noul("Does this text ask the reader to do something?"),
  // Choice: pick one label; the answer has a probability for every label.
  tone: choice("What is the tone of this text?", {
    positive: "Friendly, pleased or enthusiastic",
    neutral: "Plain and matter-of-fact",
    negative: "Upset, frustrated or hostile",
  }),
  // Score: rate on ordered levels (0, 1, 2, ...); the answer is the expected level.
  urgency: score("How urgent is this text?", [
    "Can wait",
    "Needs attention this week",
    "Needs attention today",
  ]),
};

async function loadText(path: string): Promise<string> {
  return Bun.file(path).text();
}

async function askJev(text: string) {
  // TypeSafeClient reads the key from the TYPESAFE_API_KEY environment variable.
  const client = new TypeSafeClient();
  return client.systemOne({ state: { text }, questions: QUESTIONS });
}

type Response = Awaited<ReturnType<typeof askJev>>;

function printAnswers(response: Response): void {
  console.log(`model: ${response.model}`);
  for (const [name, answer] of Object.entries(response.answers)) {
    switch (answer.type) {
      case "noul":
        console.log(`${name}: yes with probability ${answer.noul.toFixed(2)}`);
        break;
      case "choice": {
        const spread = Object.entries(answer.probabilities)
          .map(([label, p]) => `${label} ${p.toFixed(2)}`)
          .join(", ");
        console.log(`${name}: ${answer.choice} (confidence ${answer.confidence.toFixed(2)}; ${spread})`);
        break;
      }
      case "score": {
        const legend: Record<string, unknown> = answer.legend;
        const nearest = legend[String(Math.round(answer.score))];
        console.log(
          `${name}: ${answer.score.toFixed(2)} ~ ${JSON.stringify(nearest)} (confidence ${answer.confidence.toFixed(2)})`,
        );
        break;
      }
    }
  }
  const { input_tokens, output_tokens } = response.usage;
  console.log(`tokens: ${input_tokens} in, ${output_tokens} out`);
}

async function main(): Promise<void> {
  const args = Bun.argv.slice(2); // argv[0] is bun, argv[1] is this script
  if (args.length !== 1) {
    console.error("usage: bun run src/main.ts <file>");
    process.exit(1);
  }
  const path = args[0]!;
  if (!(await Bun.file(path).exists())) {
    console.error(`not a file: ${path}`);
    process.exit(1);
  }

  const text = await loadText(path);
  try {
    printAnswers(await askJev(text));
  } catch (err) {
    if (err instanceof TypeSafeError) {
      console.error(`Jev call failed: ${err.message}`);
      process.exit(1);
    }
    throw err;
  }
}

await main();
