(() => {
  const API_BASE = window.location.origin;
  const $ = (id) => document.getElementById(id);
  const form = $("registerForm");
  const result = $("result");
  if (!form) return;

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
    result.textContent = "Registrando...";

    const payload = {
      email: $("email").value.trim(),
      password: $("password").value,
      password_confirmation: $("password_confirmation").value,
      user_type: $("user_type").value,
    };

    try {
      const res = await fetch(`${API_BASE}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const { data, raw } = await parseResponse(res);
      if (!res.ok) {
        const msg = Array.isArray(data.detail)
          ? data.detail.map(d => d.msg || d.detail).join(", ")
          : (data.detail || data.error || raw || `${res.status} ${res.statusText}`);
        throw new Error(msg);
      }

      result.innerHTML = `
        <p>Usuário criado com sucesso!</p>
        <pre class="code">${JSON.stringify(data, null, 2)}</pre>
      `;
    } catch (err) {
      result.innerHTML = `<p style="color:#dc2626">Erro: ${err.message}</p>`;
    }
  });
})();