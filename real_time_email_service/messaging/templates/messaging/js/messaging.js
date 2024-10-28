function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Verifica se este cookie é o que estamos procurando
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function sendMessage(recipient, title, body) {
    const token = getCookie('jwtToken'); // Obtém o token do cookie

    const response = await fetch('/send/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // usar token aqui
        },
        body: JSON.stringify({
            recipient: recipient,
            title: title,
            body: body
        })
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Mensagem enviada:', data);
    } else {
        console.error('Erro ao enviar mensagem:', response.statusText);
    }
}

document.getElementById('message-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o envio padrão do formulário
    const recipient = document.getElementById('recipient').value;
    const title = document.getElementById('title').value;
    const body = document.getElementById('body').value;

    sendMessage(recipient, title, body); // Chama a função para enviar a mensagem
});
