async function generarPassword() {
    const longitud = parseInt(document.getElementById('longitud').value);
    const mayusculas = document.getElementById('mayusculas').checked;
    const numeros = document.getElementById('numeros').checked;
    const simbolos = document.getElementById('simbolos').checked;

    const response = await fetch('/generar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ longitud, mayusculas, numeros, simbolos })
    });

    const resultadoDiv = document.getElementById('resultado');

    if (response.ok) {
        const data = await response.json();
        resultadoDiv.textContent = data.password;
    } else {
        const error = await response.json();
        resultadoDiv.textContent = "Error: " + error.error;
    }
}
