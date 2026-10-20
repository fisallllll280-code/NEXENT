# الفهرس المرتب — NEXENT

تاريخ الجرد: 2026-10-21 (الرياض).

- المستودع: `fisallllll280-code/NEXENT`.
- مصدر الجرد: شجرة Git الكاملة للالتزام `f62cf5920174551f9a8f88deb420f9515bedc284`؛ دون اقتطاع.
- المسؤولية: البحث والاكتشاف والتركيب ومقترحات المعمارية.
- عدد الملفات قبل إضافة هذا الفهرس: **164**.
- الأصل: Derived / فهرس ملاحي مشتق من مسارات Git؛ لا يعيد ترقيم هويات Ω أو الفهرس التاريخي.
- الحالة: جرد ملفات مرصودة فقط؛ لا يثبت اجتياز الاختبارات أو التشغيل أو اعتماد المحتوى.

## 1. ترتيب القراءة والعمل

1. هوية المستودع وREADME وعقد المسؤولية إن وجد.
2. الفهارس والمواصفات والعقود والسياسات.
3. الشيفرة والموصلات والواجهات الموجودة.
4. الاختبارات وملفات CI والأدلة المسجلة؛ وجودها لا يثبت نجاحها.
5. التشغيل والاستعادة ثم مراجعة الأدلة والاعتماد.

## 2. حدود المسؤوليات بين المستودعات

| المستودع | المسؤولية | فهرسه في فرع المراجعة |
|---|---|---|
| VAIXLNS | المرجع المركزي للمعمارية والحوكمة والفهارس والاستعادة | [الفهرس](https://github.com/fisallllll280-code/VAIXLNS/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |
| VAIXLNS-unified | التنفيذ المتكامل؛ لا يمنح سلطة اعتماد مرجعي | [الفهرس](https://github.com/fisallllll280-code/VAIXLNS-unified/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |
| VX-runtime | التنفيذ المحكوم وسياسات القدرات والأحداث وإعادة التشغيل | [الفهرس](https://github.com/fisallllll280-code/VX-runtime/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |
| NEXENT | البحث والاكتشاف والتركيب ومقترحات المعمارية | [الفهرس](https://github.com/fisallllll280-code/NEXENT/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |
| NAXLNS | الهندسة وتحليل المستودعات ومرشحات التحقق | [الفهرس](https://github.com/fisallllll280-code/NAXLNS/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |
| vx-financial-kernel | النواة المالية والمحاكاة؛ الوصف لا يثبت تشغيلًا ماليًا | [الفهرس](https://github.com/fisallllll280-code/vx-financial-kernel/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |
| vx-agents-fabric | تنسيق الوكلاء المتخصصين وعقود الأدوات والمراجعة | [الفهرس](https://github.com/fisallllll280-code/vx-agents-fabric/blob/docs/ordered-repository-indexes-20261021/docs/indexes/ORDERED_REPOSITORY_INDEX_AR.md) |

VAIXLNS يحكم الاعتماد المرجعي. لا تثبت هذه الخريطة اتصالًا حيًا بين الأنظمة. تبقى مطابقة VLNS مع NAXLNS ومطابقة NEXNET مع NEXENT غير محسومتين وفق فهرس الاتحاد؛ لا إعادة تسمية أو دمج تلقائيًا.

## 3. ترتيب الفهارس الأصلي 00–27

الترتيب التالي من [تصنيف الفهرس الأصلي](https://github.com/fisallllll280-code/VAIXLNS/blob/6bd55a9b44696cc2c7746bc66e2d39f0f274a81f/registry/indexes/zero-loss-index-taxonomy.v1.json)؛ هو ترتيب مناظر الفهرس وليس أرقام بنود تاريخية.

| الترتيب | الفهرس | المفتاح الأصلي |
|---|---|---|
| 00 | المصادر | `source_index` |
| 01 | الفهرس التاريخي | `legacy_master_index` |
| 02 | الكيانات | `entity_index` |
| 03 | المصطلحات | `terminology_index` |
| 04 | الابتكارات | `innovation_index` |
| 05 | المعمارية | `architecture_index` |
| 06 | القدرات | `capability_index` |
| 07 | العقود | `contract_index` |
| 08 | الصلاحيات | `authority_index` |
| 09 | الأحداث | `event_index` |
| 10 | الحالات | `state_index` |
| 11 | الاعتماديات | `dependency_index` |
| 12 | العلاقات | `relation_index` |
| 13 | النسب والإصدارات التاريخية | `lineage_index` |
| 14 | المراجع المعتمدة | `canonical_index` |
| 15 | التنفيذ | `implementation_index` |
| 16 | المستودعات | `repository_index` |
| 17 | الملفات والمخرجات | `artifact_index` |
| 18 | الاختبارات | `test_index` |
| 19 | الأدلة | `evidence_index` |
| 20 | البراهين | `proof_index` |
| 21 | التشغيل | `operation_index` |
| 22 | الفشل والاستعادة | `failure_recovery_index` |
| 23 | الأمن | `security_index` |
| 24 | الرصد | `observability_index` |
| 25 | المحاكاة | `simulation_index` |
| 26 | التطور | `evolution_index` |
| 27 | الإحالات المتقاطعة | `cross_reference_index` |

## 4. جرد جميع الملفات بالترتيب

ترتيب ثابت بحسب المسار. الرقم هنا رقم عرض محلي فقط. البصمة **Git blob SHA-1** كما أعادتها واجهة Git وليست SHA-256 لبايتات الملف. روابط المصدر مثبتة على الالتزام أعلاه. لا يشمل الجرد فروعًا أخرى أو تاريخ Git الكامل أو ملفات خارج المستودع، ولا يشمل الفهرس الجديد نفسه.

| رقم العرض | الملف الأصلي | الحجم بالبايت | Git blob SHA-1 |
|---|---|---:|---|
| 0001 | [.github/ISSUE_TEMPLATE/custom.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.github/ISSUE_TEMPLATE/custom.md) | 126 | `48d5f81fa422964dd1eea360efdecfc5dc9a6c87` |
| 0002 | [.github/workflows/ci.yml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.github/workflows/ci.yml) | 472 | `a00accfda8538fa9de57924460867be504fc33fd` |
| 0003 | [.github/workflows/external-integration-boundary.yml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.github/workflows/external-integration-boundary.yml) | 468 | `a7ee24e9d94ca058ba0e264091e216ecf3895094` |
| 0004 | [.github/workflows/nexent.yml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.github/workflows/nexent.yml) | 446 | `cfc2437976fbb74344b4203999f02393c59ccfbd` |
| 0005 | [.github/workflows/verification.yml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.github/workflows/verification.yml) | 484 | `6776d834f2e3c4e7d5ac8225a9d7343e7005de7a` |
| 0006 | [.github/workflows/web.yml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.github/workflows/web.yml) | 601 | `ee087c6ec921fbd999d98ca42c5d52c816f1c22c` |
| 0007 | [.gitignore](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/.gitignore) | 697 | `529fe7632257e5d536c98e1cfe8a0141177fdee1` |
| 0008 | [README.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/README.md) | 57756 | `9bfa3e4f5a364d06f36b301d176c8df64446d22c` |
| 0009 | [VAIXLNS_REPOSITORY_CONTRACT.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/VAIXLNS_REPOSITORY_CONTRACT.md) | 737 | `d7173ee49044f47e705066c87513d5d50280f38a` |
| 0010 | [docs/MASTER_FEDERATED_INDEX.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/MASTER_FEDERATED_INDEX.md) | 6924 | `3ad393a78076213938694cc851665983da924819` |
| 0011 | [docs/NEXENT_ARCHITECTURE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_ARCHITECTURE.md) | 1544 | `9ac741674077300f804cb38e7a4e9ff3ff325a61` |
| 0012 | [docs/NEXENT_CANONICAL_INNOVATION_INDEX_V1.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_CANONICAL_INNOVATION_INDEX_V1.md) | 723 | `5d1c1d43577dec74f111f8f5d0fe8897a7214d23` |
| 0013 | [docs/NEXENT_COMPLETE_LINEAR_ENGINEERING_SPEC.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_COMPLETE_LINEAR_ENGINEERING_SPEC.md) | 2027 | `8a25e72cb094b6ab02c55f5ccf63b9d572521572` |
| 0014 | [docs/NEXENT_COMPLETE_SYSTEM_AND_INNOVATION_INVENTORY.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_COMPLETE_SYSTEM_AND_INNOVATION_INVENTORY.md) | 4623 | `6f329e74a16eb940cba8ae093beeb42c8bbba486` |
| 0015 | [docs/NEXENT_COMPUTATIONAL_PHYSICAL_SOFTWARE_MATHEMATICAL_ARCHITECTURE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_COMPUTATIONAL_PHYSICAL_SOFTWARE_MATHEMATICAL_ARCHITECTURE.md) | 2226 | `756da0c421a12854794fb2c0155ed72ae03592be` |
| 0016 | [docs/NEXENT_END_TO_END_DRY_RUN.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_END_TO_END_DRY_RUN.md) | 1496 | `69e556a32d48f4119f6c8e74552903bed10e3803` |
| 0017 | [docs/NEXENT_EVIDENCE_PACK_ARTIFACT.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_EVIDENCE_PACK_ARTIFACT.md) | 1589 | `4d7cbae7d15baa9c403ff61c156e9ee3ae5ff639` |
| 0018 | [docs/NEXENT_EXECUTABLE_ENGINEERING_LAYER.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_EXECUTABLE_ENGINEERING_LAYER.md) | 1091 | `b37f592857975742d66174b6541b5ea30cf19b02` |
| 0019 | [docs/NEXENT_FINANCIAL_ENGINEERING_PORTFOLIO_SPEC.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_FINANCIAL_ENGINEERING_PORTFOLIO_SPEC.md) | 7464 | `6e8af629d304915c16d7d4dc5e7f53fd65874f70` |
| 0020 | [docs/NEXENT_FORMAL_LINEAR_ENGINEERING_EXECUTION.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_FORMAL_LINEAR_ENGINEERING_EXECUTION.md) | 2195 | `d6e6e2bd76edf8c4a790556a6a70cd5facfe62f3` |
| 0021 | [docs/NEXENT_FORMAL_LINEAR_ENGINEERING_LIFECYCLE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_FORMAL_LINEAR_ENGINEERING_LIFECYCLE.md) | 1411 | `dba51eb2f60b7803351cbe3aa5967184bc9a75d1` |
| 0022 | [docs/NEXENT_IMPOSSIBLE_TO_ENGINEERING_METHOD.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_IMPOSSIBLE_TO_ENGINEERING_METHOD.md) | 635 | `64e4f73d6c29bf1084454ede188b0f86689295a5` |
| 0023 | [docs/NEXENT_INNOVATION_BOUNDARY.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_INNOVATION_BOUNDARY.md) | 1938 | `3b253f5688af0495918ca4a58b260e38985d9a72` |
| 0024 | [docs/NEXENT_INTENT_WEB_IMPLEMENTATION.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_INTENT_WEB_IMPLEMENTATION.md) | 3818 | `ae0c2589edf3f7d72f27eb3a0369e955f202020f` |
| 0025 | [docs/NEXENT_MASTER_ENGINEERING_WORK.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_MASTER_ENGINEERING_WORK.md) | 4157 | `77469c1d9258eca8f6d4ab23d4a9cf418ce8d855` |
| 0026 | [docs/NEXENT_MASTER_INVENTORY_SOURCE_NORMALIZED.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_MASTER_INVENTORY_SOURCE_NORMALIZED.md) | 17324 | `28989ebab77999cc54f41ba116cf4edbfd3988b1` |
| 0027 | [docs/NEXENT_MASTER_INVENTORY_SOVEREIGN_INNOVATION_BLUEPRINT.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_MASTER_INVENTORY_SOVEREIGN_INNOVATION_BLUEPRINT.md) | 14846 | `ec00ab0ff67d43830905adb358558be00c342ba9` |
| 0028 | [docs/NEXENT_MASTER_REGISTRY.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_MASTER_REGISTRY.md) | 1121 | `64abac0b3ec203729f1336e4d2d8942e8e8f1cc4` |
| 0029 | [docs/NEXENT_MISSING_SYSTEM_DISCOVERY_ENGINE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_MISSING_SYSTEM_DISCOVERY_ENGINE.md) | 3015 | `d56322fa04b3ab59cc6b31e3ea74f62be1c2a289` |
| 0030 | [docs/NEXENT_MULTIPLATFORM_INTERFACE_ARCHITECTURE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_MULTIPLATFORM_INTERFACE_ARCHITECTURE.md) | 4031 | `32ddf38200e8868c17df9bac0d63020ad3d832f5` |
| 0031 | [docs/NEXENT_RECOVERED_INNOVATIONS.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_RECOVERED_INNOVATIONS.md) | 3301 | `18c70954b7e6ff4c3c961a0ac43b746491f929df` |
| 0032 | [docs/NEXENT_REPOSITORY_FABRIC.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_REPOSITORY_FABRIC.md) | 2569 | `d0a3bbf72165c6724e689493f26f96e074dfc71d` |
| 0033 | [docs/NEXENT_SAFETY_KERNEL.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_SAFETY_KERNEL.md) | 1459 | `f59b4a679c08845572b7aa5ede284ae4f89f76f9` |
| 0034 | [docs/NEXENT_SEMANTIC_IMPACT_CONE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_SEMANTIC_IMPACT_CONE.md) | 1068 | `3bc9e5c8a2f35fde533d4cfea34969cd0be49b17` |
| 0035 | [docs/NEXENT_SPECIALIST_AGENT_SYSTEM.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/NEXENT_SPECIALIST_AGENT_SYSTEM.md) | 3948 | `6d4826c4566c7d4f4c2adce90b161fd8314893d9` |
| 0036 | [docs/REPOSITORY_ACTIVATION_MATRIX.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/REPOSITORY_ACTIVATION_MATRIX.md) | 2664 | `429ba583f8544b2471684a4ed50e1c872e3af661` |
| 0037 | [docs/REPOSITORY_OPERATIONS.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/REPOSITORY_OPERATIONS.md) | 948 | `e208ce145c9a61267fef5def0c15f71529e16777` |
| 0038 | [docs/SELF_DIRECTED_MULTI_MIND_ARCHITECTURE.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/SELF_DIRECTED_MULTI_MIND_ARCHITECTURE.md) | 7787 | `c1c5bfac6ab94dd7e382c3247cb3bf5721c844e9` |
| 0039 | [docs/VAIXLNS_FEDERATION_BOUNDARY.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/VAIXLNS_FEDERATION_BOUNDARY.md) | 1136 | `e3758bb0792472fd5de56223824d626665739ece` |
| 0040 | [docs/VAIXLNS_FEDERATION_ROLE_V1.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/VAIXLNS_FEDERATION_ROLE_V1.md) | 729 | `26de8fe7d067f0213e1fb5b9e1951d3092f7b601` |
| 0041 | [docs/VAIXLNS_INNOVATION_BOUNDARY.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/VAIXLNS_INNOVATION_BOUNDARY.md) | 793 | `9dee9d8dcfb38ead9e77dcc56b8693d3321130e1` |
| 0042 | [docs/VLNS_OPERATING_DEVELOPMENT_SPEC.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/VLNS_OPERATING_DEVELOPMENT_SPEC.md) | 13955 | `33d8248c4a20d72668af9880386fa6cd79708a1e` |
| 0043 | [docs/canonical/ARCHITECTURE_SEARCH.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/canonical/ARCHITECTURE_SEARCH.md) | 726 | `7bfb421dfcfd175cd1e2b9586e6cebf607134b09` |
| 0044 | [docs/canonical/ATOMIC_RECORD_SCHEMA.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/canonical/ATOMIC_RECORD_SCHEMA.md) | 800 | `a7543fcdd567f942f99e40a07cd1f9b529ac0049` |
| 0045 | [docs/canonical/NEXENT_CANONICAL_ARCHITECTURE_V1.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/canonical/NEXENT_CANONICAL_ARCHITECTURE_V1.md) | 1265 | `c900493738552426f538a14a7a072db7c2c91618` |
| 0046 | [docs/canonical/VAIXLNS_FEDERATION_BINDING_V1.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/canonical/VAIXLNS_FEDERATION_BINDING_V1.md) | 903 | `a6e20fc87d61902fc3060b5aa02d7ba0f5954c00` |
| 0047 | [docs/domains/FINANCIAL_DOMAIN_CONTRACT.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/domains/FINANCIAL_DOMAIN_CONTRACT.md) | 1628 | `766a159553e93a69b0c063bb1904ec02de4ac96c` |
| 0048 | [docs/domains/FINANCIAL_RESEARCH_MAP.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/domains/FINANCIAL_RESEARCH_MAP.md) | 877 | `d528917c3a09c2c083dee9850111210434181353` |
| 0049 | [docs/integration/ARC_X_BOUNDARY_V1.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/integration/ARC_X_BOUNDARY_V1.md) | 1103 | `cdb18f62b03bb438e3bb3eeca067258d6bb02196` |
| 0050 | [docs/integration/VAIXLNS_ADOPTION_CONTRACT.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/integration/VAIXLNS_ADOPTION_CONTRACT.md) | 691 | `59625775a12113423ed8f4f5560cb52d2fb9adb0` |
| 0051 | [docs/integration/VAIXLNS_FEDERATION.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/integration/VAIXLNS_FEDERATION.md) | 1509 | `3a42d0bf33701e3c6c31831dc805b997543b4724` |
| 0052 | [docs/lineage/STATUS_MODEL.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/lineage/STATUS_MODEL.md) | 575 | `ce9ba4a1c2f4d616852ba62a0d0c157a0991e526` |
| 0053 | [docs/manuals/00_MANUAL_INDEX_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/00_MANUAL_INDEX_AR.md) | 858 | `355de71020b0ec7e00615e37e471ddf1910af4a7` |
| 0054 | [docs/manuals/01_INSTALL_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/01_INSTALL_AR.md) | 554 | `5961077ea418f68d999ada4b13a63a245ff37981` |
| 0055 | [docs/manuals/02_FULL_OPERATION_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/02_FULL_OPERATION_AR.md) | 610 | `c76076cf23cbd5f87dad128e229cc89fdaf76d97` |
| 0056 | [docs/manuals/03_SUBSYSTEM_OPERATION_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/03_SUBSYSTEM_OPERATION_AR.md) | 850 | `13d623ee3940e138fbec6c66cb3f6a8153539cc4` |
| 0057 | [docs/manuals/04_VERIFICATION_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/04_VERIFICATION_AR.md) | 605 | `8714b284a7d47a0b313ccd2b58461cb6a01c3f95` |
| 0058 | [docs/manuals/05_RECOVERY_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/05_RECOVERY_AR.md) | 687 | `257f01b60ff508bccadf41e691f402bfd6fa04b2` |
| 0059 | [docs/manuals/06_RELEASE_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/06_RELEASE_AR.md) | 637 | `f824aad45f099c584fcf81552d40d5c817bd31b2` |
| 0060 | [docs/manuals/07_STATUS_AND_LIMITS_AR.md](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/docs/manuals/07_STATUS_AND_LIMITS_AR.md) | 652 | `12b4e05cde18f80197c0051cdcfa97e3613e279e` |
| 0061 | [examples/hello.nex](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/examples/hello.nex) | 64 | `deb26a35128a4fdf43270a021480c218226c6f70` |
| 0062 | [nexent/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/__init__.py) | 278 | `b7148879c6555528b54cad4cb53ad7456e82154e` |
| 0063 | [nexent/agents/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/agents/__init__.py) | 178 | `9fe494831d71ea63bed38372700470a70494a1be` |
| 0064 | [nexent/agents/registry.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/agents/registry.py) | 2416 | `2718e69b4d0eb26aa367aaf72eef437f497e8536` |
| 0065 | [nexent/architecture_contract.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/architecture_contract.py) | 1773 | `e315dd37f64f0051bf992b1f93117104892d66ec` |
| 0066 | [nexent/archive.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/archive.py) | 2032 | `63057ea4cbaf0d116282beca7d9eacdd5bf033e7` |
| 0067 | [nexent/canonical.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/canonical.py) | 4761 | `3bd45f91abe70fca6aff63159b045a7629c0b1d7` |
| 0068 | [nexent/cli.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/cli.py) | 1650 | `e123fec31fb3883ab1c95ff18f16646cdcb8e89d` |
| 0069 | [nexent/clock.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/clock.py) | 161 | `4fec4388333d195cf78b6743832cd710a8ec8081` |
| 0070 | [nexent/dsl.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/dsl.py) | 967 | `5534a504070504b46a04f9c58159320f9daa23b0` |
| 0071 | [nexent/engineering/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/__init__.py) | 450 | `c2b8566b3332e34e274e131236e638bd8232039a` |
| 0072 | [nexent/engineering/compiler.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/compiler.py) | 1263 | `bab035fbbaadb1472fd8d3cae1de05cc7b85b22a` |
| 0073 | [nexent/engineering/contradiction.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/contradiction.py) | 1691 | `7a8eb7209ac252d32b7a83b50c35c46cb022ab43` |
| 0074 | [nexent/engineering/coordination.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/coordination.py) | 2035 | `da2f5fc82b3c9f611f827d5cfc2df79257b66896` |
| 0075 | [nexent/engineering/core.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/core.py) | 4199 | `e15bc1b5ac9122469cd43d54fefade0cab5b6d98` |
| 0076 | [nexent/engineering/e2e_dry_run.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/e2e_dry_run.py) | 895 | `526c5b6a6e0389fff2517d4cd6879b9420a2ff9b` |
| 0077 | [nexent/engineering/formal_execution.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/formal_execution.py) | 2453 | `27eff4c03064f73b2ae3a29983017d30fb2f848b` |
| 0078 | [nexent/engineering/ideas.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/ideas.py) | 746 | `490c8c41ccf98ec7b767b1d867fc35991c037231` |
| 0079 | [nexent/engineering/impact.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/impact.py) | 2470 | `0e00198f64d0a215c2c9baee2a5244e8da020431` |
| 0080 | [nexent/engineering/lifecycle.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/lifecycle.py) | 3119 | `add02754a564c0ace7ddcea2762f47d5617e32ab` |
| 0081 | [nexent/engineering/neo.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/neo.py) | 1911 | `61f7bba34463b7b09bf1ae3f1dbb74d87a3be1c1` |
| 0082 | [nexent/engineering/pipeline.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/pipeline.py) | 2017 | `67811239d2103f90b31c3b341c776ea3accf1f4a` |
| 0083 | [nexent/engineering/runtime.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/engineering/runtime.py) | 2140 | `d6a3920de4027f7206c5e62f9a5bf5ebe16211a3` |
| 0084 | [nexent/epistemic_kernel.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/epistemic_kernel.py) | 3595 | `64224da7dce3491dc25856277fae444836580b74` |
| 0085 | [nexent/evolution.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/evolution.py) | 876 | `4f2727e770dc7be9445c3d90e42b8c9284bbdc0b` |
| 0086 | [nexent/external_integration_boundary.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/external_integration_boundary.py) | 1826 | `2c16ac58c2a3d6dd5f935bf9401cd1bf7d0b1f4a` |
| 0087 | [nexent/financial_proof.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/financial_proof.py) | 2162 | `8d48b4da2c4659e646461d6f0066e0be6744f419` |
| 0088 | [nexent/governance.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/governance.py) | 1086 | `57faad8ec0347e575ed6f7e4c9ce917c5b73d998` |
| 0089 | [nexent/graph.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/graph.py) | 1608 | `01e01dc5ed596f3c5f2cbdcbc3aea15ba791dbb6` |
| 0090 | [nexent/interfaces/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/interfaces/__init__.py) | 362 | `eaf70b14ad4e996b37ab005f6f22bbc62d0ab2e2` |
| 0091 | [nexent/interfaces/manifest.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/interfaces/manifest.py) | 2905 | `6f52216a2fd4487681e2652668eb278fcf5c0f2f` |
| 0092 | [nexent/ir.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/ir.py) | 673 | `473162fffb4819d233d61ce7bf73385f0c44c611` |
| 0093 | [nexent/kernel.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/kernel.py) | 3889 | `5a24f1339e15b902843ebaa0c114b8ff54843acd` |
| 0094 | [nexent/languages.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/languages.py) | 2550 | `ec037aadf7fe1583e92e382691d3632574780805` |
| 0095 | [nexent/lease.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/lease.py) | 770 | `fa84e8c06a0ab2ea21b3dce2c0d9ed58ee9b2d1d` |
| 0096 | [nexent/ledger.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/ledger.py) | 2908 | `572e135ee8841f87eb1a8411cae1bda07c6dcbcb` |
| 0097 | [nexent/master_registry.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/master_registry.py) | 4443 | `1c20133ea0f1127cc87a1e6d1c61085e228441f0` |
| 0098 | [nexent/missing_system.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/missing_system.py) | 5852 | `912db1c47b79b4dcd0c4b04be36ccb94141f1eca` |
| 0099 | [nexent/model.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/model.py) | 1366 | `925f042f706a8a813e4643c8945835dc970cee2a` |
| 0100 | [nexent/omega_fabric_contract.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/omega_fabric_contract.py) | 516 | `df4f71e97f43b76e16b0b2619d9874c0826caba3` |
| 0101 | [nexent/operational/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/operational/__init__.py) | 93 | `0190cf068dc6884b12628d8ac28a21c57204c41a` |
| 0102 | [nexent/operational/record.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/operational/record.py) | 907 | `dda782d2386ae80081b404f0ef8f36d04399313d` |
| 0103 | [nexent/physics/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/physics/__init__.py) | 189 | `1d22cbb24489bbbbb82ba5a975286e94ce92385f` |
| 0104 | [nexent/physics/core.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/physics/core.py) | 1633 | `7ec0fc8d74570c6eb69ad04922c2363d0dae60dd` |
| 0105 | [nexent/physics/simulation.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/physics/simulation.py) | 482 | `e9aa036dca6f4d09efb0adb34f060ad25b49b04b` |
| 0106 | [nexent/portfolio/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/portfolio/__init__.py) | 249 | `db3bca3ecc103c8641e38a413d2be55c2fa42c92` |
| 0107 | [nexent/portfolio/core.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/portfolio/core.py) | 4754 | `6fd19e79ffb2e6eef87b77a768fd58503199b2f3` |
| 0108 | [nexent/portfolio/simulation.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/portfolio/simulation.py) | 1318 | `4a53d38f4ece25105d6807649c201286e195d434` |
| 0109 | [nexent/proof.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/proof.py) | 1715 | `a64868d7fbaec837b0b7fd9cf5c6a9eb3b18d7fc` |
| 0110 | [nexent/registry.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/registry.py) | 551 | `c0e673d695fef6a8de075eec513aae8a72c9be39` |
| 0111 | [nexent/replay.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/replay.py) | 914 | `2355f49be3dd5c64d9a32367c5289298a47d156b` |
| 0112 | [nexent/repository_genome.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/repository_genome.py) | 3128 | `4d6f81997b22befc65f033f040e03384fbe965a3` |
| 0113 | [nexent/research_loop.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/research_loop.py) | 1854 | `56da90ab5c0bf16269cfe6d2e8571ed54b0859d4` |
| 0114 | [nexent/safety/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/safety/__init__.py) | 307 | `1fed8d568da8e23d3e669273382a8401baa6fc3a` |
| 0115 | [nexent/safety/containment.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/safety/containment.py) | 2939 | `3530da1bab7c636b52fefbffb73401965e903e5f` |
| 0116 | [nexent/system.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/system.py) | 4540 | `61fc183bcef71e89d446b16bf9a5467e438947b2` |
| 0117 | [nexent/van.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/van.py) | 466 | `120fcaeab3222f735f65823eb8ea5dddead4786d` |
| 0118 | [nexent/web/__init__.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/__init__.py) | 383 | `b0a44c8c1fc992aae3050b49e9ab2a1c14606e8e` |
| 0119 | [nexent/web/catalog.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/catalog.py) | 3556 | `91dd3fdee72f985beeade1260244006fca26d24c` |
| 0120 | [nexent/web/genome.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/genome.py) | 5048 | `67e984ce7ee0a76ca6168a1d29c4e6523a014fdc` |
| 0121 | [nexent/web/runtime.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/runtime.py) | 13807 | `9f2014ac88fb38a14d028f057730e2862717ac20` |
| 0122 | [nexent/web/server.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/server.py) | 6715 | `6db11caaf5ed53886462f4894eb54a9c887e697d` |
| 0123 | [nexent/web/source.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/source.py) | 3974 | `3e0c990629cf806f9768b5445e5c2fcad9c383e7` |
| 0124 | [nexent/web/static/app.js](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/static/app.js) | 26503 | `c416b85f908b4739f9b9cc4f438531306b3b3b58` |
| 0125 | [nexent/web/static/federated-index.json](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/static/federated-index.json) | 445667 | `ed70daa72abd38319805362a1ef77beabd7f226b` |
| 0126 | [nexent/web/static/index.html](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/static/index.html) | 13433 | `decb96d5105e89f4cf8a69263b45f39fde818c5c` |
| 0127 | [nexent/web/static/manifest.webmanifest](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/static/manifest.webmanifest) | 222 | `f69cabc9b5edced8e20ad407c53d59ec89d8b3d6` |
| 0128 | [nexent/web/static/style.css](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/static/style.css) | 21592 | `8060e585910e6bfdb5c763743d6f064a05bc9a62` |
| 0129 | [nexent/web/static/sw.js](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/nexent/web/static/sw.js) | 789 | `3511c10e89d33227a05fb34637767436b25be65e` |
| 0130 | [pyproject.toml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/pyproject.toml) | 429 | `97a190d134e4f948f8ebae05fb67be71066ffbde` |
| 0131 | [registry/domains/financial-domain.json](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/registry/domains/financial-domain.json) | 502 | `8801f3ef3cbff870abb884d2ff45c0e31ab4d456` |
| 0132 | [rust/nexent-evidence/Cargo.toml](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/rust/nexent-evidence/Cargo.toml) | 280 | `6760d31b04814d8a64cde656f72d8a7411269115` |
| 0133 | [rust/nexent-evidence/src/bin/evidence_demo.rs](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/rust/nexent-evidence/src/bin/evidence_demo.rs) | 505 | `81a87f34b3017ecc6ce2e170102fd537acf44f96` |
| 0134 | [rust/nexent-evidence/src/lib.rs](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/rust/nexent-evidence/src/lib.rs) | 7303 | `fa22cee1d2da9f627c5e5975d56ea1aa27616567` |
| 0135 | [schemas/financial-research-record.schema.json](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/schemas/financial-research-record.schema.json) | 1204 | `14566daad702a4e753e71c0a596c69f515313b64` |
| 0136 | [tests/test_agents.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_agents.py) | 1168 | `91b2cf2f9c68f91c966b02cce3d0327c49c65cbf` |
| 0137 | [tests/test_architecture_contract.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_architecture_contract.py) | 1176 | `76669955bb055083f23e0ef6c1f315c37b6e4271` |
| 0138 | [tests/test_canonical_languages_archive.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_canonical_languages_archive.py) | 1067 | `c57e92c6826ff7bfb45340425890aca66ec0131d` |
| 0139 | [tests/test_containment.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_containment.py) | 1135 | `10f90476e883849813daea021097cd4a3dac462b` |
| 0140 | [tests/test_e2e_dry_run.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_e2e_dry_run.py) | 959 | `0696228ffb7f312362f8a26ab0a9e52ed2d25b8c` |
| 0141 | [tests/test_end_to_end_linear.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_end_to_end_linear.py) | 1282 | `82c1a4edf9bb14675447f6bf5666767ff0ac98cd` |
| 0142 | [tests/test_engineering.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_engineering.py) | 1275 | `4aad5ed0cb3ada6ba7a468f8ead2217dfdd142b2` |
| 0143 | [tests/test_engineering_coordination.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_engineering_coordination.py) | 1462 | `cdd276baf74efc3d4981a2dd0a2eb01d3f90894c` |
| 0144 | [tests/test_engineering_runtime.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_engineering_runtime.py) | 774 | `1cba4d4d6909cfd2c4738f74d986edae69dd0b13` |
| 0145 | [tests/test_epistemic_kernel.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_epistemic_kernel.py) | 1412 | `894d23da5316a2f89b7750f378d85e3366b61a82` |
| 0146 | [tests/test_external_integration_boundary.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_external_integration_boundary.py) | 530 | `b1c3fd0e7b47308183482f4bf9a812581d933745` |
| 0147 | [tests/test_financial_domain_contract.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_financial_domain_contract.py) | 666 | `0f6c9e253329a5397709805936c0de9f63cfdbae` |
| 0148 | [tests/test_financial_proof.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_financial_proof.py) | 1406 | `9112cdff257f6caeee649f71acc88907c48866c8` |
| 0149 | [tests/test_formal_execution.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_formal_execution.py) | 916 | `f645fce54ab299e37d73471a5f1b2c8363761cd1` |
| 0150 | [tests/test_impact_cone.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_impact_cone.py) | 1070 | `ffd09dedb9d03cb688a6ce72733aeeaf21134979` |
| 0151 | [tests/test_integrated_system.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_integrated_system.py) | 1220 | `a3c46d87252c72724bb35caee29d4885cdfceee5` |
| 0152 | [tests/test_intent_web.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_intent_web.py) | 6708 | `f3fbb0d896073b51a60e079eb34ff7f316366fc4` |
| 0153 | [tests/test_interfaces.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_interfaces.py) | 913 | `44bf5f033e2e5830fa8ad362ab28f0a74167cb5d` |
| 0154 | [tests/test_kernel.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_kernel.py) | 1578 | `1c961295339fab4c3238799f684065ce86bb0771` |
| 0155 | [tests/test_lifecycle.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_lifecycle.py) | 1022 | `c6c338b2c3403328b37277b36674b15a7f44dddb` |
| 0156 | [tests/test_master_layers.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_master_layers.py) | 573 | `44949133f4974e3952f0848a782ac3913cdb3160` |
| 0157 | [tests/test_master_registry.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_master_registry.py) | 1109 | `49d5a4df4183aa64364081a99e236cf48913d9aa` |
| 0158 | [tests/test_missing_system.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_missing_system.py) | 1451 | `abd7324416a8568df4aeb54d5e0746d23fe75391` |
| 0159 | [tests/test_persistence_compiler.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_persistence_compiler.py) | 801 | `41be20a212a91291ad81d31150beccea37875157` |
| 0160 | [tests/test_physics_operational_van.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_physics_operational_van.py) | 657 | `2f88945babca01c7a160b6bebed8c0fe2678c3bb` |
| 0161 | [tests/test_pipeline.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_pipeline.py) | 1077 | `2819af2dd515f90f55d1e90390a476339a95d7bb` |
| 0162 | [tests/test_portfolio.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_portfolio.py) | 1255 | `cb65aa53904391a7c645946378fceaa050892489` |
| 0163 | [tests/test_repository_genome.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_repository_genome.py) | 1226 | `85a86e8107038b8150195b08daf337f0668c6756` |
| 0164 | [tests/test_research_loop.py](https://github.com/fisallllll280-code/NEXENT/blob/f62cf5920174551f9a8f88deb420f9515bedc284/tests/test_research_loop.py) | 895 | `d88375ede9ce5a921559d0306bf4cc4720ba6aaa` |

## 5. تحديث الفهرس والاستعادة

1. اقرأ عقود المستودع وأي AGENTS.md قبل التعديل، وثبّت التزام المصدر.
2. اجلب شجرة Git كاملة مع recursive=1 وارفض نتيجة truncated=true.
3. أعد الجرد بالمسار مع حجم كل ملف وبصمة blob، واحفظ مصدر كل سجل.
4. قارن الإضافات والتغييرات والحذف بالمصدر السابق؛ لا تحذف سجلًا تاريخيًا بصمت.
5. حافظ على أرقام الابتكارات الأصلية، وافصل رقم عرض الملفات عن legacy_id وcanonical_id.
6. احفظ التحديث في فرع مراجعة؛ لا دمج إلى main، ولا تعديل project.genome أو Ω.000 ضمن هذه المهمة.

## 6. الفجوات وحدود الإثبات

- الاستعادة الكاملة لبنود 0001–2750 غير مثبتة؛ لا تُنشأ بنود افتراضية لسد الأرقام.
- RECOVERED وCANONICAL وPROPOSED وIMPLEMENTED وVERIFIED حالات منفصلة؛ الجرد لا يرقّي أيًّا منها.
- فحص هذه المهمة يثبت مطابقة المسارات والبصمات لشجرة المصدر فقط؛ لا اختبارات تشغيلية نُفذت ضمن إنشاء هذا الملف.
