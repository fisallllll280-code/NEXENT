# NEXENT — كتيب التشغيل الكامل

## المسار التشغيلي
```
INPUT
  ↓
DSL / Intent
  ↓
Kernel
  ↓
Capability Binding
  ↓
Execution
  ↓
Evidence
  ↓
Ledger / State
  ↓
Verification
  ↓
Result
```

## تشغيل العرض
```bash
nexent demo
```

## تشغيل Intent
```bash
nexent run --intent 'INTENT demo BY CLI USING echo WITH message=NEXENT'
```

## تشغيل الحالة
```bash
nexent status
```

كل نتيجة تشغيل يجب أن تبقى قابلة لإعادة الاختبار، وأي جزء لم يثبت تشغيليًا لا يسمى Verified.
