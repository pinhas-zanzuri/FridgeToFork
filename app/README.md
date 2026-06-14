# 🍴 FridgeToFork — Recipe Suggester

A Docker-based smart home management system.  
The app reads the ingredients available in your fridge and suggests the best matching recipe — including partial matches with a list of what you're still missing.

---

## 🧱 Architecture

The project runs two containers working together:

```
User's Browser
      │
      ▼
  [ Nginx :80 ]  ←─ Reverse proxy + serves the Dashboard
      │
      ▼
 [ Flask :5000 ] ←─ Application logic & API
      │
      ▼
 inventory.txt / recipes.json  ←─ Shared data via Docker Volumes
```

| Container | Role |
|-----------|------|
| `app` | Flask server — business logic, API, recipe suggestions |
| `proxy` | Nginx — serves the static dashboard and forwards API requests |

---

## ✨ Features

- **Automatic recipe suggestion** based on `inventory.txt`
- **Manual search** — select from ingredient tags or type freely
- **Meal type filter** — Dairy / Meat / Pareve / Any
- **Partial matching** — if no full match exists, returns the closest recipe and lists what's missing
- **Live editing** — changes to `recipes.json` take effect immediately, no restart needed

---

## 🚀 Getting Started

```bash
cd FridgeToFork
docker-compose up --build
```

Then open your browser at: http://localhost

To stop:

```bash
docker-compose down
```

---

## 🗂️ Project Structure

```
FridgeToFork/
├── docker-compose.yml       # Container orchestration
├── .env                     # Environment variables (username)
├── inventory.txt            # Fridge contents (one ingredient per line)
├── recipes.json             # Recipe definitions — editable at runtime
│
├── app/
│   ├── recipe_app.py        # Flask server + all API endpoints
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Build instructions for the app container
│
├── nginx/
│   └── nginx.conf           # Proxy configuration
│
└── dashboard/
    └── index.html           # Frontend UI
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api` | Suggest recipe from `inventory.txt` (for testing) |
| `POST` | `/api/suggest` | Suggest recipe from user-provided ingredients and type |
| `GET` | `/api/ingredients` | Return all unique ingredients across all recipes |

**Example request to `/api/suggest`:**

```json
{
  "ingredients": ["eggs", "butter", "salt"],
  "type": "dairy"
}
```

**Example response (partial match):**

```json
{
  "user": "Ariel And Pinhas",
  "recipe": "Cheese Toast",
  "matched_ingredients": 2,
  "missing": ["bread", "cheese", "tomatoes"],
  "full_match": false
}
```

---

## ✏️ Adding a New Recipe

Open `recipes.json` and add a recipe in this format:

```json
"Pizza": {
  "ingredients": ["bread", "tomatoes", "cheese"],
  "type": "dairy"
}
```

Valid types: `"dairy"` / `"meat"` / `"pareve"`  
Changes take effect immediately — no rebuild required.

---

## 🌱 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USER_NAME` | `Guest` | Username displayed in the dashboard |

Edit the `.env` file to change it.

---

*Built with Flask · Nginx · Docker Compose*
