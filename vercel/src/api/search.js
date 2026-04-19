import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const searchNews = async ({ q, source, time, sort, page = 1 }) => {
  const res = await axios.get(`${API}/search`, {
    params: { q, source, time, sort, page, size: 10 }
  });
  return res.data;
};
