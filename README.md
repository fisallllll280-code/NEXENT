# NEXENT

نظام تنظيم شامل قابل للتشغيل، وليس مجرد فهرس.

NEXENT يجمع الأنظمة والمكونات والمفاهيم، يبني علاقاتها، يمرر النوايا عبر حوكمة صريحة، ينفذ القدرات، يسجل الأدلة، ويفتح دورة تطور منضبطة.

## الحلقة

IDENTIFY -> STRUCTURE -> CONNECT -> GOVERN -> EXECUTE -> OBSERVE -> PROVE -> RECORD -> REPLAY -> EVOLVE

## ما تم تركيبه

- System Graph: كيانات واعتماديات وكشف الدورات.
- Constitutional Gate: قرار صريح قبل التنفيذ.
- Capability Registry/Fabric: قدرات بإصدارات وحدود.
- V-IR boundary: تحويل Intent إلى تمثيل وسيط ثابت.
- Proof Lease: تفويض زمني ونطاقي للقدرة.
- Event Ledger: سجل append-only بسلسلة SHA-256.
- Evidence Engine: بصمات وربط التنفيذ برأس السجل والسياسة.
- Replay Engine: فحص سلامة السجل وإعادة التحقق.
- NEXENT DSL: لغة نوايا أولية.
- Evolution Engine: مقترحات تطور لا تنشر نفسها.

## مصادر التصميم

تمت مراجعة مستودعات VAIXLNS المتاحة المرتبطة بهذا الحساب، ومنها VAIXLNS-unified وvaixlns-core وvaixlns-csd-kernel. استفاد NEXENT من مفاهيم مثل ledger وdeterministic boundary وgovernance وproof وV-IR وleases وcontrolled evolution.

NEXENT مستقل عن VAIXLNS. الاستفادة هنا تركيب هندسي للأفكار، وليست دمجًا للمشروعين ولا ادعاء أن كل VAIXLNS منفذ داخل NEXENT.

## التشغيل

    python -m pip install -e .
    pytest
    python -m nexent.cli status
    python -m nexent.cli demo
    python -m nexent.cli run --intent "INTENT hello BY USER USING echo WITH message=world"

## الحالة

Implemented baseline: kernel + graph + governance + capability registry + ledger + evidence + replay + DSL + proof lease + evolution + tests + CI.

Target layers: persistent storage, full compiler/IR pipeline, sandboxing, distributed execution, knowledge graph/pattern forest/causal DAG, multi-agent mesh, cryptographic signatures, external adapters and production deployment.

القاعدة: لا ادعاء تنفيذ بلا أثر قابل للفحص في المستودع أو الاختبار.
