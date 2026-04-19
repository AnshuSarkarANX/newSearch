export default function Pagination({ page, total, size, onPageChange }) {
  const totalPages = Math.ceil(total / size);
  if (totalPages <= 1) return null;
  const pages = [];
  for (let i = Math.max(1, page - 2); i <= Math.min(totalPages, page + 2); i++) pages.push(i);

  return (
    <div className="flex items-center gap-2 justify-center mt-8">
      <button onClick={() => onPageChange(page - 1)} disabled={page === 1}
        className="px-4 py-2 rounded-lg border text-sm font-medium disabled:opacity-40 hover:bg-gray-50 transition">
        ← Prev
      </button>
      {pages.map((p) => (
        <button key={p} onClick={() => onPageChange(p)}
          className={`w-9 h-9 rounded-lg text-sm font-medium transition
            ${p === page ? "bg-teal-600 text-white" : "border hover:bg-gray-50 text-gray-600"}`}>
          {p}
        </button>
      ))}
      <button onClick={() => onPageChange(page + 1)} disabled={page >= totalPages}
        className="px-4 py-2 rounded-lg border text-sm font-medium disabled:opacity-40 hover:bg-gray-50 transition">
        Next →
      </button>
      <span className="text-sm text-gray-400 ml-2">{total.toLocaleString()} results</span>
    </div>
  );
}
