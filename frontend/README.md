# Frontend - Course Registration System

React + TypeScript frontend with intentional security vulnerabilities.

## Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. **Run development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Security Vulnerabilities

⚠️ **This application contains intentional vulnerabilities:**

1. **Reflected XSS** - Course search results echo user input unsafely
2. **CSRF** - Enrollment requests lack CSRF token
3. **Broken Authentication** - Sensitive data stored in localStorage

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   │   └── Layout.tsx
│   ├── pages/           # Page components
│   │   ├── Login.tsx
│   │   ├── Courses.tsx  # VULNERABLE: XSS
│   │   ├── Dashboard.tsx
│   │   └── ...
│   ├── services/        # API services
│   │   └── api.ts       # VULNERABLE: No CSRF tokens
│   ├── App.tsx
│   └── main.tsx
├── package.json
└── vite.config.js
```

## Development

Run with hot reload:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

