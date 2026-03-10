import { useState } from 'react';
import { fetchSummary } from '@/lib/api';

export function SummaryCard({ resource }: { resource: any }) {
  const [summary, setSummary] = useState(resource.summary || null);

  const handleSummarize = async () => {
    if (!resource.content) return;
    const result = await fetchSummary(resource.content, 'biomedical_engineering');
    setSummary(result.summary);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="font-bold text-lg mb-2 truncate">{resource.title}</h3>
      <p className="text-sm text-gray-500 mb-2 truncate">{resource.url}</p>
      
      {summary ? (
        <div className="mt-3 p-3 bg-gray-50 rounded">
          <p className="text-gray-700">{summary}</p>
          {resource.citations && (
            <div className="mt-3">
              <h4 className="font-semibold mb-1">Citations:</h4>
              <ul className="list-disc pl-5 space-y-1">
                {resource.citations.map((c: any, i: number) => (
                  <li key={i} className="text-sm text-blue-600 hover:underline">
                    {c.source}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ) : (
        <button
          onClick={handleSummarize}
          className="mt-3 px-4 py-2 bg-linkai-blue text-white rounded hover:bg-blue-600"
        >
          Generate Summary
        </button>
      )}
    </div>
  );
}

export default SummaryCard
