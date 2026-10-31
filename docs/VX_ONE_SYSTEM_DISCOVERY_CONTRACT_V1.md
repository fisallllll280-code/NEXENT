# VX ONE — System Discovery & Compatibility Contract v1

**Status:** PROPOSED / DISCOVERY CONTRACT ONLY  
**Responsibility:** NEXENT  
**Shared loader candidate:** VAIXLNS-unified PR #71

## Purpose

NEXENT supplies research, system discovery, compatibility intelligence, dependency analysis, and candidate metadata to the shared VX ONE loader. It does not become a second bootloader, installer, or execution authority.

## Discovery output

Each candidate system profile should include:
- stable system and release identity;
- vendor and official release metadata references;
- supported CPU architectures;
- UEFI/BIOS compatibility;
- Secure Boot support and constraints;
- TPM / measured-boot support where documented;
- minimum CPU, RAM, storage and firmware requirements;
- known conflicts, deprecated releases, and end-of-support dates;
- artifact digest and signature metadata, when available;
- source timestamp and provenance;
- confidence and unresolved evidence gaps.

## Discovery rules

- Prefer official vendor documentation and release metadata.
- Never invent download URLs, hashes, signing keys, or compatibility claims.
- Treat third-party mirrors as untrusted until separately admitted.
- Record contradictory vendor information instead of silently choosing one.
- Do not download, execute, install, partition, write boot sectors, modify firmware, or reboot.
- A compatibility prediction is not a successful boot test.

## Handoff

NEXENT emits a candidate profile and evidence references. VAIXLNS applies canonical governance and source policy. VAIXLNS-unified validates the shared manifest and creates a plan. VX-runtime may execute only separately authorized, isolated adapters.

## Status boundary

This document is not an implemented discovery agent or live vendor feed. It establishes the no-parallel-system boundary for future work.
