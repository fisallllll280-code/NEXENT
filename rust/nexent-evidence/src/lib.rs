use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub const SCHEMA_VERSION: &str = "NEXENT-EVIDENCE-1";

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum SystemStatus { Nominal, Degraded, Contained, Halted }

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SystemState {
    pub memory_usage_mb: u64,
    pub max_memory_limit_mb: u64,
    pub active_processes: u32,
    pub error_count: u32,
    pub status: SystemStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct InvariantCheckResult {
    pub invariant_id: String,
    pub passed: bool,
    pub detail: String,
}

pub trait Invariant {
    fn id(&self) -> &'static str;
    fn check(&self, state: &SystemState) -> InvariantCheckResult;
}

pub struct MemoryInvariant;
impl Invariant for MemoryInvariant {
    fn id(&self) -> &'static str { "INV_MEM_01" }
    fn check(&self, state: &SystemState) -> InvariantCheckResult {
        let passed = state.memory_usage_mb <= state.max_memory_limit_mb;
        InvariantCheckResult {
            invariant_id: self.id().into(), passed,
            detail: format!("memory={}MB limit={}MB", state.memory_usage_mb, state.max_memory_limit_mb),
        }
    }
}

pub struct ErrorInvariant { pub max_errors: u32 }
impl Invariant for ErrorInvariant {
    fn id(&self) -> &'static str { "INV_ERR_02" }
    fn check(&self, state: &SystemState) -> InvariantCheckResult {
        let passed = state.error_count < self.max_errors;
        InvariantCheckResult {
            invariant_id: self.id().into(), passed,
            detail: format!("errors={} threshold={}", state.error_count, self.max_errors),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AuditEntry {
    pub sequence: u64,
    pub timestamp: u64,
    pub step_name: String,
    pub state_snapshot: SystemState,
    pub invariant_results: Vec<InvariantCheckResult>,
    pub previous_hash: String,
    pub current_hash: String,
}

impl AuditEntry {
    fn calculate_hash(
        sequence: u64, timestamp: u64, step_name: &str, state: &SystemState,
        checks: &[InvariantCheckResult], previous_hash: &str,
    ) -> String {
        let payload = serde_json::to_vec(&(sequence, timestamp, step_name, state, checks, previous_hash))
            .expect("canonical evidence serialization cannot fail");
        let mut hasher = Sha256::new();
        hasher.update(payload);
        format!("{:x}", hasher.finalize())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EvidencePack {
    pub schema_version: String,
    pub project_name: String,
    pub total_steps_executed: usize,
    pub all_invariants_passed: bool,
    pub audit_trail: Vec<AuditEntry>,
    pub final_system_status: SystemStatus,
    pub cryptographic_root_hash: String,
}

impl EvidencePack {
    pub fn verify_integrity(&self) -> bool {
        let mut previous = "GENESIS".to_string();
        for entry in &self.audit_trail {
            if entry.previous_hash != previous { return false; }
            let expected = AuditEntry::calculate_hash(
                entry.sequence, entry.timestamp, &entry.step_name,
                &entry.state_snapshot, &entry.invariant_results, &entry.previous_hash,
            );
            if entry.current_hash != expected { return false; }
            previous = entry.current_hash.clone();
        }
        self.cryptographic_root_hash == previous
    }
}

pub struct NexentCoreEngine {
    pub current_state: SystemState,
    pub audit_trail: Vec<AuditEntry>,
    invariants: Vec<Box<dyn Invariant>>,
}

impl NexentCoreEngine {
    pub fn new(max_memory_mb: u64, max_errors: u32) -> Self {
        Self {
            current_state: SystemState {
                memory_usage_mb: 128, max_memory_limit_mb: max_memory_mb,
                active_processes: 1, error_count: 0, status: SystemStatus::Nominal,
            },
            audit_trail: Vec::new(),
            invariants: vec![
                Box::new(MemoryInvariant),
                Box::new(ErrorInvariant { max_errors }),
            ],
        }
    }

    pub fn execute_step(
        &mut self, timestamp: u64, step_name: impl Into<String>,
        memory_delta_mb: i64, error_injected: bool,
    ) -> &AuditEntry {
        let name = step_name.into();
        if memory_delta_mb >= 0 {
            self.current_state.memory_usage_mb =
                self.current_state.memory_usage_mb.saturating_add(memory_delta_mb as u64);
        } else {
            self.current_state.memory_usage_mb =
                self.current_state.memory_usage_mb.saturating_sub(memory_delta_mb.unsigned_abs());
        }
        if error_injected {
            self.current_state.error_count = self.current_state.error_count.saturating_add(1);
        }

        let checks: Vec<_> = self.invariants.iter().map(|i| i.check(&self.current_state)).collect();
        if checks.iter().any(|c| !c.passed) {
            self.current_state.status = SystemStatus::Contained;
        }

        let previous_hash = self.audit_trail.last()
            .map(|e| e.current_hash.clone()).unwrap_or_else(|| "GENESIS".into());
        let sequence = self.audit_trail.len() as u64;
        let current_hash = AuditEntry::calculate_hash(
            sequence, timestamp, &name, &self.current_state, &checks, &previous_hash,
        );
        self.audit_trail.push(AuditEntry {
            sequence, timestamp, step_name: name,
            state_snapshot: self.current_state.clone(),
            invariant_results: checks, previous_hash, current_hash,
        });
        self.audit_trail.last().expect("entry was just pushed")
    }

    pub fn export_evidence_pack(&self) -> EvidencePack {
        let root_hash = self.audit_trail.last()
            .map(|e| e.current_hash.clone()).unwrap_or_else(|| "GENESIS".into());
        EvidencePack {
            schema_version: SCHEMA_VERSION.into(),
            project_name: "NEXENT_CORE".into(),
            total_steps_executed: self.audit_trail.len(),
            all_invariants_passed: self.audit_trail.iter()
                .all(|e| e.invariant_results.iter().all(|c| c.passed)),
            audit_trail: self.audit_trail.clone(),
            final_system_status: self.current_state.status,
            cryptographic_root_hash: root_hash,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn scenario() -> EvidencePack {
        let mut engine = NexentCoreEngine::new(1024, 5);
        engine.execute_step(1, "boot", 64, false);
        engine.execute_step(2, "load", 256, false);
        engine.execute_step(3, "stress", 800, true);
        engine.export_evidence_pack()
    }
    #[test] fn deterministic_same_inputs_same_evidence() { assert_eq!(scenario(), scenario()); }
    #[test] fn invariant_failure_contains_system() {
        let pack = scenario();
        assert_eq!(pack.final_system_status, SystemStatus::Contained);
        assert!(!pack.all_invariants_passed);
    }
    #[test] fn tampering_breaks_integrity() {
        let mut pack = scenario();
        pack.audit_trail[0].step_name = "tampered".into();
        assert!(!pack.verify_integrity());
    }
    #[test] fn valid_chain_verifies() { assert!(scenario().verify_integrity()); }
}
