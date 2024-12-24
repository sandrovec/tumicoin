// Determinar la URL de la API
const API_URL = 'https://tumicoin.onrender.com';


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
        localStorage.setItem('token', data.token);
        alert(data.message);
        showWallet(data.balance);
    } catch (error) {
        alert("Ocurrió un error al iniciar sesión.");
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
        showLogin();
    } catch (error) {
        alert("Ocurrió un error al registrarte.");
        console.error(error);
    }
}

// Función para regresar a la página inicial
function goHome() {
    document.getElementById('home-section').classList.remove('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('register-section').classList.add('hidden');
}

// Función para mostrar la wallet
function showWallet(balance = '0 TumiCoins') {
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('wallet-section').classList.remove('hidden');
    document.getElementById('balance').innerText = balance;
}

// Función para cerrar sesión
function logout() {
    localStorage.removeItem('token');
    document.getElementById('wallet-section').classList.add('hidden');
    document.getElementById('home-section').classList.remove('hidden');
}
