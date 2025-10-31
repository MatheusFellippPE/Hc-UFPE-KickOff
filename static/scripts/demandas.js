let usuario = null;

async function carregarUsuario() {
  const res = await fetch('/api/me');
  if (!res.ok) throw new Error('Falha ao obter usuário.');
  usuario = await res.json();
}

function criarItem(d) {
  const li = document.createElement('li');

  const header = document.createElement('div');
  header.style.cursor = 'pointer';

  const img = document.createElement('img');
  img.src = d.userPhotoUrl || 'https://via.placeholder.com/48';
  img.alt = 'foto de perfil';
  img.width = 32;
  img.height = 32;

  const spanAutor = document.createElement('span');
  spanAutor.textContent = ` ${d.userName} - ${d.userTitle} | `;

  const spanTitulo = document.createElement('strong');
  spanTitulo.textContent = d.titulo + ' | ';

  const spanStatus = document.createElement('em');
  spanStatus.textContent = d.status;

  header.appendChild(img);
  header.appendChild(spanAutor);
  header.appendChild(spanTitulo);
  header.appendChild(spanStatus);

  const desc = document.createElement('div');
  desc.textContent = d.descricao;
  desc.style.display = 'none';
  desc.style.whiteSpace = 'pre-wrap';

  header.addEventListener('click', () => {
    desc.style.display = desc.style.display === 'none' ? 'block' : 'none';
  });

  li.appendChild(header);
  li.appendChild(desc);
  return li;
}

async function carregarDemandas() {
  const ul = document.getElementById('listaDemandas');
  ul.innerHTML = '';
  const res = await fetch('/api/demandas');
  if (!res.ok) {
    ul.textContent = 'Erro ao carregar demandas.';
    return;
  }
  const demandas = await res.json();
  if (!demandas.length) {
    ul.textContent = 'Nenhuma demanda cadastrada.';
    return;
  }
  demandas.forEach(d => ul.appendChild(criarItem(d)));
}

async function salvarDemanda(payload) {
  const res = await fetch('/api/demandas', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Falha ao salvar.');
  }
  return res.json();
}

document.getElementById('btnNova').addEventListener('click', () => {
  document.getElementById('formDemanda').style.display = 'block';
  document.getElementById('titulo').focus();
});

document.getElementById('btnCancelar').addEventListener('click', () => {
  document.getElementById('formDemanda').reset();
  document.getElementById('formDemanda').style.display = 'none';
});

document.getElementById('formDemanda').addEventListener('submit', async (e) => {
  e.preventDefault();
  const titulo = document.getElementById('titulo').value.trim();
  const descricao = document.getElementById('descricao').value.trim();
  const status = document.getElementById('status').value;

  if (!titulo || !descricao || !status) return;

  try {
    await salvarDemanda({ titulo, descricao, status });
    document.getElementById('formDemanda').reset();
    document.getElementById('formDemanda').style.display = 'none';
    await carregarDemandas();
  } catch (err) {
    alert(err.message || 'Erro ao salvar demanda.');
  }
});

(async function init() {
  try {
    await carregarUsuario();
    await carregarDemandas();
  } catch (e) {
    document.getElementById('listaDemandas').textContent = 'Erro ao iniciar a página.';
  }
})();
