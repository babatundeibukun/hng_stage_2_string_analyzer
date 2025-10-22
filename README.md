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


3️⃣ Get All Strings (with Filtering)
GET /strings
Query Parameters:
Parameter	Type	Description
is_palindrome	boolean	Filter by palindrome status
min_length	integer	Minimum string length
max_length	integer	Maximum string length
word_count	integer	Exact number of words
contains_character	string	Filter strings containing a character

4️⃣ Natural Language Filtering
GET /strings/filter-by-natural-language?query=your%20query
Examples:
/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings
/strings/filter-by-natural-language?query=strings%20longer%20than%2010%20characters
/strings/filter-by-natural-language?query=strings%20containing%20the%20letter%20z
Response:

{
  "data": [ ... ],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}

5️⃣ Delete String
DELETE /strings/{string_value}
Deletes a specific string from the database.
Returns 204 No Content on success.


⚙️ Setup Instructions
🧩 Prerequisites
Ensure you have the following installed:
Python 3.9+
Git

📦 Installation
# Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt







