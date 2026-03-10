import os
import json
import re
import httpx
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Helper: extract JSON payload that may be wrapped in Markdown code fences.
# ---------------------------------------------------------------------------
def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

# ---------------------------------------------------------------------------
# Core inference caller – shared by all AI helpers.
# ---------------------------------------------------------------------------
async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    api_key = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    model = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
    url = "https://inference.do-ai.run/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        json_text = _extract_json(content)
        if not json_text:
            return {"note": "AI returned no JSON payload"}
        return json.loads(json_text)
    except Exception as exc:
        # Fallback – never raise to the FastAPI layer.
        return {"note": "AI service is temporarily unavailable.", "error": str(exc)}

# ---------------------------------------------------------------------------
# Public wrappers used by the API routes.
# ---------------------------------------------------------------------------
async def generate_summary(
    document: str,
    summary_type: str = "condensed",
    include_citations: bool = True,
    domain: str = "general",
) -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": "You are an academic summarizer. Produce a concise summary with citations when requested."},
        {
            "role": "user",
            "content": f"Document:\n{document}\n\nSummary type: {summary_type}\nInclude citations: {include_citations}\nDomain: {domain}",
        },
    ]
    return await _call_inference(messages)

async def extract_tags(text: str, domain: str = "general") -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": "You extract domain‑specific tags and relationships from research text. Return a JSON list of tags with confidence scores."},
        {"role": "user", "content": f"Text:\n{text}\n\nDomain: {domain}"},
    ]
    return await _call_inference(messages)

async def search_embeddings(query: str, filters: Dict[str, Any] | None = None) -> Dict[str, Any]:
    filter_part = json.dumps(filters) if filters else "{}"
    messages = [
        {"role": "system", "content": "You perform semantic search. Return a JSON array of resource identifiers with a relevance score (0‑1)."},
        {"role": "user", "content": f"Query: {query}\nFilters: {filter_part}"},
    ]
    return await _call_inference(messages)
