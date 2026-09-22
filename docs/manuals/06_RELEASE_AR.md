# NEXENT — كتيب النشر

## بوابة النشر
يجب تحقق:
- Source inventory
- Dependency closure
- Unit/integration tests
- Rust evidence tests
- CLI smoke test
- Documentation complete
- Status explicitly classified
- No untracked release-critical files

## أمر التحقق
```bash
python -m pytest -q
cargo test --manifest-path rust/nexent-evidence/Cargo.toml
python -m nexent.cli status
python -m nexent.cli demo
```

## النتيجة
READY تعني نجاح البوابات المحددة فقط. لا تعني أن كل فكرة تاريخية أو كل مواصفة مستقبلية أصبحت منفذة.
