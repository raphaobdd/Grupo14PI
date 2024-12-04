document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Impede o envio padrão do formulário (não recarrega a página)
    
    // Exibe o alerta de sucesso
    alert('Mensagem enviada com sucesso!');
    
    // Opcional: Limpa os campos do formulário após o envio
    document.getElementById('contactForm').reset();

    // Redireciona para a página principal após 1 segundo (1000 milissegundos)
    setTimeout(function() {
        window.location.href = "./searchPage.html"; // Redireciona para a página principal
    }, 1000); // Espera 1 segundo antes de redirecionar
});
