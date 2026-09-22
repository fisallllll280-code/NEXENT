# NEXENT — كتيب التحقق والأدلة

## الاختبارات
```bash
python -m pytest -q
cargo test --manifest-path rust/nexent-evidence/Cargo.toml
```

## طبقات الدليل
1. Source evidence
2. Test evidence
3. Runtime evidence
4. Determinism/replay evidence عندما ينطبق
5. Provenance

## حالة النظام
- SPECIFIED: مواصفة فقط.
- IMPLEMENTED: كود موجود.
- TESTED: اختبار منفذ وناجح.
- VERIFIED: دليل متكامل ومتكرر ومطابق للعقد.

لا يرفع المستودع إلى حالة VERIFIED بالنص وحده.
