# Deployment to Vercel

## Frontend Deployment (Next.js on Vercel)

### Prerequisites
1. GitHub repository pushed (✓ Already done)
2. Vercel account (create at https://vercel.com)

### Steps to Deploy

1. **Connect Repository to Vercel**
   - Go to https://vercel.com/new
   - Import your GitHub repository: `Dnrahul/intelligence-review`
   - Select the `frontend` directory as the root

2. **Environment Variables**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL:
     - Development: `http://localhost:8000`
     - Production: Your deployed backend URL (e.g., `https://your-backend.herokuapp.com`)

3. **Build Settings**
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically build and deploy your frontend

## Backend Deployment (FastAPI)

### Option 1: Deploy to Heroku (Recommended for free tier)

```bash
# 1. Install Heroku CLI
# 2. Create Procfile in backend directory with:
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 3. Create runtime.txt with:
python-3.13.12

# 4. Create .gitignore in backend (if not exists)
# 5. Deploy
heroku login
heroku create your-app-name
git push heroku master
```

### Option 2: Deploy to Railway
- Connect GitHub repository at https://railway.app
- Set environment variables for OpenAI API key
- Railway will detect and deploy automatically

### Option 3: Deploy to Render
- Connect GitHub repository at https://render.com
- Select Python as the environment
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

## Update Frontend API URL

Once backend is deployed, update the `.env.production.local` file in frontend:

```
NEXT_PUBLIC_API_URL=https://your-deployed-backend-url.com
```

Then redeploy the frontend on Vercel.
