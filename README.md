## Contract Risk Radar

AI-powered legal risk intelligence platform.

### Production Setup

This project is now configured for a normal server deployment with MongoDB Atlas.

Backend storage uses:

- `users` collection for authentication
- `contracts` collection for uploaded contracts and embedded clauses
- `counters` collection for stable numeric IDs

### Backend

1. Create a MongoDB Atlas cluster.
2. Create a database user and allow your server IP in Atlas network access.
3. Update `backend/.env` with:
   - `MONGO_URI`
   - `MONGO_DB_NAME`
   - `JWT_SECRET_KEY`
   - `GROQ_API_KEY` or `OPENAI_API_KEY`
   - `BACKEND_CORS_ORIGINS` to your frontend origin
4. Install dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

5. Start the API server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The backend exposes:

- API root at `/api`
- Health check at `/health`
- OpenAPI docs at `/api/docs`

### Frontend

Set the backend URL before running or building the frontend:

```bash
cd frontend
npm install
$env:NEXT_PUBLIC_API_BASE_URL="https://your-backend-domain.com/api"
npm run build
npm run start
```

For local development:

```bash
$env:NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
npm run dev
```

### Notes

- Docker is not required.
- The backend no longer uses SQLite or Postgres.
- All persisted app data now lives in MongoDB Atlas.

