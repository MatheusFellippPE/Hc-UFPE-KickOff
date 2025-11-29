<h1 align="left">📝 Guia de Implantação do MVP</h1>

###

<br clear="both">

<p align="left">Este Guia de Implantação do MVP fornece um passo a passo detalhado e completo para configurar e executar o Sistema Central e Integrado - HC-UFPE (Hub HC-UFPE) do zero em qualquer novo ambiente. O objetivo é permitir a reprodução exata do projeto, cobrindo a criação do ambiente virtual, instalação de dependências, configuração do banco de dados e inicialização do servidor.</p>

###

<h1 align="left">🌐 Tecnologias Utilizadas no Hub HC-UFPE</h1>

###

<p align="left">Front-end: HTML, CSS, JavaScript</p>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-plain-wordmark.svg" height="40" alt="html5 logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-plain-wordmark.svg" height="40" alt="css logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-plain.svg" height="40" alt="javascript logo"  />
</div>

###

<p align="left">Back-end: Python (Django)</p>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain-wordmark.svg" height="40" alt="django logo"  />
</div>

###

<p align="left">Banco de Dados: SQLite3</p>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original-wordmark.svg" height="40" alt="sqlite logo"  />
</div>

###

<h1 align="left">⚙️ Como Rodar o Hub HC-UFPE</h1>

###

<h3 align="left">1. Clone este repositório:</h3>

###

<p align="left">O primeiro passo é obter o código-fonte do projeto para sua máquina local.</p>

###

<h4 align="left">1.1. Clone o Repositório:</h4>

###

<p align="left">Use o comando git clone seguido do URL do repositório para baixar todos os arquivos para uma pasta local.</p>

###

```bash
git clone https://github.com/MatheusFellippPE/Hc-UFPE-KickOff.git
````

###

<h4 align="left">1.2. Acesse a Pasta do Projeto:</h4>

###

<p align="left">Entre no diretório recém-clonado para executar os próximos comandos.</p>

###

```bash
cd Hc-UFPE-KickOff
````

###

<h3 align="left">2. Configuração Inicial e Ambiente Virtual</h3>

###

<p align="left">O primeiro passo é configurar um ambiente virtual para isolar as dependências do projeto e garantir que não haja conflitos com outras instalações do Python.</p>

###

<h4 align="left">2.1. Crie o Ambiente Virtual:</h4>

###

<p align="left">Use o comando abaixo para criar um ambiente virtual chamado .venv na pasta raiz do projeto.</p>

###

```bash
py -m venv .venv
````

###

<p align="left">Nota: Em alguns sistemas, o comando pode ser python -m venv .venv ou, no Linux/macOS, apenas python3 -m venv .venv. Estamos usando py conforme seu comando de referência.</p>

###

<h4 align="left">2.2. Ative o Ambiente Virtual:</h4>

###

<p align="left">Windows(Prompt de Comando):</p>

###

```bash
.venv\Scripts\activate
````

###

<p align="left">ou Windows(PowerShell):</p>

###

```bash 
.venv\Scripts\Activate.ps1
````

###

<p align="left">Linux/macOS:</p>

###

```bash 
source .venv/bin/activate
````

###

<p align="left">Após a execução, você deve ver (.venv) no início da linha de comando, indicando que o ambiente está ativo</p>

###

<h3 align="left">3. Instalação de Dependências</h3>

###

<p align="left">Com o ambiente virtual ativo, você pode instalar as bibliotecas necessárias para o projeto.</p>

###

<h4 align="left">3.1. Atualize o Instalador de Pacotes (pip):</h4>

###

<p align="left">É uma boa prática garantir que o pip (o gerenciador de pacotes do Python) esteja atualizado.</p>

###

```bash 
python -m pip install --upgrade pip
````

###

<h4 align="left">3.2. Instale as Dependências do Projeto:</h4>

###

<p align="left">Instale todas as bibliotecas listadas no arquivo requirements.txt. Este arquivo deve conter todos os pacotes necessários (como Django, Flask, etc.).</p>

###

```bash
pip install -r requirements.txt
````

###

<p align="left">O pip fará o download e a instalação de todos os pacotes listados.</p>

###

<h3 align="left">4. Configuração do Banco de Dados</h3>

###

<p align="left">Assumindo que sua solução utiliza um framework como Django (inferido pelo uso do manage.py), é necessário preparar o banco de dados.</p>

###

<h4 align="left">4.1. Aplique as Migrações do Banco de Dados:</h4>

###

<p align="left">As migrações criam as tabelas e a estrutura do banco de dados (SQLite por padrão, se não for configurado de outra forma) conforme definido nos modelos do seu projeto.</p>

###

```bash
py manage.py migrate
````

###

<p align="left">Este comando inspeciona os arquivos de migração e aplica as mudanças ao banco de dados.</p>

###

<h3 align="left">5. Execução da Solução</h3>

###

<p align="left">O passo final é iniciar o servidor de desenvolvimento para que a solução fique acessível.</p>

###

<h4 align="left">5.1 Inicie o Servidor de Desenvolvimento:</h4>

###

<p align="left">Este comando inicia um servidor web local, que geralmente fica acessível em http://127.0.0.1:8000/.</p>

###

```bash
py manage.py runserver
````

###

<p align="left">Se tudo estiver correto, você verá uma mensagem no terminal indicando que o servidor foi iniciado e a porta em que ele está rodando.</p>

###

<h2 align="left">🚀 Acesso à Solução</h2>

###

<p align="left">Abra seu navegador e navegue até o endereço fornecido pelo comando runserver (geralmente é http://127.0.0.1:8000/) para interagir com o MVP.<br><br>Para parar o servidor, retorne ao terminal onde ele está sendo executado e pressione Ctrl + C.</p>

###

<h1 align="left">👥 Integrantes do Grupo do Projeto Hub HC-UFPE</h1>

###

<h4 align="left">Matheus Fellipp Pinto Soares de Melo Ferreira</h4>

###

<h4 align="left">Mateus Vinicius da Silva Gonçalves</h4>

###

<h4 align="left">Maurilio Santos Silva da Cunha</h4>

###

<h4 align="left">Mariana Freitas de Azevedo</h4>

###

<h4 align="left">Jhonatas Adriano da Silva Leão</h4>

###

<h4 align="left">João Gabriel Brasil de Freitas</h4>

###
