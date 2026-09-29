# AI Chef Recommendation Backend

FastAPI backend for the AI Chef online-learning recommendation experiment.

## Run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend exposes interaction endpoints and a recommendation endpoint. The recommendation engine uses River's Bernoulli Naive Bayes model and persists the demo user's interaction history locally.
