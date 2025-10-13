(() => {
  const API_BASE = window.location.origin;
  const form = document.getElementById("registerForm");
  const result = document.getElementById("result");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    result.textContent = "Registrando...";

    const payload = {
      email: document.getElementById("email").value.trim(),
      password: document.getElementById("password").value,
      password_confirmation: document.getElementById("password_confirmation").value,
      user_type: document.getElementById("user_type").value,
    };

    try {
      const res = await fetch(`${API_BASE}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) {
        const msg = Array.isArray(data.detail)
          ? data.detail.map(d => d.msg || d.detail).join(", ")
          : (data.detail || "Falha no cadastro");
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