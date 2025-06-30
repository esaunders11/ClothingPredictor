import React from "react";
import PredictionForm from "../components/PredictionForm";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-center text-gray-800">
          🧥 Clothing Price Predictor
        </h1>
        <p className="text-center text-gray-600 mt-2">
          Enter item details to get a price estimate based on past sales.
        </p>
      </header>

      <main className="max-w-xl mx-auto bg-white shadow-md p-6 rounded-lg">
        <PredictionForm />
      </main>

    </div>
  );
}
