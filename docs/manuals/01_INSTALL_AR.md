# NEXENT — كتيب التثبيت

## المتطلبات
- Python 3.11 أو أحدث.
- Git.
- Rust toolchain لطبقة الأدلة Rust.

## التثبيت
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . pytest
```

## فحص الحالة
```bash
python -m nexent.cli status
```

## فحص الحزمة
```bash
python -m pytest -q
cargo test --manifest-path rust/nexent-evidence/Cargo.toml
```

لا يبدأ النشر قبل نجاح الاختبارات المحلية وCI.
