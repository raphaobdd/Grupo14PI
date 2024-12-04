document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('empresaForm');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        // Obtém o nome da empresa
        const nomeEmpresa = document.getElementById('empresa').value.trim();

        if (nomeEmpresa === '') {
            alert('Por favor, insira um nome para a empresa.');
            return;
        }

        // Salva o nome no localStorage
        localStorage.setItem('nomeEmpresa', nomeEmpresa);

        // Redireciona para outra página (ajuste conforme necessário)
        window.location.href = "index.html";
    });
});
