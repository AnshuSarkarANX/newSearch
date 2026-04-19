const SOURCE_META = {
  techcrunch:  { color: "bg-green-100 text-green-700",   label: "TechCrunch"   },
  arstechnica: { color: "bg-orange-100 text-orange-700", label: "Ars Technica" },
  hackernews:  { color: "bg-yellow-100 text-yellow-800", label: "Hacker News"  },
  theverge:    { color: "bg-purple-100 text-purple-700", label: "The Verge"    },
};

function timeAgo(dateStr) {
  if (!dateStr) return "";
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1)  return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24)  return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export default function ResultCard({ article }) {
  const meta = SOURCE_META[article.source] || { color: "bg-gray-100 text-gray-600", label: article.source };
  return (
    <a href={article.url} target="_blank" rel="noopener noreferrer"
      className="flex gap-4 p-4 bg-white rounded-xl border border-gray-100
                 shadow-sm hover:shadow-md hover:border-gray-200 transition group">
      {article.image_url && (
        <img src={article.image_url} alt="" width={96} height={80} loading="lazy"
          className="w-24 h-20 object-cover rounded-lg flex-shrink-0 bg-gray-100"
          onError={(e) => { e.target.style.display = "none"; }} />
      )}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1.5 flex-wrap">
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${meta.color}`}>{meta.label}</span>
          <span className="text-xs text-gray-400">{timeAgo(article.published_at)}</span>
          {article.author && <span className="text-xs text-gray-400">· {article.author}</span>}
        </div>
        <h2 className="font-semibold text-gray-900 group-hover:text-teal-600 transition
                       line-clamp-2 text-[15px] leading-snug mb-1.5"
          dangerouslySetInnerHTML={{ __html: article.title }} />
        {article.summary && (
          <p className="text-sm text-gray-500 line-clamp-2 leading-relaxed"
            dangerouslySetInnerHTML={{ __html: article.summary }} />
        )}
        {article.tags?.length > 0 && (
          <div className="flex gap-1 mt-2 flex-wrap">
            {article.tags.slice(0, 4).map((tag) => (
              <span key={tag} className="text-xs bg-gray-50 text-gray-400 px-2 py-0.5 rounded-full">#{tag}</span>
            ))}
          </div>
        )}
      </div>
    </a>
  );
}
