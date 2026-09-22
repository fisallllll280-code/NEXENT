# NEXENT — تشغيل المنظومات الداخلية

## Kernel
يمثل نقطة تجميع التنفيذ والحوكمة والإثبات.

## Ledger / Evidence
يُستخدم لتسجيل ما حدث وتوفير أثر قابل للمراجعة.

## DSL
تحويل صيغة Intent إلى بنية تنفيذية يفهمها النواة.

## Registry / Canonical / Archive
هذه منظومات تنظيم وتحليل. لا تُعامل كخدمات مستقلة قابلة للنشر إلا عندما يوجد Entry Point واختبار تشغيل فعلي.

## قاعدة الربط
كل منظومة تُسجل:
```
System ID
Source
Inputs
Outputs
Dependencies
Invariants
Evidence
Verification State
```

ولا يتم دمج منظومتين بحذف مصدر أي منهما؛ الربط يتم عبر provenance والعقود.
