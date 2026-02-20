# Agent Instructions

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**
- SOPs in `directives/`
- Define goals, inputs, tools/scripts, outputs, edge cases

**Layer 2: Orchestration (Decision making)**
- This is you. Read directives, call execution tools, handle errors, update directives

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Use `.env` for secrets

## Operating Principles

1. Check for tools first
2. Self-anneal when things break
3. Update directives as you learn

## Self-annealing loop
1. Fix it
2. Update the tool
3. Test tool
4. Update directive
5. System is now stronger

## File Organization
- `.tmp/` - Intermediates
- `execution/` - Python scripts
- `directives/` - SOPs
- `.env` - Environment variables

## Cloud Webhooks (Modal)
- See `directives/add_webhook.md` for setup

## Summary
You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, continuously improve the system.
