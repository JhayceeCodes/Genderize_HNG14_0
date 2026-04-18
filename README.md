# Name Classification API

This API accepts a name, enriches it using external services (Genderize, Agify, Nationalize), applies basic classification logic, and stores the result in a database. It also prevents duplicate entries based on name.

---

## Base URL
`/api/profiles`

---

## Features

- Predict gender using Genderize API
- Estimate age using Agify API
- Detect nationality using Nationalize API
- Classify age into:
  - child (0–12)
  - teenager (13–19)
  - adult (20–59)
  - senior (60+)
- Prevent duplicate profiles (case-insensitive name match)
- Persistent storage in database
- Structured JSON responses

---

## Endpoints

### Create Profile
**POST** `/api/profiles`

```json
{
  "name": "ella"
}
```

## Success Response (201):

```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

## Get All Profiles

**GET** `/api/profiles`

### Optional filters:
- gender
- country_id
- age_group

## Get Single Profile

**GET** `/api/profiles/{uuid}`

## Delete Profile

**DELETE** `/api/profiles/{uuid}`

#### Returns:
```bash
204 No Content
```

### Error Format
```json
{
  "status": "error",
  "message": "error description"
}
```

### Error Codes
- 400 – Missing or empty name
- 422 – Invalid input
- 404 – Profile not found
- 502 – External API failure


## How to Run

```bash
git clone https://github.com/JhayceeCodes/Genderize_HNG14_0.git
cd Genderize_HNG14_0.git

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### API will be available at:
```bash
http://127.0.0.1:8000/
```