# NEXENT Multi-Platform Operational Interface Architecture

## Purpose

NEXENT exposes one canonical operational contract through multiple clients:

- Linux
- Windows
- Android
- Desktop shell
- Web/browser

The clients are presentation and device layers. They do not fork NEXENT's
kernel, governance, ledger, evidence, replay, or execution semantics.

## Canonical topology

```text
                         NEXENT CORE
                             |
              +--------------+--------------+
              |              |              |
          API Gateway    Event Gateway   Identity
              |              |              |
       +------+------+------+------+------+
       |      |      |      |      |
     Linux Windows Android Desktop Web
     Client Client Client  Shell  Client
       |      |      |      |      |
       +------+------+------+------+------+
                      |
              Shared NEXENT Contract
```

## Client boundary

Every client MUST use the same logical operations:

| Operation | Purpose |
|---|---|
| `intent.submit` | Submit a user/system intent |
| `execution.status` | Observe execution state |
| `event.stream` | Subscribe to canonical events |
| `governance.check` | Read/await governance decision |
| `evidence.get` | Retrieve evidence and provenance |
| `replay.verify` | Verify/replay an execution record |
| `registry.resolve` | Resolve canonical system/capability IDs |
| `session.sync` | Synchronize a client session |

## Platform roles

### Linux

Primary use: engineering, automation, service operation, local runtime,
diagnostics, and headless operation.

### Windows

Primary use: full desktop operational control, administration, development,
and user-facing workflows.

### Android

Primary use: mobile control, monitoring, approvals, notifications, search,
and session continuation. Android is a client; it does not become the
canonical execution authority.

### Desktop

The desktop shell provides a common desktop UX surface. It may host a web
UI or native presentation layer while keeping the same NEXENT protocol.

### Web

The browser client provides zero-install access to the same core contract.

## State and authority rules

1. Client UI state is not canonical system state.
2. The NEXENT core remains the source of operational truth.
3. Events are canonical and append-only at the core boundary.
4. Governance decisions are enforced by the core, not by UI code.
5. Evidence and replay identifiers are portable between clients.
6. A session may move from Android to desktop/Linux/Windows without creating
   a second execution identity.
7. Platform adapters may add device capabilities but cannot silently expand
   authority.

## Suggested repository layout

```text
nexent/
  interfaces/
    __init__.py
    manifest.py

interfaces/
  linux/
  windows/
  android/
  desktop/
  web/

docs/
  NEXENT_MULTIPLATFORM_INTERFACE_ARCHITECTURE.md
```

The `interfaces/*` directories are client implementations. The Python
`nexent/interfaces` package is the shared contract and must stay
platform-neutral.

## VAIXLNS boundary

NEXENT remains an independent engine. When integrated with VAIXLNS:

```text
VAIXLNS / V
      |
      +-- VV  Knowledge / Discovery
      +-- VX  Execution
      +-- XV  Intelligence
      |
      +-- NEXENT
             |
             +-- Linux
             +-- Windows
             +-- Android
             +-- Desktop
             +-- Web
```

NEXENT can consume and propose through governed VAIXLNS interfaces, but a
client UI must never bypass the governance boundary.

## Implementation status

- **Specified:** canonical five-platform interface surface.
- **Implemented:** Python manifest and validation contract.
- **Pending:** native Linux/Windows clients, Android application, desktop
  shell, web client, authenticated API gateway, event transport, and
  end-to-end conformance tests.

This distinction is intentional: interface specification is not presented as
evidence of native applications already being built.
