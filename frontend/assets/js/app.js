const apiUrl = "https://tumicoin.onrender.com";

// Función genérica para manejar solicitudes y errores
async function fetchWithHandling(url, options = {}) {
    try {
        const response = await fetch(url, {
            mode: "cors", // Modo explícito para solicitudes entre dominios
            ...options,
        });
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error en la solicitud:", error);
        document.getElementById('output').innerText = `Error: ${error.message}`;
        throw error;
    }
}

// Obtener la cadena de bloques
async function getChain() {
    const url = `${apiUrl}/chain`;
    const data = await fetchWithHandling(url);
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

// Añadir una nueva transacción
async function addTransaction() {
    const url = `${apiUrl}/add_transaction`;
    const payload = { sender: "Alice", recipient: "Bob", amount: 10 };

    const data = await fetchWithHandling(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

// Minar un nuevo bloque
async function mineBlock() {
    const url = `${apiUrl}/mine`;
    const payload = { miner_address: "Minero1" };

    const data = await fetchWithHandling(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

// Obtener balance de una wallet
async function getBalance() {
    const address = document.getElementById('wallet-address').value.trim();

    if (!address) {
        document.getElementById('wallet-output').innerText = "Por favor, ingresa una dirección válida.";
        return;
    }

    const url = `${apiUrl}/balance/${address}`;
    const data = await fetchWithHandling(url, {
        mode: 'cors',
    });

    document.getElementById('wallet-output').innerText = JSON.stringify(data, null, 2);
}
