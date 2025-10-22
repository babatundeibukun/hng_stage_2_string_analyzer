# 🧠 String Analyzer API

A RESTful API service that analyzes strings and stores their computed properties.

Built with **FastAPI**, this service computes and stores multiple properties of any input string, including its length, palindrome status, unique character count, word count, SHA-256 hash, and character frequency map.  
It also supports advanced **filtering**, including **natural language queries** like  
> “all single word palindromic strings”.

---

## 🚀 Features

- **Analyze any string** for multiple linguistic and structural properties  
- **Retrieve** individual or all analyzed strings  
- **Filter results** with query parameters (e.g., `is_palindrome=true&min_length=5`)  
- **Natural language filtering** (e.g., “strings longer than 10 characters”)  
- **Persistent local storage** in `data.json`  
- **Fast, lightweight REST API** powered by FastAPI  

---

## 📂 API Endpoints

### 1️⃣ Create or Analyze String  
**POST** `/strings`

**Request Body:**
```json
{

 "value": "string to analyze"
}


Response:
{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": { "s": 2, "t": 3 }
  },
  "created_at": "2025-10-21T10:00:00Z"
}

2️⃣ Get Specific String

GET /strings/{string_value}

Response:

{
  "id": "sha256_hash_value",
  "value": "requested string",
  "properties": { ... },
  "created_at": "2025-10-21T10:00:00Z"
}

