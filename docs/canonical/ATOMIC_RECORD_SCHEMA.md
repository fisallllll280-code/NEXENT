# NEXENT Atomic Record Schema

Every recovered or generated architecture artifact must be representable without losing identity or lineage.

Required dimensions:

- identity
- legacy_id
- aliases
- semantic_type
- status
- origin
- meaning
- parent
- children
- dependencies
- capabilities
- contracts
- authority
- policies
- constraints
- inputs
- outputs
- state
- events
- execution
- evidence
- verification
- proof
- failure
- recovery
- security
- observability
- implementation
- repository
- tests
- lifecycle
- supersedes
- superseded_by
- canonical_destination

Atomicity rule:

A record is atomic only when removing a further independent semantic unit would change the identity or contract of the record.

Lineage is preserved even when a legacy record is merged into a canonical record.
