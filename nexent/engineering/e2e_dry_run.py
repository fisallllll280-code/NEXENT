from nexent.engineering.formal_execution import FormalExecution
from nexent.engineering.lifecycle import Phase

PHASES=list(Phase)

def run_end_to_end(system_id="NEXENT-E2E"):
    run=FormalExecution(system_id)
    for phase in PHASES[:-1]:
        artifact=run.emit(
            f"{phase.value.lower()}-001",
            phase.value.lower(),
            {"phase":phase.value,"system_id":system_id,"sequence":PHASES.index(phase)},
        )
        run.advance(
            artifact.artifact_id,
            approved=phase in {Phase.GOVERNANCE, Phase.RELEASE},
        )
    return run

def main():
    run=run_end_to_end()
    manifest=run.manifest()
    assert manifest["complete"] is True
    assert manifest["current_phase"] == Phase.EVOLUTION.value
    assert len(manifest["records"]) == len(PHASES)-1
    print("NEXENT E2E PASS")
    print(manifest)

if __name__ == "__main__":
    main()
