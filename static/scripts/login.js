(() => {
  const API_BASE = window.location.origin;
  const form = document.getElementById("loginForm");
  const result = document.getElementById("result");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    result.textContent = "Autenticando...";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const body = new URLSearchParams();
    body.append("username", email);
    body.append("password", password);

    try {
      const res = await fetch(`${API_BASE}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Falha no login");

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