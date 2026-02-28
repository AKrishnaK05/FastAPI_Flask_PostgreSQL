# FastAPI + Flask + PostgreSQL Full-Stack App

## Architecture (Brief)

- **Backend service (`backend`)**: FastAPI API-only service with SQLAlchemy models and PostgreSQL.
- **Frontend service (`frontend`)**: Flask app that renders Jinja templates and consumes FastAPI via REST.
- **Database (`db`)**: PostgreSQL accessed only by FastAPI.
- **Communication flow**:
  1. User submits form in Flask UI.
  2. Flask calls FastAPI endpoint through HTTP.
  3. FastAPI validates input, performs DB operation, returns JSON.
  4. Flask handles result and renders/redirects.

This enforces separation of concerns and clean service boundaries.

---

## Project Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   └── routers/
│       ├── users.py
│       └── auth.py
├── alembic/
├── tests/
├── requirements.txt
└── .env

frontend/
├── app.py
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   └── style.css
├── requirements.txt
└── .env
```

---

## Backend API Endpoints

- `POST /api/v1/users/` → create user
- `GET /api/v1/users/{id}` → fetch user by id
- `POST /api/v1/auth/token` → login and receive JWT
- `GET /health` → health check

All responses are JSON.

---

## Local Setup (Without Docker)

### 1) Start PostgreSQL

Run local PostgreSQL and create DB/user matching backend `.env`, or update backend `.env` with your local credentials.

### 2) Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3) Run Frontend

```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:5000`

---

## Docker Setup (Recommended)

From project root:

```bash
docker compose up --build
```

Services:
- Frontend: `http://localhost:5000`
- Backend Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

---

## Sample API Requests

### Create User

```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","full_name":"John Doe","password":"StrongPass123"}'
```

### Get User

```bash
curl http://localhost:8000/api/v1/users/1
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"StrongPass123"}'
```

---

## Testing

Run backend tests:

```bash
cd backend
pytest -q
```

---

## Notes

- No hardcoded production secrets: replace keys in `.env` files.
- FastAPI handles all data access; Flask never talks to DB directly.
- DB tables auto-create at backend startup (`Base.metadata.create_all`).
- `alembic/` folder is included for migration upgrade path.
