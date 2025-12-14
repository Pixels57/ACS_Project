# GitHub Repository Setup Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Repository name: `course-registration-vulnerable` (or your preferred name)
4. Description: "Vulnerable course registration system for security assessment"
5. **Visibility**: Choose Private (recommended for academic projects) or Public
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Initialize Local Git Repository

Open terminal in your project directory:

```bash
cd d:\UNI\ACS\Project

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Backend and frontend infrastructure with vulnerabilities"
```

## Step 3: Connect to GitHub

```bash
# Add remote repository (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/course-registration-vulnerable.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Create Baseline Tag

After pushing, create the baseline tag for Stage 1:

```bash
# Create annotated tag
git tag -a baseline-unpatched -m "Baseline unpatched version for Stage 1 - Reconnaissance phase"

# Push tag to GitHub
git push origin baseline-unpatched
```

## Step 5: Verify Setup

1. Go to your GitHub repository page
2. Verify all files are present
3. Check that the tag `baseline-unpatched` exists under "Releases" or "Tags"

## Step 6: Set Up Branch Protection (Optional)

For team collaboration:

1. Go to repository Settings → Branches
2. Add rule for `main` branch:
   - Require pull request reviews
   - Require status checks to pass
   - Include administrators

## Collaboration Setup

### For Team Member 2:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/course-registration-vulnerable.git

# Navigate to project
cd course-registration-vulnerable

# Set up backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Set up frontend
cd ../frontend
npm install
```

## Workflow for Development

### Daily Workflow:

```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Before Major Milestones:

```bash
# Ensure you're on main branch
git checkout main

# Pull latest
git pull origin main

# Create milestone tag
git tag -a stage1-complete -m "Stage 1: Reconnaissance complete"
git push origin stage1-complete
```

## Repository Structure on GitHub

Your repository should have:

```
course-registration-vulnerable/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── docs/              # (to be created in Stage 1)
├── recon/             # (to be created in Stage 1)
├── .gitignore
├── README.md
├── SETUP.md
└── ARCHITECTURE_AND_TASKS.md
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

```bash
# Use GitHub CLI or Personal Access Token
# Generate token: GitHub Settings → Developer settings → Personal access tokens
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/course-registration-vulnerable.git
```

### Large Files

If you accidentally commit large files:

```bash
# Remove from git history (use carefully)
git rm --cached large-file.db
git commit -m "Remove large file"
```

## Next Steps

1. ✅ Repository created and connected
2. ✅ Initial code pushed
3. ✅ Baseline tag created
4. ⏭️ Start Stage 1: Reconnaissance & Threat Modeling
5. ⏭️ Create docs/ and recon/ folders
6. ⏭️ Complete threat model documentation

