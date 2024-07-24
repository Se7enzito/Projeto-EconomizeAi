function marcarComoPago(button) {
    const nome = button.getAttribute('data-nome');
    fetch('/marcar_pago', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome: nome })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Marcado como pago com sucesso!');
            location.reload();
        } else {
            alert('Erro ao marcar como pago.');
        }
    })
    .catch(error => console.error('Erro:', error));
}