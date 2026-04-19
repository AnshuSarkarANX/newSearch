import { useState } from "react";

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState("");

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSearch(query); }} className="flex gap-2 w-full">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search tech news... e.g. 'AI chips', 'React 19', 'Apple'"
        className="flex-1 px-4 py-3 rounded-xl border border-gray-200 text-base
                   focus:outline-none focus:ring-2 focus:ring-teal-500 bg-white shadow-sm"
      />
      <button
        type="submit"
        disabled={loading}
        className="px-6 py-3 bg-teal-600 text-white rounded-xl font-semibold
                   hover:bg-teal-700 transition disabled:opacity-50 whitespace-nowrap"
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}
