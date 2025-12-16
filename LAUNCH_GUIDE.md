# Launch Guide - Matching Frontend and Backend Protocols

## Important: Frontend and Backend Must Match!

The frontend and backend must use the **same protocol** (HTTP or HTTPS). If they don't match, you'll get "socket hang up" errors.

---

## Option 1: Both on HTTPS (Recommended - Secure)

### Start Backend (HTTPS):
```powershell
cd backend
python main.py
# Or explicitly:
# USE_HTTP=false python main.py
```

### Start Frontend (HTTPS):
```powershell
cd frontend
npm run dev:https
```

**Access:**
- Frontend: `https://localhost:3000` ✅ Secure
- Backend: `https://localhost:8000` ✅ Secure

---

## Option 2: Both on HTTP (For Network Analysis)

### Start Backend (HTTP):
```powershell
cd backend
USE_HTTP=true python main.py
# Or:
# python main.py --http
```

### Start Frontend (HTTP):
```powershell
cd frontend
npm run dev:http
```

**Access:**
- Frontend: `http://localhost:3000` ⚠️ Not Secure (for testing)
- Backend: `http://localhost:8000` ⚠️ Not Secure (for testing)

**Use this mode for:**
- Wireshark network analysis
- Testing unencrypted traffic
- Debugging network issues

---

## Common Error: "socket hang up"

This error occurs when protocols don't match:

**Wrong:**
- Frontend: HTTP (`npm run dev:http`)
- Backend: HTTPS (`python main.py` without `USE_HTTP=true`)
- ❌ **Result:** Socket hang up error

**Correct:**
- Frontend: HTTP + Backend: HTTP ✅
- Frontend: HTTPS + Backend: HTTPS ✅

---

## Quick Reference

| Frontend Command | Backend Command | Frontend URL | Backend URL |
|-----------------|----------------|--------------|-------------|
| `npm run dev:https` | `python main.py` | `https://localhost:3000` | `https://localhost:8000` |
| `npm run dev:http` | `USE_HTTP=true python main.py` | `http://localhost:3000` | `http://localhost:8000` |
| `npm run dev` | `python main.py` | `http://localhost:3000` | `https://localhost:8000` ⚠️ Mismatch! |

**Note:** `npm run dev` (without `:https` or `:http`) defaults to HTTP frontend but HTTPS backend - this will cause errors!

---

## Recommended Setup

For secure development, use **Option 1 (Both HTTPS)**:
1. Start backend: `python backend/main.py`
2. Start frontend: `npm run dev:https` (in frontend folder)
3. Visit: `https://localhost:3000`

Both will use the trusted certificate and show as secure! 🔒


