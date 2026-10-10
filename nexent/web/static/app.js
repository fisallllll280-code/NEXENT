const state = {
  screen: "overview",
  innovationMode: "operational",
  innovationStatus: "",
  since: 0,
  federation: null,
  health: null,
  runtime: null,
  liveInnovations: [],
  capabilities: {},
  events: [],
  world: null,
  lastProof: null,
  lastRefresh: null,
};
const $ = id => document.getElementById(id);
const SCREEN_META = {
  overview: ["مركز القيادة", "حالة التشغيل منفصلة عن لقطة سجل الابتكارات."],
  indexes: ["أطلس الفهارس", "مناظير الفهرسة وحدود الاستخراج التاريخي."],
  innovations: ["مصنع الابتكارات", "آليات الابتكار وحالاتها وأدلتها المصدرية."],
  runtime: ["التشغيل والأدلة", "قراءة مباشرة من الصحة والحالة والإمكانات وسجل الأحداث."],
  federation: ["اتحاد المستودعات", "تصفح المصادر والمراجعات المثبتة مع إظهار حدود المزامنة."],
};
async function api(path, options) {
  options = options || {};
  const response = await fetch(path, { headers: Object.assign({"Content-Type":"application/json"}, options.headers || {}), ...options });
  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("json") ? await response.json() : await response.text();
  if (!response.ok) throw new Error((data && data.error) || ("HTTP " + response.status + " for " + path));
  return data;
}
function esc(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[ch]));
}
function jsonText(value) { return esc(JSON.stringify(value == null ? {} : value, null, 2)); }
function listMarkup(values, empty) {
  if (!Array.isArray(values) || !values.length) return "<li class=\"muted-list-item\">" + esc(empty || "غير مدوّن في المصدر") + "</li>";
  return values.map(v => "<li>" + esc(typeof v === "string" ? v : JSON.stringify(v)) + "</li>").join("");
}
function safeHref(value) {
  try {
    const url = new URL(value, window.location.href);
    if (url.protocol === "https:" || url.protocol === "http:") return esc(url.href);
  } catch (_) {}
  return "#";
}
function shortSha(value) { return value ? String(value).slice(0,10) : "غير متاح"; }
function showError(error) {
  $("app-alert").hidden = false;
  $("alert-message").textContent = String(error && error.message ? error.message : error);
}
function clearError() { $("app-alert").hidden = true; $("alert-message").textContent = ""; }
function navigate(screen) {
  if (!SCREEN_META[screen]) return;
  state.screen = screen;
  document.querySelectorAll(".screen").forEach(el => el.classList.toggle("active", el.dataset.view === screen));
  document.querySelectorAll(".nav-item").forEach(el => el.classList.toggle("active", el.dataset.screen === screen));
  $("page-title").textContent = SCREEN_META[screen][0];
  $("page-subtitle").textContent = SCREEN_META[screen][1];
  try { window.history.replaceState(null, "", "#" + screen); } catch (_) {}
  renderCurrentScreen();
}
function statusClass(status) {
  if (["IMPLEMENTED","CANONICAL","VERIFIED","IMPLEMENTED_FOUNDATION"].includes(status)) return "status-good";
  if (["CONFLICT","UNKNOWN"].includes(status)) return "status-warning";
  return "status-unknown";
}
function renderOverview() {
  const summary = (state.federation && state.federation.summary) || {};
  const online = Boolean(state.health && state.health.ok);
  const cards = [
    ["صحة NEXENT", state.health ? (online ? "متصل" : "غير متصل") : "—", (state.health && state.health.service) || "GET /api/health", online ? "good" : "neutral", "◉"],
    ["مناظير zero-loss", summary.zero_loss_index_view_count || "—", "تصنيف الفهارس المحدد", "cyan", "▦"],
    ["سجلات الابتكار", summary.operational_innovation_record_count || "—", "السجل التشغيلي التفصيلي", "violet", "✳"],
    ["الإمكانات", Object.keys(state.capabilities || {}).length || "—", "من /api/capabilities", "amber", "◇"],
  ];
  $("overview-metrics").innerHTML = cards.map(c => "<article class=\"metric-card tone-" + c[3] + "\"><div class=\"metric-top\"><span>" + esc(c[0]) + "</span><i>" + c[4] + "</i></div><strong>" + esc(c[1]) + "</strong><small>" + esc(c[2]) + "</small></article>").join("");
  $("runtime-status-label").className = "status-pill " + (state.health ? (online ? "status-good" : "status-warning") : "");
  $("runtime-status-label").textContent = state.health ? (online ? "الخدمة متاحة" : "الخدمة غير متاحة") : "جارٍ الفحص";
  const rt = state.runtime || {};
  const runtimeRows = [["عوالم العمل",rt.web_worlds],["النوايا",rt.intents],["ابتكارات الويب",rt.innovations],["موائم الذكاء",rt.ai_adapter || "غير موصول"]];
  $("runtime-summary").innerHTML = runtimeRows.map(r => "<div class=\"runtime-stat\"><span>" + esc(r[0]) + "</span><strong>" + esc(r[1] == null ? "—" : r[1]) + "</strong></div>").join("");
  $("overview-event-count").textContent = state.events.length + " حديثة";
  $("overview-events").innerHTML = eventMarkup(state.events.slice(-5).reverse(), true);
  $("overview-updated").textContent = state.lastRefresh ? "آخر قراءة " + state.lastRefresh : "بانتظار أول قراءة";
  if (state.world) renderWorld();
}
function renderIndexView() {
  const data = state.federation;
  if (!data) { $("index-view-list").innerHTML = "<div class=\"empty-state\">لم تُحمّل لقطة الفهارس.</div>"; return; }
  const all = data.index_views || [];
  const q = ($("index-search").value || "").trim().toLowerCase();
  const filtered = all.filter(x => [x.name,x.key,x.scope,x.match_mode,x.ordinal].join(" ").toLowerCase().includes(q));
  $("index-result-count").textContent = filtered.length + " من " + all.length + " منظورًا";
  const metrics = [
    ["مناظير محددة",all.length,"00–27"],
    ["مراحل الانتقال",5,"SOURCE → VERIFIED"],
    ["سجلات تشغيلية",data.summary.operational_innovation_record_count,"مرتبطة بمصادر"],
    ["نطاق تاريخي","0001–2750","غير مثبت صفًا بصف"],
  ];
  $("index-metrics").innerHTML = metrics.map(m => "<div class=\"mini-metric\"><span>" + esc(m[0]) + "</span><strong>" + esc(m[1]) + "</strong><small>" + esc(m[2]) + "</small></div>").join("");
  $("index-view-list").innerHTML = filtered.map(x => "<article class=\"index-card\"><div class=\"index-card-head\"><span class=\"ordinal\">Ω." + esc(x.ordinal) + "</span><span class=\"tiny-state\">SCHEMA</span></div><h3>" + esc(x.name) + "</h3><code class=\"index-key\">" + esc(x.key) + "</code><p>" + esc(x.scope) + "</p><div class=\"index-card-foot\"><span>مطابقة: <b>" + esc(x.match_mode) + "</b></span><span>الترقية: <b>" + esc(x.promotion || "لا ترقية آلية") + "</b></span></div></article>").join("") || "<div class=\"empty-state\">لا توجد مناظير تطابق البحث.</div>";
  $("index-snapshot-date").textContent = (data.captured_date || "تاريخ غير متاح") + " · لقطة غير متزامنة تلقائيًا";
  const range = data.summary.historical_legacy_range || {};
  $("legacy-gap").textContent = String(range.start || 1).padStart(4,"0") + "–" + (range.end || 2750) + " · " + (range.state || "UNKNOWN");
}
function fillInnovationStatusOptions() {
  const sel = $("innovation-status-filter");
  if (!sel || !state.federation) return;
  const previous = state.innovationStatus;
  const statuses = Object.keys(state.federation.summary.operational_innovation_status_counts || {}).sort();
  sel.innerHTML = '<option value="">كل الحالات</option>' + statuses.map(s => '<option value="' + esc(s) + '">' + esc(s) + "</option>").join("");
  sel.value = statuses.includes(previous) ? previous : "";
  state.innovationStatus = sel.value;
}
function innovationDataset() {
  const data = state.federation || {};
  if (state.innovationMode === "master") return (data.master_innovations || []).map(x => Object.assign({_kind:"master"},x));
  if (state.innovationMode === "primitives") return (data.vx_invention_primitives.items || []).map(x => Object.assign({_kind:"primitive"},x));
  if (state.innovationMode === "web") return (data.nexent_web_innovations || []).map(x => Object.assign({_kind:"web"},x));
  return (data.operational_innovations || []).map(x => Object.assign({_kind:"operational"},x));
}
function renderInnovations() {
  const data = state.federation;
  if (!data) { $("innovation-list").innerHTML = "<div class=\"empty-state\">لم تُحمّل لقطة الابتكارات.</div>"; return; }
  const s = data.summary;
  const metrics = [
    ["تفاصيل تشغيلية",s.operational_innovation_record_count,"حالات مصدرية محفوظة"],
    ["الفهرس الرئيسي",s.master_index_named_innovation_count,"ليست إثبات تنفيذ"],
    ["تحتاج مراجعة يدوية",s.operational_records_requiring_manual_review,"سجلًا"],
    ["تعارضات مصدريّة",s.operational_innovation_status_counts.CONFLICT || 0,"لا تحسم تلقائيًا"],
  ];
  $("innovation-metrics").innerHTML = metrics.map(m => "<div class=\"mini-metric\"><span>" + esc(m[0]) + "</span><strong>" + esc(m[1]) + "</strong><small>" + esc(m[2]) + "</small></div>").join("");
  $("tab-operational-count").textContent = s.operational_innovation_record_count;
  $("tab-master-count").textContent = s.master_index_named_innovation_count;
  $("tab-primitives-count").textContent = s.vx_invention_primitive_count;
  $("tab-web-count").textContent = s.nexent_web_foundation_innovation_count;
  document.querySelectorAll(".mode-tab").forEach(el => el.classList.toggle("active",el.dataset.innovationMode === state.innovationMode));
  $("innovation-status-filter").hidden = state.innovationMode !== "operational";
  const query = ($("innovation-search").value || "").trim().toLowerCase();
  let items = innovationDataset();
  if (state.innovationMode === "operational" && state.innovationStatus) items = items.filter(x => x.status === state.innovationStatus);
  if (query) items = items.filter(x => JSON.stringify(x).toLowerCase().includes(query));
  $("innovation-result-count").textContent = items.length + " سجل";
  if (state.innovationMode === "master") {
    $("innovation-list").innerHTML = items.map(x => '<article class="master-row"><span class="master-ordinal">' + String(x.ordinal).padStart(2,"0") + '</span><div><strong>' + esc(x.name) + '</strong><small>' + esc(x.family) + '</small></div><span class="master-tag">SOURCE-DERIVED</span></article>').join("") || '<div class="empty-state">لا توجد نتائج.</div>';
    return;
  }
  if (state.innovationMode === "primitives") {
    $("innovation-list").innerHTML = items.map(x => '<article class="innovation-card"><div class="record-head"><span class="record-id">' + esc(x.id) + '</span><span class="status-pill status-good">CATALOG</span></div><h3>' + esc(x.id.replace(/_/g," ")) + '</h3><p>' + esc(x.description) + '</p><div class="domain-tags">' + (x.domains || []).map(d => "<span>" + esc(d) + "</span>").join("") + '</div><small class="muted">النوع: ' + esc(x.type) + '</small></article>').join("") || '<div class="empty-state">لا توجد نتائج.</div>';
    return;
  }
  if (state.innovationMode === "web") {
    $("innovation-list").innerHTML = items.map(x => '<article class="innovation-card"><div class="record-head"><span class="record-id">' + esc(x.id) + '</span><span class="status-pill status-good">' + esc(x.status) + '</span></div><h3>' + esc(x.name) + '</h3><p>' + esc(x.purpose) + '</p><details><summary>مراجع التنفيذ والتحقق</summary><div class="detail-columns"><div><b>المراجع البرمجية</b><ul>' + listMarkup(x.implementation) + '</ul></div><div><b>الاختبارات</b><ul>' + listMarkup(x.verification) + '</ul></div></div></details></article>').join("") || '<div class="empty-state">لا توجد نتائج.</div>';
    return;
  }
  $("innovation-list").innerHTML = items.map(x => {
    const sources = (x.source_refs || []).map(ref => '<li><a href="' + safeHref("https://github.com/fisallllll280-code/VAIXLNS/blob/main/" + ref) + '" target="_blank" rel="noopener noreferrer">' + esc(ref) + "</a></li>").join("") || "<li>غير مدوّن</li>";
    return '<article class="innovation-card"><div class="record-head"><span class="record-id">' + esc(x.canonical_id) + '</span><span class="status-pill ' + statusClass(x.status) + '">' + esc(x.status) + '</span></div><h3>' + esc(x.name) + '</h3><p class="innovation-description">' + esc(x.description || "لا يوجد وصف صريح في المصدر.") + '</p><div class="innovation-meta"><span>' + esc(x.family || "غير مصنف") + '</span><span>المالك: ' + esc(x.owner || "غير محسوم") + '</span><span>جودة الوصف: ' + esc(x.profile_quality || "غير مسجل") + '</span></div>' + (x.status_disagreement ? '<div class="conflict-note">⚠ اختلاف بين حالات المصادر</div>' : "") + '<details><summary>فتح الآلية والأدلة والحدود</summary><div class="detail-columns"><div><b>آلية التشغيل</b><ol>' + listMarkup(x.operating_mechanism) + '</ol></div><div><b>المدخلات</b><ul>' + listMarkup(x.inputs) + '</ul><b>المخرجات</b><ul>' + listMarkup(x.outputs) + '</ul></div><div><b>بوابات القبول</b><ul>' + listMarkup(x.admission_gates) + '</ul><b>أنماط الفشل</b><ul>' + listMarkup(x.failure_modes) + '</ul></div><div><b>المصادر</b><ul>' + sources + '</ul><b>حالات المصدر</b><ul>' + listMarkup(x.source_statuses) + '</ul><b>أدلة مسجلة</b><ul>' + listMarkup(x.evidence_refs) + '</ul></div></div><div class="record-foot"><span>Canonical promotion: <strong>' + (x.canonical_promotion_allowed === true ? "YES" : "NO") + '</strong></span><span>Manual review: <strong>' + (x.review_required ? "REQUIRED" : "not flagged") + "</strong></span></div></details></article>";
  }).join("") || '<div class="empty-state">لا توجد سجلات مطابقة.</div>';
}
function eventMarkup(events, compact) {
  if (!events || !events.length) return '<div class="empty-state">لا توجد أحداث جديدة في السجل.</div>';
  return events.map(event => '<div class="event-row ' + (compact ? "compact" : "") + '"><span class="event-seq">#' + esc(event.seq == null ? "?" : event.seq) + '</span><div class="event-main"><strong>' + esc(event.type || "EVENT") + '</strong><small>' + esc(event.target || event.entity || event.actor || "runtime") + '</small></div><code>' + esc(JSON.stringify(event.payload || {})) + "</code></div>").join("");
}
function renderRuntime() {
  const status = state.runtime || {};
  const metrics = [
    ["صحة الخدمة",state.health ? (state.health.ok ? "ONLINE" : "OFFLINE") : "UNKNOWN","nexent-web"],
    ["عوالم العمل",status.web_worlds == null ? "—" : status.web_worlds,"runtime"],
    ["أحداث مستلمة",state.events.length,"live event feed"],
    ["الإمكانات",Object.keys(state.capabilities || {}).length,"عقود معروضة"],
  ];
  $("runtime-metrics").innerHTML = metrics.map(m => '<article class="metric-card tone-cyan"><div class="metric-top"><span>' + esc(m[0]) + '</span><i>◈</i></div><strong>' + esc(m[1]) + '</strong><small>' + esc(m[2]) + "</small></article>").join("");
  $("runtime-json").textContent = JSON.stringify(status,null,2);
  const caps = Object.entries(state.capabilities || {});
  $("capability-count").textContent = caps.length;
  $("capability-list").innerHTML = caps.map(entry => '<article class="capability-item"><div><strong>' + esc(entry[0]) + '</strong><span class="tiny-state">v' + esc(entry[1].version || "?") + '</span></div><p>' + esc(entry[1].description || "No description supplied") + '</p><small>' + esc(JSON.stringify(entry[1].constraints || {})) + "</small></article>").join("") || '<div class="empty-state">لم تُرجع الواجهة أي إمكانات.</div>';
  $("runtime-events").innerHTML = eventMarkup(state.events.slice().reverse(), false);
  $("runtime-event-head").textContent = state.runtime ? String(state.runtime.events == null ? state.events.length : state.runtime.events) + " متاح" : state.events.length + " حدث";
  $("runtime-refresh-time").textContent = state.lastRefresh ? "آخر تحقق: " + state.lastRefresh : "بانتظار القراءة";
  if (state.lastProof) {
    $("proof-state").className = "status-pill " + (state.lastProof.result && state.lastProof.result.status === "COMPLETED" ? "status-good" : "status-warning");
    $("proof-state").textContent = (state.lastProof.result && state.lastProof.result.status) || "نتيجة موجودة";
    $("proof-detail").textContent = JSON.stringify(state.lastProof,null,2);
  }
}
function renderFederation() {
  const data = state.federation;
  if (!data) return;
  const repos = data.repositories || [];
  const rows = [
    ["مستودعات مرصودة",repos.length,"مراجعات main"],
    ["مراجع وثائق", (data.source_documents || []).length,"روابط مثبتة"],
    ["مراجعة يدوية",data.summary.operational_records_requiring_manual_review,"سجلات الابتكار"],
    ["المزامنة الحية","غير مفعلة","لقطة ثابتة"],
  ];
  $("repository-metrics").innerHTML = rows.map(m => '<div class="mini-metric"><span>' + esc(m[0]) + '</span><strong>' + esc(m[1]) + '</strong><small>' + esc(m[2]) + "</small></div>").join("");
  $("repository-list").innerHTML = repos.map(r => '<article class="repository-card"><div class="repo-heading"><span class="repo-icon">' + esc(r.name.slice(0,2).toUpperCase()) + '</span><span class="tiny-state">SNAPSHOT</span></div><h3>' + esc(r.name) + '</h3><p>' + esc(r.role) + '</p><div class="repo-meta"><span>Commit</span><code>' + esc(shortSha(r.observed_commit_sha)) + '</code></div><div class="repo-meta"><span>تاريخ المراجعة</span><span>' + esc(r.observed_commit_date || "غير متاح") + '</span></div><a class="text-link external-link" href="' + safeHref(r.observed_commit_url || r.repository_url) + '" target="_blank" rel="noopener noreferrer">فتح المستودع ↗</a><details><summary>الملفات التي تمت معاينتها</summary><ul>' + listMarkup(r.inspected_paths) + "</ul></details></article>").join("");
  const docs = data.source_documents || [];
  $("source-document-count").textContent = docs.length + " مرجعًا";
  $("source-document-list").innerHTML = docs.map(d => '<a class="source-row" href="' + safeHref(d.url) + '" target="_blank" rel="noopener noreferrer"><span class="source-doc-icon">↗</span><span class="source-doc-copy"><strong>' + esc(d.path) + '</strong><small>' + esc(d.repository) + " · " + esc(d.purpose) + '</small></span><span class="source-sha">' + esc(shortSha(d.git_blob_sha)) + "</span></a>").join("");
}
function renderWorld() {
  const world = state.world;
  if (!world) return;
  $("world-id").textContent = world.world_id || "—";
  $("world-output").innerHTML = '<div class="world-metrics"><div><strong>' + (world.objects || []).length + '</strong><small>كائنات</small></div><div><strong>' + (world.relations || []).length + '</strong><small>علاقات</small></div><div><strong>' + (world.memory || []).length + '</strong><small>ذاكرة</small></div></div><p class="world-objective">' + esc(world.objective) + '</p><div class="object-grid">' + (world.objects || []).map(o => '<article class="world-object"><strong>' + esc(o.name) + '</strong><small>' + esc(o.object_type) + '</small><p>' + esc(o.meaning) + "</p></article>").join("") + '</div><div class="action-bar"><label class="confirm-check"><input type="checkbox" id="confirm-action"> تأكيد صريح لتنفيذ الإجراء</label><input id="action-input" placeholder="مدخل الإجراء، عند الحاجة…" autocomplete="off"><div class="action-buttons">' + (world.actions || []).map(a => '<button class="button-secondary action-button" data-action="' + esc(a.action_id) + '" title="' + esc(a.description) + '">' + esc(a.name) + "</button>").join("") + "</div></div>";
}
async function createWorld() {
  const objective = $("objective").value.trim();
  if (!objective) throw new Error("اكتب الهدف الهندسي أولًا.");
  let context = {};
  const raw = $("context").value.trim();
  if (raw) {
    context = JSON.parse(raw);
    if (!context || typeof context !== "object" || Array.isArray(context)) throw new Error("السياق يجب أن يكون كائن JSON.");
  }
  const payload = await api("/api/intent", {method:"POST",body:JSON.stringify({objective:objective,context:context})});
  if (!payload.world) throw new Error("لم ينشئ runtime عالمًا؛ راجع نتيجة التنفيذ.");
  state.world = payload.world;
  state.lastProof = payload;
  renderWorld(); renderOverview(); renderRuntime();
  await refreshLive();
}
async function runAction(actionId) {
  if (!state.world || !state.world.world_id) throw new Error("لا يوجد عالم عمل نشط.");
  const input = $("action-input") ? $("action-input").value.trim() : "";
  const confirm = Boolean($("confirm-action") && $("confirm-action").checked);
  const worldId = encodeURIComponent(state.world.world_id);
  const result = await api("/api/world/" + worldId + "/action/" + encodeURIComponent(actionId), {method:"POST",body:JSON.stringify({input:input ? {content:input} : {},confirm:confirm})});
  state.lastProof = result;
  state.world = await api("/api/world/" + worldId);
  renderWorld(); renderRuntime(); renderOverview();
  await refreshLive();
}
function renderCurrentScreen() {
  if (state.screen === "overview") renderOverview();
  else if (state.screen === "indexes") renderIndexView();
  else if (state.screen === "innovations") renderInnovations();
  else if (state.screen === "runtime") renderRuntime();
  else if (state.screen === "federation") renderFederation();
}
async function refreshLive() {
  const responses = await Promise.allSettled([api("/api/health"),api("/api/status"),api("/api/innovations"),api("/api/capabilities"),api("/api/events?since=" + state.since)]);
  const health = responses[0], runtime = responses[1], innovations = responses[2], capabilities = responses[3], events = responses[4];
  if (health.status === "fulfilled") state.health = health.value;
  if (runtime.status === "fulfilled") state.runtime = runtime.value;
  if (innovations.status === "fulfilled") state.liveInnovations = innovations.value.items || [];
  if (capabilities.status === "fulfilled") state.capabilities = capabilities.value;
  if (events.status === "fulfilled") {
    const bySeq = new Map(state.events.map(e => [e.seq,e]));
    (events.value.events || []).forEach(e => bySeq.set(e.seq,e));
    state.events = Array.from(bySeq.values()).sort((a,b)=>(a.seq||0)-(b.seq||0)).slice(-120);
    const latest = Math.max(0,...state.events.map(e=>Number(e.seq)||0));
    state.since = Math.max(state.since,Number(events.value.head)||0,latest);
  }
  state.lastRefresh = new Intl.DateTimeFormat("ar-SA",{hour:"2-digit",minute:"2-digit",second:"2-digit"}).format(new Date());
  const enoughLive = health.status === "fulfilled" && runtime.status === "fulfilled";
  const online = Boolean(state.health && state.health.ok);
  $("health-badge").className = "health-badge " + (online ? "is-online" : (enoughLive ? "is-warning" : ""));
  $("health-badge").innerHTML = "<i></i>" + (online ? "NEXENT متصل" : (enoughLive ? "الحالة غير سليمة" : "تعذر التحقق"));
  $("connection-dot").className = "connection-dot " + (online ? "is-online" : "is-offline");
  $("connection-label").textContent = online ? "runtime متصل" : "runtime غير متحقق";
  $("connection-subtitle").textContent = enoughLive ? "حالة مباشرة محدثة" : "تعذر قراءة جميع واجهات الحالة";
  $("footer-time").textContent = "آخر فحص: " + state.lastRefresh;
  renderCurrentScreen();
  if (state.screen !== "overview") renderOverview();
  if (state.screen !== "runtime") renderRuntime();
  if (state.screen !== "federation") renderFederation();
  if (state.screen !== "indexes") renderIndexView();
  if (state.screen !== "innovations") renderInnovations();
  if (!enoughLive) showError(new Error("تعذر الوصول إلى واجهات runtime؛ بيانات الفهرس تبقى لقطة مصدرية منفصلة."));
  else clearError();
}
async function boot() {
  try {
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
    state.federation = await api("/federated-index.json");
    fillInnovationStatusOptions();
    const requested = window.location.hash.replace(/^#/,"");
    if (SCREEN_META[requested]) state.screen = requested;
    navigate(state.screen);
    await refreshLive();
    window.setInterval(() => refreshLive().catch(showError), 4000);
  } catch (error) {
    showError(error);
    navigate("overview");
  }
}
document.addEventListener("click",event => {
  const screenButton = event.target.closest("[data-screen]");
  if (screenButton) { event.preventDefault(); navigate(screenButton.dataset.screen); return; }
  const modeButton = event.target.closest("[data-innovation-mode]");
  if (modeButton) { state.innovationMode = modeButton.dataset.innovationMode; renderInnovations(); return; }
  const actionButton = event.target.closest("[data-action]");
  if (actionButton) runAction(actionButton.dataset.action).catch(showError);
});
$("refresh-button").addEventListener("click",() => refreshLive().catch(showError));
$("dismiss-alert").addEventListener("click",clearError);
$("start-intent").addEventListener("click",() => createWorld().catch(showError));
$("objective").addEventListener("keydown",event => { if (event.key === "Enter") createWorld().catch(showError); });
$("index-search").addEventListener("input",renderIndexView);
$("innovation-search").addEventListener("input",renderInnovations);
$("innovation-status-filter").addEventListener("change",event => {state.innovationStatus=event.target.value;renderInnovations();});
window.addEventListener("hashchange",() => {const key=window.location.hash.replace(/^#/,"");if(SCREEN_META[key])navigate(key);});
boot();
