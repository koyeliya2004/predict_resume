# 🚀 Deploy to Hugging Face Spaces (Docker)

## Step 1 — Create a new Space
1. Go to https://huggingface.co/new-space
2. Set **Space name**: `resume-analyzer-api`
3. Select **SDK**: `Docker`
4. Set **Visibility**: Public
5. Click **Create Space**

## Step 2 — Push your code to the Space
In your terminal:
```bash
# Clone the HF Space repo
git clone https://huggingface.co/spaces/koyelog/resume-analyzer-api
cd resume-analyzer-api

# Copy these files into it:
# - Dockerfile (from root)
# - backend/ folder (all files)

# Then push
git add .
git commit -m "Deploy resume analyzer backend"
git push
```

## Step 3 — Wait for build (~3-5 mins)
Hugging Face will automatically build your Docker container and deploy it.

Your API URL will be:
```
https://koyelog-resume-analyzer-api.hf.space
```

## Step 4 — Update your frontend
In `frontend/env.js`, change the API URL to:
```js
window._ENV_API_URL = "https://koyelog-resume-analyzer-api.hf.space";
```

## Step 5 — Deploy frontend to Vercel
1. Go to https://vercel.com
2. Import your GitHub repo
3. Set **Root Directory** to `frontend`
4. Deploy!

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/analyze/text` | Analyze resume text |
| POST | `/analyze/file` | Upload PDF/DOCX/TXT |

## Memory Usage
| Component | RAM |
|-----------|-----|
| spaCy | ~50MB |
| BERT NER | ~400MB |
| FastAPI | ~30MB |
| **Total** | **~480MB** |

Hugging Face free tier gives **16GB RAM** — plenty of space! ✅
