export async function fetchSummary(document: string, domain: string) {
  const res = await fetch('/api/summaries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document, domain })
  });
  return res.json();
}

export async function generateTags(text: string, domain: string) {
  const res = await fetch('/api/semantic-tags', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, domain })
  });
  return res.json();
}

export async function searchResources(query: string, filters: any) {
  const res = await fetch('/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, filters })
  });
  return res.json();
}