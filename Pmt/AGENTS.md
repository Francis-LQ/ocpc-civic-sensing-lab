# AGENTS.md

## Directory Role

`Pmt` stores reusable prompts, agent instructions, development prompts, and structured task templates.

## Working Rules

- Keep prompts executable: include role, context, input, output format, constraints, and acceptance criteria.
- Prefer versioned prompt files when meaningfully changing behavior.
- Avoid mixing final deliverables with scratch prompts; create clearly named drafts when needed.
- If a prompt is intended for Codex, include concrete file paths, module names, tests, and expected outputs.
