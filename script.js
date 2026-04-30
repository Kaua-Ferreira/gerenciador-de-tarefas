const BASE_URL = `http://${window.location.hostname}:8000`;
let tempoRestante = 0;
let intervalo = null;
let sessoesHoje = 0;

// --- 1. INICIALIZAÇÃO ---
window.onload = () => {
    const usuarioLogado = localStorage.getItem('usuario');
    if (usuarioLogado) {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('app-content').style.display = 'block';
        document.getElementById('tituloApp').innerText = `Estudos de ${usuarioLogado}`;
        carregar();
    }
};

// --- 2. NAVEGAÇÃO E TEMA ---
function mostrarCadastro() {
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('cadastro-screen').style.display = 'block';
}

function mostrarLogin() {
    document.getElementById('cadastro-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'block';
}

function alternarTema() {
    document.body.classList.toggle('light-mode');
}

// --- 3. LOGIN E CADASTRO ---
async function realizarCadastro() {
    const user = document.getElementById('userCad').value;
    const pass = document.getElementById('passCad').value;
    try {
        const res = await fetch(`${BASE_URL}/cadastro`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "username": user, "password": pass })
        });
        if (res.ok) { alert("Cadastrado! Faça login."); mostrarLogin(); }
        else { const erro = await res.json(); alert("Erro: " + erro.detail); }
    } catch (e) { console.error("Erro na rede:", e); }
}

async function realizarLogin() {
    const username = document.getElementById('userLogin').value;
    const password = document.getElementById('passLogin').value;
    try {
        const res = await fetch(`${BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (res.ok) {
            localStorage.setItem('usuario', username);
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('app-content').style.display = 'block';
            document.getElementById('tituloApp').innerText = `Estudos de ${username}`;
            carregar();
        } else { alert("Usuário ou senha incorretos!"); }
    } catch (e) { console.error(e); }
}

// --- 4. GERENCIAMENTO DE TAREFAS (CRUD) ---
async function carregar() {
    try {
        const res = await fetch(`${BASE_URL}/tarefas`);
        const dados = await res.json();

        const total = dados.length;
        const concluidas = dados.filter(t => t.concluida).length;
        document.getElementById('progress-bar').style.width = (total > 0 ? (concluidas / total) * 100 : 0) + "%";

        document.getElementById('lista').innerHTML = dados.map(t => `
            <li class="${t.concluida ? 'concluida' : ''}">
                <div class="info" onclick="alternar(${t.id})">
                    <strong>${t.nome}</strong>
                    <span class="badge cat-${t.categoria.toLowerCase()}">${t.categoria}</span>
                    <span class="data">${t.data} | ⏳ ${t.tempo}min</span>
                </div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <button type="button" onclick="iniciarFocoTarefa('${t.nome}', ${t.tempo})" style="width: auto; padding: 5px 10px; background: #ff4d4d;">⏱️</button>
                    <span style="cursor:pointer; color:orange;" onclick="editar(${t.id}, '${t.nome}')">✏️</span>
                    <span class="btn-excluir" onclick="excluir(${t.id})">×</span>
                </div>
            </li>
        `).join('');
    } catch (e) { console.error("Erro ao carregar:", e); }
}

async function salvar() {
    const nome = document.getElementById('taskInput').value;
    const categoria = document.getElementById('taskCategory').value;
    const tempo = document.getElementById('focoEstimado').value;
    
    if (!nome) return;

    const res = await fetch(`${BASE_URL}/tarefas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            "nome": nome, 
            "categoria": categoria, 
            "tempo_foco": parseInt(tempo) 
        })
    });

    if (res.ok) {
        document.getElementById('taskInput').value = '';
        carregar();
    }
}

// --- 5. SISTEMA DE FOCO (POMODORO DINÂMICO) ---
function iniciarFocoTarefa(nome, minutos) {
    document.getElementById('painel-foco').style.display = 'block';
    document.getElementById('tarefa-ativa-nome').innerText = `🚀 Focando em: ${nome}`;
    
    tempoRestante = minutos * 60;
    atualizarDisplay(minutos, 0);

    if (intervalo) clearInterval(intervalo);

    intervalo = setInterval(() => {
        tempoRestante--;
        const m = Math.floor(tempoRestante / 60);
        const s = tempoRestante % 60;
        atualizarDisplay(m, s);

        if (tempoRestante <= 0) {
            finalizarFoco();
        }
    }, 1000);
}

function atualizarDisplay(m, s) {
    document.getElementById('timer').innerText = `${m}:${s.toString().padStart(2, '0')}`;
}

// --- FUNÇÃO DO FOGUETINHO ---
function animarFoguete() {
    const foguete = document.createElement('div');
    foguete.innerText = '🚀';
    foguete.style.position = 'fixed';
    foguete.style.bottom = '-100px'; // Começa fora da tela
    foguete.style.left = Math.random() * 80 + 10 + '%'; // Posição aleatória na horizontal
    foguete.style.fontSize = '4rem';
    foguete.style.zIndex = '9999';
    foguete.style.transition = 'transform 2s ease-in'; // Suaviza a subida
    document.body.appendChild(foguete);

    // Pequeno atraso para o CSS perceber a mudança e animar
    setTimeout(() => {
        foguete.style.transform = 'translateY(-120vh)';
    }, 100);

    // Remove o foguete da memória depois que ele some
    setTimeout(() => {
        foguete.remove();
    }, 2500);
}

// --- FINALIZAR FOCO ATUALIZADO ---
function finalizarFoco() {
    clearInterval(intervalo);
    intervalo = null;

    // 1. Toca o som com o volume escolhido na barrinha
    const somAlerta = new Audio('sons/alerta.mp3');
    const volume = document.getElementById('volumeControl').value;
    somAlerta.volume = volume; // Aplica o volume da barrinha
    somAlerta.play();

    // 2. Dispara o foguete
    animarFoguete();

    // 3. Espera 500ms para o som começar antes do Alerta travar tudo
    setTimeout(() => {
        alert("Excelente! Ciclo de foco finalizado.");
        pararFoco();
    }, 500);

    // 4. Contador de sessões
    sessoesHoje++;
    const contador = document.getElementById('sessaoCount');
    if(contador) contador.innerText = sessoesHoje;
}

function pararFoco() {
    clearInterval(intervalo);
    intervalo = null;
    document.getElementById('painel-foco').style.display = 'none';
}

// --- OUTRAS FUNÇÕES ---
async function alternar(id) { await fetch(`${BASE_URL}/tarefas/${id}`, { method: 'PUT' }); carregar(); }
async function editar(id, nomeAntigo) {
    const novoNome = prompt("Editar nome da tarefa:", nomeAntigo);
    if (novoNome && novoNome !== nomeAntigo) {
        await fetch(`${BASE_URL}/tarefas/editar/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "nome": novoNome })
        });
        carregar();
    }
}
async function excluir(id) { if (confirm("Excluir?")) { await fetch(`${BASE_URL}/tarefas/${id}`, { method: 'DELETE' }); carregar(); } }
async function limparTudo() { if (confirm("Limpar tudo?")) { await fetch(`${BASE_URL}/limpar`, { method: 'DELETE' }); carregar(); } }
function sair() { localStorage.removeItem('usuario'); location.reload(); }