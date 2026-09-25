const state = { worldId: null, since: 0 };

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "request failed");
  return data;
}

function renderWorld(world) {
  state.worldId = world.world_id;
  $("world-id").textContent = world.world_id;
  $("action-count").textContent = world.actions.length;
  $("world").innerHTML = `
    <div class="world-meta">
      <div class="metric"><strong>${world.objects.length}</strong><span>objects</span></div>
      <div class="metric"><strong>${world.relations.length}</strong><span>relations</span></div>
      <div class="metric"><strong>${world.memory.length}</strong><span>memory entries</span></div>
    </div>
    <p><b>${escapeHtml(world.objective)}</b></p>
    <div class="objects">
      ${world.objects.map(obj => `
        <div class="object">
          <b>${escapeHtml(obj.name)}</b>
          <small>${escapeHtml(obj.object_type)}</small>
          <div>${escapeHtml(obj.meaning)}</div>
        </div>`).join("")}
    </div>
  `;

  $("actions").innerHTML = world.actions.map(action => `
    <button class="action-btn" data-action="${action.action_id}" title="${escapeHtml(action.description)}">
      ${escapeHtml(action.name)}
    </button>`).join("");
  document.querySelectorAll(".action-btn").forEach(btn => {
    btn.addEventListener("click", () => runAction(btn.dataset.action));
  });
}

function renderProof(payload) {
  $("proof-state").textContent = payload?.result?.status || "waiting";
  $("proof").textContent = JSON.stringify(payload, null, 2);
}

function renderEvents(events) {
  if (!events.length) return;
  state.since = Math.max(state.since, ...events.map(e => e.seq));
  $("event-count").textContent = state.since;
  const rows = events.slice().reverse().map(e => `
    <div class="event">
      <span class="seq">#${e.seq}</span>
      <span class="type">${escapeHtml(e.type)}</span>
      <span class="payload">${escapeHtml(JSON.stringify(e.payload))}</span>
    </div>`).join("");
  $("events").insertAdjacentHTML("afterbegin", rows);
  while ($("events").children.length > 80) $("events").lastElementChild.remove();
}

async function createWorld() {
  const objective = $("objective").value.trim();
  if (!objective) return;
  let context = {};
  const raw = $("context").value.trim();
  if (raw) context = JSON.parse(raw);
  const data = await api("/api/intent", {
    method: "POST",
    body: JSON.stringify({ objective, context }),
  });
  renderWorld(data.world);
  renderProof(data);
  await refreshEvents();
}

async function runAction(actionId) {
  if (!state.worldId) return;
  const input = $("action-input").value.trim();
  const payload = {
    input: input ? { content: input } : {},
    confirm: $("confirm").checked,
  };
  const data = await api(`/api/world/${state.worldId}/action/${actionId}`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
  renderProof(data);
  const world = await api(`/api/world/${state.worldId}`);
  renderWorld(world);
  await refreshEvents();
}

async function refreshEvents() {
  const data = await api(`/api/events?since=${state.since}`);
  renderEvents(data.events || []);
}

async function boot() {
  try {
    const health = await api("/api/health");
    $("health").textContent = health.ok ? "online" : "offline";
    const innovations = await api("/api/innovations");
    $("innovations").textContent = `${innovations.count} web innovations registered`;
    await refreshEvents();
    setInterval(refreshEvents, 1800);
  } catch (error) {
    $("health").textContent = "error";
    console.error(error);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[ch]));
}

$("run-intent").addEventListener("click", () => createWorld().catch(showError));
$("objective").addEventListener("keydown", e => {
  if (e.key === "Enter") createWorld().catch(showError);
});
boot();

function showError(error) {
  $("proof-state").textContent = "error";
  $("proof").textContent = String(error);
}
