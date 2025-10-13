(() => {
  const API_BASE = window.location.origin;
  const $ = (id) => document.getElementById(id);
  const form = $("loginForm");
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
    result.textContent = "Autenticando...";

    const body = new URLSearchParams();
    body.set("username", $("email").value.trim());
    body.set("password", $("password").value);

    try {
      const res = await fetch(`${API_BASE}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body
      });

      const { data, raw } = await parseResponse(res);
      if (!res.ok) {
        const msg = data.detail || data.error || raw || `${res.status} ${res.statusText}`;
        throw new Error(msg);
      }

      result.innerHTML = `
        <p>Login efetuado com sucesso!</p>
        <p><strong>token_type:</strong> ${data.token_type}</p>
        <p><strong>access_token:</strong></p>
        <pre class="code">${data.access_token}</pre>
      `;
    } catch (err) {
      result.innerHTML = `<p style="color:#dc2626">Erro: ${err.message}</p>`;
    }
  });
})();