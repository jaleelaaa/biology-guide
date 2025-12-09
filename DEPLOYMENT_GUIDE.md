# Firebase Deployment Guide

This guide explains how to deploy the Plus One Biology website to Firebase Hosting with automated CI/CD.

---

## Prerequisites

1. **GitHub Account**: Your repository at https://github.com/jaleelaaa/biology-guide
2. **Firebase Account**: Sign up at https://firebase.google.com
3. **Node.js & npm**: For Firebase CLI (optional for manual deployment)

---

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click **"Add project"**
3. Enter project name: `biology-guide` (or your preferred name)
4. Disable Google Analytics (optional)
5. Click **"Create project"**

---

## Step 2: Initialize Firebase Hosting

1. In Firebase Console, go to **Build** → **Hosting**
2. Click **"Get started"**
3. Follow the setup wizard (you can skip installation steps since we already have config files)

---

## Step 3: Update Firebase Project ID

Edit `.firebaserc` file and replace with your Firebase project ID:

```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

Find your project ID in Firebase Console → Project Settings

---

## Step 4: Generate Firebase Service Account

This is needed for GitHub Actions to deploy automatically.

### Option A: Using Firebase Console (Recommended)

1. Go to Firebase Console → **Project Settings** → **Service accounts**
2. Click **"Generate new private key"**
3. Download the JSON file (keep it secure!)
4. Copy the entire JSON content

### Option B: Using Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your Firebase project
3. Go to **IAM & Admin** → **Service Accounts**
4. Create a new service account with **Firebase Admin** role
5. Create and download a JSON key

---

## Step 5: Configure GitHub Secrets

1. Go to your GitHub repository: https://github.com/jaleelaaa/biology-guide
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add these secrets:

### Secret 1: FIREBASE_SERVICE_ACCOUNT

- **Name**: `FIREBASE_SERVICE_ACCOUNT`
- **Value**: Paste the entire JSON content from the service account key
- Click **"Add secret"**

### Secret 2: FIREBASE_PROJECT_ID

- **Name**: `FIREBASE_PROJECT_ID`
- **Value**: Your Firebase project ID (e.g., `biology-guide-12345`)
- Click **"Add secret"**

---

## Step 6: Push Firebase Configuration

Commit and push the Firebase configuration files:

```bash
git add .firebaserc firebase.json .github/
git commit -m "Add Firebase hosting configuration and CI/CD workflow"
git push origin main
```

---

## Step 7: Verify Deployment

1. Go to **GitHub** → **Actions** tab in your repository
2. You should see the **"Deploy to Firebase Hosting"** workflow running
3. Wait for it to complete (usually 1-2 minutes)
4. Check the logs for the deployment URL

---

## Step 8: Access Your Deployed Site

Once deployed, your site will be available at:

**Primary URL**: `https://YOUR_PROJECT_ID.web.app`

**Custom domain** (optional): You can add a custom domain in Firebase Console → Hosting → Add custom domain

---

## Manual Deployment (Alternative)

If you prefer to deploy manually instead of using CI/CD:

### Install Firebase CLI

```bash
npm install -g firebase-tools
```

### Login to Firebase

```bash
firebase login
```

### Deploy

```bash
cd D:\Plus_One_Doc\Botany\Web
firebase deploy
```

---

## CI/CD Workflow Explanation

The GitHub Actions workflow (`.github/workflows/firebase-deploy.yml`) automatically:

1. **Triggers on**:
   - Push to `main` branch
   - Pull requests to `main` branch

2. **Build steps**:
   - Checks out code
   - Sets up Python environment
   - Installs dependencies (markdown2)
   - Optionally builds content

3. **Deploy step**:
   - Uses Firebase service account from secrets
   - Deploys to Firebase Hosting
   - Updates the live site

---

## File Structure

```
biology-guide/
├── .firebaserc                # Firebase project configuration
├── firebase.json              # Firebase hosting configuration
├── .github/
│   └── workflows/
│       └── firebase-deploy.yml  # CI/CD workflow
└── [all your web files]
```

---

## Troubleshooting

### Issue: Deployment fails with "permission denied"

**Solution**: Ensure your Firebase service account has the following roles:
- Firebase Admin
- Hosting Admin

### Issue: "Project not found"

**Solution**: 
1. Check `.firebaserc` has correct project ID
2. Check GitHub secret `FIREBASE_PROJECT_ID` matches
3. Verify project exists in Firebase Console

### Issue: Workflow doesn't trigger

**Solution**:
1. Check GitHub Actions is enabled in repository settings
2. Verify the workflow file is in `.github/workflows/`
3. Ensure you've pushed to the `main` branch

---

## Updating Content

### Automatic Update (CI/CD)

Simply push changes to GitHub:

```bash
git add .
git commit -m "Update content"
git push origin main
```

GitHub Actions will automatically deploy the changes to Firebase Hosting.

### Manual Update

If you've changed the markdown source and need to rebuild:

```bash
python convert_study_guide_proper.py
git add .
git commit -m "Rebuild content"
git push origin main
```

---

## Monitoring & Analytics

### Firebase Console

Monitor deployment status, traffic, and performance:
- Firebase Console → Hosting → Dashboard

### GitHub Actions

View deployment logs and history:
- GitHub Repository → Actions tab

---

## Next Steps

1. ✅ Set up custom domain (optional)
2. ✅ Enable Firebase Performance Monitoring
3. ✅ Set up Firebase Analytics (optional)
4. ✅ Configure CDN caching rules
5. ✅ Add SSL certificate (automatic with Firebase)

---

## Support

For issues or questions:
- **Firebase Documentation**: https://firebase.google.com/docs/hosting
- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Repository**: https://github.com/jaleelaaa/biology-guide

---

**Ready to deploy!** 🚀

Your Plus One Biology website will be live on Firebase Hosting with automatic deployments on every push to main.
