import { useState, useCallback } from "react";
import { searchNews } from "./api/search";
import SearchBar  from "./components/SearchBar";
import Filters    from "./components/Filters";
import ResultCard  from "./components/ResultCard";
import Pagination  from "./components/Pagination";


const DEFAULT_FILTERS = { source: "all", time: "", sort: "relevant" };
const TRENDING = ["AI", "React", "Apple", "OpenAI", "Python", "Startups", "GPT", "Android"];

export default function App() {
  const [results,  setResults]  = useState([]);
  const [total,    setTotal]    = useState(0);
  const [page,     setPage]     = useState(1);
  const [loading,  setLoading]  = useState(false);
  const [query,    setQuery]    = useState("");
  const [searched, setSearched] = useState(false);
  const [error,    setError]    = useState(null);
  const [filters,  setFilters]  = useState(DEFAULT_FILTERS);

  const doSearch = useCallback(async (q, currentPage = 1, currentFilters = filters) => {
    setLoading(true);
    setError(null);
    setQuery(q);
    try {
      const data = await searchNews({
        q,
        source: currentFilters.source !== "all" ? currentFilters.source : undefined,
        time:   currentFilters.time   || undefined,
        sort:   currentFilters.sort,
        page:   currentPage,
      });
      setResults(data.results);
      setTotal(data.total);
      setPage(currentPage);
      setSearched(true);
    } catch {
      setError("Search failed. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    if (query) doSearch(query, 1, newFilters);
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <header className="bg-white border-b border-gray-100 sticky top-0 z-10 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 space-y-3">
          <div className="flex items-center gap-3">
            <svg width="34" height="34" viewBox="0 0 34 34" fill="none" aria-label="TechPulse">
              <circle cx="14" cy="14" r="10" stroke="#01696f" strokeWidth="2.5" fill="none"/>
              <line x1="21.5" y1="21.5" x2="30" y2="30" stroke="#01696f" strokeWidth="2.5" strokeLinecap="round"/>
              <path d="M9 14 L12 10 L15 16 L17 12 L20 14" stroke="#01696f" strokeWidth="1.8"
                    strokeLinecap="round" strokeLinejoin="round" fill="none"/>
            </svg>
            <div>
              <h1 className="text-xl font-bold text-gray-900 leading-none">TechPulse</h1>
              <p className="text-xs text-gray-400 mt-0.5">TechCrunch · Ars Technica · The Verge · Hacker News</p>
            </div>
          </div>
          <SearchBar onSearch={(q) => doSearch(q, 1)} loading={loading} />
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        {searched && (
          <div className="mb-5 space-y-2">
            <Filters filters={filters} onChange={handleFilterChange} />
            {!loading && (
              <p className="text-sm text-gray-400">
                {total === 0 ? "No results" : <>{total.toLocaleString()} results {query && <>for <strong className="text-gray-600">"{query}"</strong></>}</>}
              </p>
            )}
          </div>
        )}

        {error && <div className="p-4 bg-red-50 text-red-600 rounded-xl text-sm border border-red-100 mb-4">{error}</div>}

        {loading && (
          <div className="space-y-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="flex gap-4 p-4 bg-white rounded-xl border border-gray-100">
                <div className="w-24 h-20 bg-gray-100 rounded-lg animate-pulse flex-shrink-0" />
                <div className="flex-1 space-y-2 py-1">
                  <div className="h-3 bg-gray-100 rounded animate-pulse w-1/4" />
                  <div className="h-5 bg-gray-100 rounded animate-pulse w-4/5" />
                  <div className="h-3 bg-gray-100 rounded animate-pulse w-full" />
                  <div className="h-3 bg-gray-100 rounded animate-pulse w-3/5" />
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && results.length > 0 && (
          <>
            <div className="space-y-3">
              {results.map((article, i) => <ResultCard key={article.url || i} article={article} />)}
            </div>
            <Pagination page={page} total={total} size={10} onPageChange={(p) => doSearch(query, p)} />
          </>
        )}

        {!loading && searched && results.length === 0 && !error && (
          <div className="flex flex-col items-center py-24 text-gray-400">
            <svg className="w-14 h-14 mb-4 opacity-25" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
            </svg>
            <p className="text-lg font-medium text-gray-500">No results found</p>
            <p className="text-sm mt-1">Try different keywords or remove filters</p>
          </div>
        )}

        {!searched && !loading && (
          <div className="flex flex-col items-center py-24 text-center text-gray-400 select-none">
            <svg className="w-16 h-16 mb-6 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
            </svg>
            <p className="text-lg font-medium text-gray-500">Search the latest tech news</p>
            <p className="text-sm mt-2">Crawled from 4 sources · Updated every 30 minutes</p>
            <div className="flex gap-2 mt-5 flex-wrap justify-center">
              {TRENDING.map((term) => (
                <button key={term} onClick={() => doSearch(term, 1)}
                  className="px-3 py-1 text-sm bg-white border border-gray-200 rounded-full
                             hover:border-teal-400 hover:text-teal-600 transition">
                  {term}
                </button>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
