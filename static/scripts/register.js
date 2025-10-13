(() => {
  const API_BASE = window.location.origin;
  const $ = (id) => document.getElementById(id);
  const form = $("registerForm");
  const result = $("result");
  if (!form) return;

  const elPw = $("password");
  const elPc = $("password_confirmation");
  const btnSubmit = form.querySelector("button[type='submit']");
  const reqItems = [...document.querySelectorAll("#pwReqList .req")];
  const meter = $("pwMeter");
  const meterBar = meter?.querySelector(".pw-meter__bar");

  function check(pw, pc) {
    return {
      len: pw.length >= 6 && pw.length <= 8,
      lower: /[a-z]/.test(pw),
      upper: /[A-Z]/.test(pw),
      digit: /\d/.test(pw),
      special: /[^A-Za-z0-9]/.test(pw),
      space: !/\s/.test(pw),
      match: pw.length > 0 && pw === pc,
    };
  }

  function strength(state) {
    // força baseada em 5 requisitos principais (ignora "match" e "space" já avaliados)
    const keys = ["len", "lower", "upper", "digit", "special"];
    const score = keys.reduce((acc, k) => acc + (state[k] ? 1 : 0), 0);
    return score; // 0..5
  }

  function renderRules(state) {
    reqItems.forEach(el => {
      const key = el.getAttribute("data-key");
      const ok = !!state[key];
      el.classList.toggle("req--ok", ok);
      el.classList.toggle("req--bad", !ok);
    });

    const s = strength(state);
    if (meter && meterBar) {
      const pct = [0, 20, 40, 60, 80, 100][s];
      meterBar.style.width = `${pct}%`;
      meter.classList.toggle("is-medium", s >= 3 && s <= 4);
      meter.classList.toggle("is-strong", s >= 5);
      if (s <= 2) { meter.classList.remove("is-medium", "is-strong"); }
    }

    // Habilita submit só quando todas as regras (incluindo match/space) estão OK
    const allOk = Object.values(state).every(Boolean);
    if (btnSubmit) btnSubmit.disabled = !allOk;
  }

  function update() {
    const state = check(elPw.value, elPc.value);
    renderRules(state);
  }

  elPw.addEventListener("input", update);
  elPc.addEventListener("input", update);
  update(); // estado inicial

  function setAlert(type, html) {
    const cls = type === "success" ? "alert alert--success" : "alert alert--error";
    result.innerHTML = `<div class="${cls}">${html}</div>`;
  }

  async function parseResponse(res) {
    const ct = res.headers.get("content-type") || "";
    const text = await res.text();
    if (ct.includes("application/json")) {
      try { return { data: JSON.parse(text), raw: text }; }
      catch { return { data: { detail: text }, raw: text }; }
    }
    return { data: { detail: text }, raw: text };
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setAlert("success", "Enviando...");

    const payload = {
      email: $("email").value.trim(),
      password: elPw.value,
      password_confirmation: elPc.value,
      user_type: $("user_type") ? $("user_type").value : undefined,
    };

    try {
      const res = await fetch(`${API_BASE}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const { data, raw } = await parseResponse(res);
      if (!res.ok) {
        const reqs = data?.password_requirements;
        const msg = Array.isArray(reqs)
          ? `A senha deve atender: ${reqs.join(", ")}`
          : (Array.isArray(data?.detail)
              ? data.detail.map(d => d.msg || d.detail).join(", ")
              : (data?.detail || data?.error || raw || `${res.status} ${res.statusText}`));
        setAlert("error", `<strong>Erro:</strong> ${msg}`);
        return;
      }

      setAlert("success", `<strong>Usuário criado com sucesso!</strong>`);
    } catch (err) {
      setAlert("error", `<strong>Erro:</strong> ${err.message}`);
    }
  });
})();