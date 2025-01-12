import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("https://tumicoin.onrender.com/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        alert("Usuario registrado exitosamente");
        navigate("/login");
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      console.error("Error en el registro:", err);
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <form className="bg-white p-8 rounded-lg shadow-md" onSubmit={handleSubmit}>
        <h2 className="text-2xl font-bold text-yellow-600 mb-4">Registrarse</h2>
        <input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 w-full mb-4"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 w-full mb-4"
        />
        <button
          type="submit"
          className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-500 w-full"
        >
          Registrarse
        </button>
      </form>
    </div>
  );
}

export default Register;