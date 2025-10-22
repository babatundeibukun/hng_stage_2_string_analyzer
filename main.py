from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from hashlib import sha256
import json, os, re
import uvicorn

app = FastAPI(title="HNG Stage 1 — String Analyzer API")

DATA_FILE = "data/strings.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Initialize storage file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def analyze_string(value: str):
    """Compute all required string properties."""
    value_clean = value.strip()
    length = len(value_clean)
    is_palindrome = value_clean.lower() == value_clean[::-1].lower()
    unique_chars = len(set(value_clean))
    word_count = len(value_clean.split())
    hash_value = sha256(value_clean.encode()).hexdigest()
    freq_map = {ch: value_clean.count(ch) for ch in set(value_clean)}

    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_chars,
        "word_count": word_count,
        "sha256_hash": hash_value,
        "character_frequency_map": freq_map,
    }

@app.post("/strings", status_code=201)
def create_string(payload: dict):
    """Analyze and store a new string."""
    value = payload.get("value")
    if not isinstance(value, str):
        raise HTTPException(status_code=422, detail="Value must be a string")
    if not value.strip():
        raise HTTPException(status_code=400, detail="Missing 'value' field")

    data = load_data()
    hash_value = sha256(value.encode()).hexdigest()

    if hash_value in data:
        raise HTTPException(status_code=409, detail="String already exists")

    properties = analyze_string(value)
    entry = {
        "id": hash_value,
        "value": value,
        "properties": properties,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    data[hash_value] = entry
    save_data(data)

    return JSONResponse(status_code=201, content=entry)

@app.get("/strings/filter-by-natural-language")
def filter_by_natural_language(query: str = Query(..., description="Natural language query")):
    """
    Parse a natural language query and return matching strings.
    Examples:
    - 'all single word palindromic strings'
    - 'strings longer than 10 characters'
    - 'palindromic strings that contain the first vowel'
    - 'strings containing the letter z'
    """

    data = load_data()
    results = list(data.values())

    parsed_filters = {}

    # Normalize query
    q = query.lower().strip()

    # === SIMPLE PATTERN MATCHING RULES ===
    if "palindromic" in q or "palindrome" in q:
        parsed_filters["is_palindrome"] = True
        results = [r for r in results if r["properties"]["is_palindrome"]]

    match = re.search(r"longer than (\d+)", q)
    if match:
        min_len = int(match.group(1)) + 1
        parsed_filters["min_length"] = min_len
        results = [r for r in results if r["properties"]["length"] >= min_len]

    match = re.search(r"shorter than (\d+)", q)
    if match:
        max_len = int(match.group(1)) - 1
        parsed_filters["max_length"] = max_len
        results = [r for r in results if r["properties"]["length"] <= max_len]

    if "single word" in q or "one word" in q:
        parsed_filters["word_count"] = 1
        results = [r for r in results if r["properties"]["word_count"] == 1]

    match = re.search(r"containing the letter ([a-z])", q)
    if match:
        ch = match.group(1)
        parsed_filters["contains_character"] = ch
        results = [r for r in results if ch in r["value"]]

    if "contain the first vowel" in q:
        parsed_filters["contains_character"] = "a"
        results = [r for r in results if "a" in r["value"]]

    # If no rules matched
    if not parsed_filters:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    return {
        "data": results,
        "count": len(results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }


@app.get("/strings/{string_value}")
def get_string(string_value: str):
    """Retrieve specific analyzed string."""
    data = load_data()
    hash_value = sha256(string_value.encode()).hexdigest()
    if hash_value not in data:
        raise HTTPException(status_code=404, detail="String not found")
    return data[hash_value]

@app.get("/strings")
def get_all_strings(
    is_palindrome: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    word_count: int | None = None,
    contains_character: str | None = None
):
    """Retrieve all strings with optional filters."""
    data = load_data()
    results = list(data.values())

    if is_palindrome is not None:
        results = [r for r in results if r["properties"]["is_palindrome"] == is_palindrome]
    if min_length is not None:
        results = [r for r in results if r["properties"]["length"] >= min_length]
    if max_length is not None:
        results = [r for r in results if r["properties"]["length"] <= max_length]
    if word_count is not None:
        results = [r for r in results if r["properties"]["word_count"] == word_count]
    if contains_character is not None:
        results = [r for r in results if contains_character in r["value"]]

    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }

    return {"data": results, "count": len(results), "filters_applied": filters}

@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    """Delete string by its value."""
    data = load_data()
    hash_value = sha256(string_value.encode()).hexdigest()
    if hash_value not in data:
        raise HTTPException(status_code=404, detail="String not found")
    del data[hash_value]
    save_data(data)
    return JSONResponse(status_code=204, content=None)

if __name__ == "_main_":
    port = int(os.environ.get("PORT", 8000))  # Railway provides PORT dynamically
    uvicorn.run("main:app", host="0.0.0.0",port=port)
