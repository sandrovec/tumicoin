import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Wallet() {
  const [balance, setBalance] = useState("0 TumiCoins");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBalance = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }
      try {
        const response = await fetch("https://tumicoin.onrender.com/balance/myAddress", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          const data = await response.json();
          setBalance(`${data.balance} TumiCoins`);
        } else {
          navigate("/login");
        }
      } catch (err) {
        console.error("Error obteniendo balance:", err);
        navigate("/login");
      }
    };

    fetchBalance();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md text-center">
        <h2 className="text-2xl font-bold text-yellow-600 mb-4">Tu Wallet</h2>
        <p className="text-lg mb-6">Saldo: {balance}</p>
        <button
          onClick={handleLogout}
          className="bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
        >
          Cerrar Sesión
        </button>
      </div>
    </div>
  );
}

export default Wallet;
