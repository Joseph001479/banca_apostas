document.addEventListener("DOMContentLoaded", function () {
    carregarDados();
});

// Logout
document.getElementById("logout-btn").addEventListener("click", function () {
    alert("Você saiu da sua conta!");
    window.location.href = 'index.html'; // Redireciona para a página de login
});

let saldoTotal = parseFloat(localStorage.getItem("saldo")) || 0;
let apostas = JSON.parse(localStorage.getItem("apostas")) || [];
let labelsGrafico = JSON.parse(localStorage.getItem("labelsGrafico")) || ['Início'];
let saldoGrafico = JSON.parse(localStorage.getItem("saldoGrafico")) || [0];

// Configuração do gráfico com Chart.js
const ctx = document.getElementById('graficoSaldo').getContext('2d');
const graficoSaldo = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labelsGrafico,
        datasets: [{
            label: 'Saldo Total',
            data: saldoGrafico,
            borderColor: '#4caf50',
            backgroundColor: 'rgba(0, 123, 255, 0.2)',
            borderWidth: 2,
            fill: true
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: { title: { display: true, text: 'Tempo' } },
            y: { 
                title: { display: true, text: 'Saldo (R$)' }, 
                min: 0,
                ticks: { beginAtZero: true } 
            }
        }
    }
});

function registrarAposta() {
    let nomeTime = document.getElementById("nomeTime").value.trim();
    let valor = parseFloat(document.getElementById("valorAposta").value);
    let odds = parseFloat(document.getElementById("odds").value);
    let resultado = document.getElementById("resultado").value;

    if (!nomeTime) {
        alert("Por favor, insira o nome do time.");
        return;
    }
    if (isNaN(valor) || isNaN(odds) || valor <= 0 || odds <= 1) {
        alert("Insira valores válidos para aposta e odds!");
        return;
    }

    let ganho = resultado === "win" ? valor * (odds - 1) : -valor;
    saldoTotal += ganho;
    apostas.push({ nomeTime, valor, odds, resultado, ganho });

    // Atualizar armazenamento local
    localStorage.setItem("saldo", saldoTotal.toFixed(2));
    localStorage.setItem("apostas", JSON.stringify(apostas));

    // Atualiza o gráfico
    labelsGrafico.push(`Aposta ${labelsGrafico.length}`);
    saldoGrafico.push(saldoTotal);
    localStorage.setItem("labelsGrafico", JSON.stringify(labelsGrafico));
    localStorage.setItem("saldoGrafico", JSON.stringify(saldoGrafico));
    
    graficoSaldo.update();

    // Atualiza o dashboard
    updateDashboard();
}

function updateDashboard() {
    // Atualiza os valores no HTML
    document.getElementById("saldo").innerText = saldoTotal.toFixed(2);
    let lucroPrejuizo = apostas.reduce((acc, aposta) => acc + aposta.ganho, 0);
    document.getElementById("lucro").innerText = lucroPrejuizo.toFixed(2);
    let investimentoTotal = apostas.reduce((acc, aposta) => acc + aposta.valor, 0);
    let roi = investimentoTotal > 0 ? (lucroPrejuizo / investimentoTotal * 100).toFixed(2) : 0;
    document.getElementById("roi").innerText = `${roi}%`;

    // Atualiza o histórico de apostas
    let lista = document.getElementById("listaApostas");
    lista.innerHTML = "";
    apostas.forEach(aposta => {
        let item = document.createElement("li");
        item.innerText = `Time: ${aposta.nomeTime}, Aposta: R$${aposta.valor}, Odds: ${aposta.odds}, ${aposta.resultado === "win" ? "Vitória" : "Derrota"}, Ganho: R$${aposta.ganho.toFixed(2)}`;
        lista.appendChild(item);
    });
}

function carregarDados() {
    updateDashboard();
}
