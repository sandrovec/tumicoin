// URL de tu backend en Render
const apiUrl = "https://tumicoin-backend.onrender.com";

// Función para obtener la cadena de bloques
async function getChain() {
    try {
        const response = await fetch(`${apiUrl}/chain`);
        const data = await response.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('output').innerText = "Error al obtener la cadena de bloques.";
        console.error(error);
    }
}

// Función para añadir una transacción
async function addTransaction() {
    try {
        const sender = prompt("Ingrese el remitente:");
        const recipient = prompt("Ingrese el destinatario:");
        const amount = parseFloat(prompt("Ingrese el monto:"));

        if (!sender || !recipient || isNaN(amount)) {
            alert("Datos inválidos.");
            return;
        }

        const response = await fetch(`${apiUrl}/add_transaction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sender: sender,
                recipient: recipient,
                amount: amount
            })
        });

        const data = await response.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('output').innerText = "Error al añadir la transacción.";
        console.error(error);
    }
}

// Función para minar un bloque
async function mineBlock() {
    try {
        const minerAddress = prompt("Ingrese la dirección del minero:");

        if (!minerAddress) {
            alert("La dirección del minero es requerida.");
            return;
        }

        const response = await fetch(`${apiUrl}/mine`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ miner_address: minerAddress })
        });

        const data = await response.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('output').innerText = "Error al minar el bloque.";
        console.error(error);
    }
}

// Agrega más funciones aquí, como registrar usuarios, consultar balance, etc.
