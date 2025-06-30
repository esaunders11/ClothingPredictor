import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const predictPrice = async (data) =>
  axios.post(`${API_BASE}/predict`, data);
