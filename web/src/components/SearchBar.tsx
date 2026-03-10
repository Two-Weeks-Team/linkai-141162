import { useState } from 'react';
import { searchResources } from '@/lib/api';

export function SearchBar({ onSearch }: { onSearch: (results: any[]) => void }) {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<Record<string, any>>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const results = await searchResources(query, filters);
    onSearch(results);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="query" className="block mb-2">
          Search Query
        </label>
        <input
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-3 border rounded"
          placeholder="Recent advances in protein folding simulations"
        />
      </div>
      <div>
        <label htmlFor="domain" className="block mb-2">
          Research Domain
        </label>
        <select
          id="domain"
          value={filters.domain || ''}
          onChange={(e) => setFilters({...filters, domain: e.target.value})}
          className="w-full p-3 border rounded"
        >
          <option value="">Select domain</option>
          <option value="biomedical_engineering">Biomedical Engineering</option>
          <option value="quantum_computing">Quantum Computing</option>
        </select>
      </div>
      <button
        type="submit"
        className="w-full bg-linkai-blue text-white p-3 rounded hover:bg-blue-600"
      >
        Search
      </button>
    </form>
  );
}

export default SearchBar
