import React from "react";
import TrendChart from "../components/TrendChart";

export default function Trends() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-center text-gray-800">
          📈 Price Trends
        </h1>
        <p className="text-center text-gray-600 mt-2">
          Visualize how resale prices change over time by category, brand, and more.
        </p>
      </header>

      <main className="max-w-4xl mx-auto bg-white shadow-md p-6 rounded-lg">
        <TrendChart />
      </main>

      <footer className="text-center text-gray-500 mt-8 text-sm">
        Powered by real sales data. Future filters and breakdowns coming soon.
      </footer>
    </div>
  );
}
