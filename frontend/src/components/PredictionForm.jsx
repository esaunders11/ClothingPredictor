import React, { useState } from "react";
import axios from "axios";

export default function PredictionForm() {
  const [form, setForm] = useState({
    brand: "",
    category: "",
    condition: "",
    size: "",
    platform: "eBay", // Default selection
  });

  const [price, setPrice] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      const response = await axios.post("http://localhost:8000/predict", form);
      setPrice(response.data);
    } catch (err) {
      setError("Failed to fetch prediction." + err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {["brand", "category", "condition", "size"].map((field) => (
        <div key={field}>
          <label className="block text-sm font-medium text-gray-700 capitalize">{field}</label>
          <input
            type="text"
            name={field}
            value={form[field]}
            onChange={handleChange}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>
      ))}

      {/* Platform Dropdown */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Platform</label>
        <select
          name="platform"
          value={form.platform}
          onChange={handleChange}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        >
          <option value="eBay">eBay</option>
          <option value="Poshmark">Poshmark</option>
        </select>
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
      >
        Predict Price
      </button>

      {price && (
        <div className="mt-4 text-green-600 font-semibold">
          Predicted Price: ${price.toFixed(2)}
        </div>
      )}

      {error && (
        <div className="mt-4 text-red-500 font-semibold">
          {error}
        </div>
      )}
    </form>
  );
}
