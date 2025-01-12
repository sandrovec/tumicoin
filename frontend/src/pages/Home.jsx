import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center text-center">
      <h1 className="text-4xl font-bold text-yellow-600">Bienvenido a TumiCoin</h1>
      <p className="mt-4 text-lg text-gray-700">
        La <span className="font-bold text-yellow-600">criptomoneda peruana</span> que transforma la economía.
      </p>
      <div className="mt-6 space-x-4">
        <Link to="/login">
          <button className="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-500">
            Iniciar Sesión
          </button>
        </Link>
        <Link to="/register">
          <button className="bg-gray-700 text-white px-6 py-2 rounded-lg hover:bg-gray-600">
            Registrarse
          </button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
