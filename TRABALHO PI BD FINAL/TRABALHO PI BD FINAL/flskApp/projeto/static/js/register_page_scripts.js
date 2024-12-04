document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", (event) => {
        // Limpa a mensagem de erro
        errorMessage.textContent = "";
        errorMessage.style.display = "none";

        // Coleta os valores dos campos
        const nome = document.getElementById("nome").value.trim();
        const email = document.getElementById("email").value.trim();
        const senha = document.getElementById("senha").value.trim();
        const confirmarSenha = document.getElementById("confirmar_senha").value.trim();

        // Validação básica
        if (!nome || !email || !senha || !confirmarSenha) {
            event.preventDefault();
            errorMessage.textContent = "Por favor, preencha todos os campos.";
            errorMessage.style.display = "block";
            return;
        }

        // Verificar se as senhas coincidem
        if (senha !== confirmarSenha) {
            event.preventDefault();
            errorMessage.textContent = "As senhas não coincidem.";
            errorMessage.style.display = "block";
            return;
        }

        // Se todas as validações forem aprovadas, o formulário será enviado
        alert("Cadastro realizado com sucesso!");
    });
});
