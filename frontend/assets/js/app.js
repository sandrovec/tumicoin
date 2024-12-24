const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : 'https://tumicoin.onrender.com';

// Función para mostrar la sección de inicio de sesión
function showLogin() {
    document.getElementById('home-section').classList.add('hidden');
    document.getElementById('register-section').classList.add('hidden');
    document.getElementById('login-section').classList.remove('hidden');
}

// Función para mostrar la sección de registro
function showRegister() {
    document.getElementById('home-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('register-section').classList.remove('hidden');
}

// Función para iniciar sesión
async function login() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        alert("Por favor, ingresa tu correo y contraseña.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.message}`);
            return;
        }

        const data = await response.json();
        localStorage.setItem('token', data.token); // Almacena el token JWT
        alert(data.message);
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('wallet-section').classList.remove('hidden');
        document.getElementById('balance').innerText = data.balance || '0 TumiCoins';
    } catch (error) {
        alert("Ocurrió un error al iniciar sesión. Por favor, intenta nuevamente.");
        console.error(error);
    }
}

// Función para registrar un usuario
async function register() {
    const name = document.getElementById('register-name').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;

    if (!name || !email || !password) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });

        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.message}`);
            return;
        }

        const data = await response.json();
        alert(data.message);
        document.getElementById('register-section').classList.add('hidden');
        document.getElementById('login-section').classList.remove('hidden');
    } catch (error) {
        alert("Ocurrió un error al registrarte. Por favor, intenta nuevamente.");
        console.error(error);
    }
}

// Función para cerrar sesión
function logout() {
    localStorage.removeItem('token');
    document.getElementById('wallet-section').classList.add('hidden');
    document.getElementById('home-section').classList.remove('hidden');
}

// Función para manejar solicitudes con manejo de errores
async function fetchWithHandling(url, options = {}) {
    try {
        const token = localStorage.getItem('token'); // Obtén el token almacenado
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(url, { mode: 'cors', ...options, headers });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || `Error ${response.status}`);
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
    const url = `${API_URL}/chain`;
    try {
        const data = await fetchWithHandling(url);
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        // El mensaje de error ya está manejado en fetchWithHandling
    }
}

// Añadir una nueva transacción
async function addTransaction() {
    const url = `${API_URL}/add_transaction`;
    const payload = { sender: "Alice", recipient: "Bob", amount: 10 };

    try {
        const data = await fetchWithHandling(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        // El mensaje de error ya está manejado en fetchWithHandling
    }
}

// Minar un nuevo bloque
async function mineBlock() {
    const url = `${API_URL}/mine`;
    const payload = { miner_address: "Minero1" };

    try {
        const data = await fetchWithHandling(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        // El mensaje de error ya está manejado en fetchWithHandling
    }
}

// Obtener balance de una wallet (si tienes un input para esto)
async function getBalance() {
    const address = document.getElementById('wallet-address').value.trim();

    if (!address) {
        document.getElementById('wallet-output').innerText = "Por favor, ingresa una dirección válida.";
        return;
    }

    const url = `${API_URL}/balance/${address}`;
    try {
        const data = await fetchWithHandling(url, {
            mode: 'cors',
        });

        document.getElementById('wallet-output').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        // El mensaje de error ya está manejado en fetchWithHandling
    }
}
