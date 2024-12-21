const apiUrl = "https://tumicoin.onrender.com";

async function getChain() {
    try {
        const response = await fetch(`${apiUrl}/chain`);
        const data = await response.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
}

async function addTransaction() {
    try {
        const response = await fetch(`${apiUrl}/add_transaction`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender: "Alice", recipient: "Bob", amount: 10 })
        });
        const data = await response.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
}

async function mineBlock() {
    try {
        const response = await fetch(`${apiUrl}/mine`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ miner_address: "Minero1" })
        });
        const data = await response.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
}

async function getBalance() {
    try {
        const address = document.getElementById('wallet-address').value;
        const response = await fetch(`${apiUrl}/balance/${address}`);
        const data = await response.json();
        document.getElementById('wallet-output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
}
