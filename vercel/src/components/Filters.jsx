const SOURCES = [
  { value: "all",         label: "All Sources"  },
  { value: "techcrunch",  label: "TechCrunch"   },
  { value: "arstechnica", label: "Ars Technica"  },
  { value: "hackernews",  label: "Hacker News"  },
  { value: "theverge",    label: "The Verge"    },
];
const TIMES = [
  { value: "",      label: "Any time"    },
  { value: "hour",  label: "Past hour"   },
  { value: "today", label: "Today"       },
  { value: "week",  label: "This week"   },
  { value: "month", label: "This month"  },
];
const SORTS = [
  { value: "relevant", label: "Most Relevant" },
  { value: "latest",   label: "Latest First"  },
];

export default function Filters({ filters, onChange }) {
  return (
    <div className="flex flex-wrap gap-3 items-center">
      <div className="flex gap-1.5 flex-wrap">
        {SOURCES.map((s) => (
          <button key={s.value} onClick={() => onChange({ ...filters, source: s.value })}
            className={`px-3 py-1 rounded-full text-sm font-medium transition
              ${filters.source === s.value
                ? "bg-teal-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>
            {s.label}
          </button>
        ))}
      </div>
      <select value={filters.time} onChange={(e) => onChange({ ...filters, time: e.target.value })}
        className="px-3 py-1.5 rounded-lg border border-gray-200 text-sm bg-white">
        {TIMES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
      </select>
      <select value={filters.sort} onChange={(e) => onChange({ ...filters, sort: e.target.value })}
        className="px-3 py-1.5 rounded-lg border border-gray-200 text-sm bg-white">
        {SORTS.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
      </select>
    </div>
  );
}
