## Contract Risk Radar

AI-powered legal risk intelligence platform.

### Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`, OpenAPI docs at `/api/docs`.

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

### Basic Flow

1. Register and log in via the UI.
2. Upload a contract (PDF/DOCX/TXT) on the `Contracts` page.
3. The backend extracts text, segments clauses, calls the NLP/LLM risk engine, and returns structured clause analysis.
4. Dashboard shows aggregate risk metrics; the contracts view provides clause-by-clause explanations and safer rewrites.

