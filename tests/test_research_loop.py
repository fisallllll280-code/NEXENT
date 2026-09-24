from nexent.research_loop import ResearchLoop, ResearchRecord, ResearchStage


def test_research_loop_follows_declared_order():
    loop = ResearchLoop()
    record = ResearchRecord(ResearchStage.OBSERVE, "SYS-1")
    for stage in ResearchLoop.ORDER[1:]:
        record = loop.transition(record, stage)
    assert record.stage is ResearchStage.ADOPTION


def test_research_loop_rejects_skipping_a_stage():
    loop = ResearchLoop()
    record = ResearchRecord(ResearchStage.OBSERVE, "SYS-1")
    try:
        loop.transition(record, ResearchStage.CANDIDATE)
    except ValueError:
        return
    raise AssertionError("stage skipping must be rejected")


def test_nexent_does_not_grant_authority():
    loop = ResearchLoop()
    record = ResearchRecord(ResearchStage.GOVERNANCE, "SYS-1")
    assert not loop.is_authorized(record, {})
    assert loop.is_authorized(record, {"approved": True})
