const btnTema = document.getElementById('btnTema');
const iconeTema = document.getElementById('iconeTema');
const htmlElement = document.documentElement;

// Função para atualizar o ícone visualmente
function atualizarInterface(tema) {
    if (tema === 'dark') {
        iconeTema.classList.replace('bi-moon-stars-fill', 'bi-sun-fill');
        btnTema.classList.replace('btn-outline-dark', 'btn-outline-light');
    } else {
        iconeTema.classList.replace('bi-sun-fill', 'bi-moon-stars-fill');
        btnTema.classList.replace('btn-outline-light', 'btn-outline-dark');
    }
}

const temaSalvo = localStorage.getItem('theme') || 'light';
htmlElement.setAttribute('data-bs-theme', temaSalvo);
atualizarInterface(temaSalvo);

btnTema.addEventListener('click', () => {
    const temaAtual = htmlElement.getAttribute('data-bs-theme');
    const novoTema = temaAtual === 'dark' ? 'light' : 'dark';

    htmlElement.setAttribute('data-bs-theme', novoTema);
    localStorage.setItem('theme', novoTema);
    atualizarInterface(novoTema);
});
