import { useState } from 'react';
import { SearchBar } from '@/components/SearchBar';
import { SummaryCard } from '@/components/SummaryCard';

export default function Home() {
  const [results, setResults] = useState<any[]>([]);

  return (
    <div className="space-y-8">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold mb-6">Semantic Research Search</h2>
        <SearchBar onSearch={setResults} />
      </div>
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {results.map((result, i) => (
          <SummaryCard key={i} resource={result} />
        ))}
      </div>
    </div>
  );
}