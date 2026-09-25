# NEXENT Frontier Engineering Fabric

This slice turns the existing NEXENT research/engineering architecture into an executable boundary for three linked domains:

MATHEMATICAL MODEL -> COMPUTATIONAL MODEL -> PHYSICAL MODEL

and connects those domains to the explicit multi-mind reasoning protocol.

## Runtime boundary

CLIENT -> NEXENT HTTP API -> FRONTIER FABRIC -> {MULTI-MIND | MATH | PHYSICS} -> EVIDENCE/VERIFICATION HANDOFF

The HTTP server is localhost-first and dependency-free. It does not make governance decisions or silently mutate VAIXLNS.

## Model connection

The model layer is provider-agnostic at the fabric boundary and currently includes an OpenAI Responses adapter.

Environment:

- NEXENT_OPENAI_API_KEY (or OPENAI_API_KEY)
- NEXENT_OPENAI_MODEL (default gpt-5.6)
- NEXENT_REASONING_EFFORT (default high)
- NEXENT_ROLE_MODELS such as verification=gpt-5.6,domain=gpt-5.6

The default gpt-5.6 setting is an alias for the current OpenAI flagship family; the deployment can override it without code changes.

## Multi-mind protocol

The council defines these reasoning roles:

causal, system, risk, security, economic, domain, adversarial, verification, synthesis

Each role receives a distinct instruction contract. They are collected independently, then a final synthesis pass is created only when model replies are available.

This is a reasoning protocol, not a claim that nine independent model weights are running.

## Exposed interfaces

- GET /health
- GET /v1/interfaces
- POST /v1/think
- POST /v1/engineer
- POST /v1/compute/linear2x2
- POST /v1/simulate/physics

Example:

    python -m nexent.interfaces

Then:

    curl http://127.0.0.1:8787/v1/interfaces

Engineering request:

    curl -X POST http://127.0.0.1:8787/v1/engineer \
      -H 'Content-Type: application/json' \
      -d '{"problem":"Design a robotic thermal management system for a harsh environment."}'

## Domain guarantees

Mathematical computation uses Decimal and residual checks.

Physical simulation uses the existing deterministic nexent.physics engine.

No LLM is used to perform arithmetic or to grant execution authority.

Generated architectures remain candidates until downstream simulation, adversarial testing, verification, proof and VAIXLNS governance are satisfied.
