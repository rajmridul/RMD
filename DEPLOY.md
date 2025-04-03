# AR-MED Deployment Guide for Render

This document guides you through the process of deploying the AR-MED application on Render.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code repository.
2. **Render Account**: Sign up for a free account at [render.com](https://render.com).

## Steps to Deploy

### 1. Prepare Your Code Repository

1. Push your code to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Prepare for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ar-med.git
   git push -u origin main
   ```

### 2. Deploy the Backend on Render

1. Log in to your Render account.

2. Click on **"New +"** and select **"Web Service"**.

3. Connect your GitHub repository by authorizing Render to access your GitHub account.

4. Configure the web service:
   - **Name**: `armed-backend` (or your preferred name)
   - **Region**: Choose closest to your target users
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn 'app:app' --config gunicorn.conf.py`
   - **Plan**: Free (or choose a paid plan for better performance)

5. Click on **"Advanced"** and add these environment variables:
   - `PYTHON_VERSION`: `3.9.16`
   - `PYTHONUNBUFFERED`: `true`
   - `DEBUG`: `false`

6. Click **"Create Web Service"** and wait for the deployment to complete.

7. Once deployed, note the URL of your backend service (e.g., `https://armed-backend.onrender.com`).

### 3. Deploy the Frontend on Render

1. Go back to the Render dashboard and click **"New +"** again.

2. Select **"Static Site"**.

3. Connect the same GitHub repository.

4. Configure the static site:
   - **Name**: `armed-frontend` (or your preferred name)
   - **Branch**: `main`
   - **Build Command**: `cd frontend/ar-med && npm install && npm run build`
   - **Publish Directory**: `frontend/ar-med/build`

5. Add this environment variable:
   - `REACT_APP_API_URL`: The URL of your backend service (e.g., `https://armed-backend.onrender.com`)

6. Click **"Create Static Site"** and wait for the deployment to complete.

### 4. Testing Your Deployment

1. Once both deployments are complete, visit your frontend URL (e.g., `https://armed-frontend.onrender.com`).

2. Test the application by uploading an image or video for analysis.

3. If you encounter any issues, check the Render logs for both the backend and frontend services.

### 5. Maintenance Notes

- **File Storage**: Render has ephemeral storage, meaning files are not permanently stored. The application automatically cleans up files older than 1 hour.

- **Free Tier Limitations**: 
  - The free tier has limited CPU and memory resources
  - Services may spin down after periods of inactivity
  - Consider upgrading to a paid plan for production use

- **Updating Your Application**:
  - Push changes to your GitHub repository
  - Render will automatically rebuild and redeploy your application

## Troubleshooting

If you encounter issues during deployment:

1. **Backend Errors**: Check the logs in your Render dashboard for the Web Service.

2. **Frontend Errors**: Check the browser console and the logs in your Render dashboard for the Static Site.

3. **CORS Issues**: Ensure the CORS configuration in `app.py` includes your frontend domain.

4. **Memory Issues**: If processing large videos causes crashes, consider reducing the number of frames processed or upgrading to a paid plan.

For any other issues, refer to the [Render documentation](https://render.com/docs) or contact support. 