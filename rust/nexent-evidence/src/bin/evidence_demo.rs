use nexent_evidence::NexentCoreEngine;

fn main() {
    let mut engine = NexentCoreEngine::new(1024, 5);
    engine.execute_step(1, "boot", 64, false);
    engine.execute_step(2, "load_models_and_constraints", 256, false);
    engine.execute_step(3, "heavy_simulation", 500, false);
    engine.execute_step(4, "fault_injection", 300, true);
    let evidence = engine.export_evidence_pack();
    assert!(evidence.verify_integrity());
    println!("{}", serde_json::to_string_pretty(&evidence).unwrap());
}
