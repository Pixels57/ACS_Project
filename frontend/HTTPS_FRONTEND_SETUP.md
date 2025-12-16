# HTTPS for Frontend

## Setup

The frontend can run on HTTPS when using `npm run dev:https`. The configuration automatically uses the same trusted certificate from the backend.

## Usage

### Run Frontend on HTTP (Default)
```powershell
cd frontend
npm run dev
```
- Frontend: `http://localhost:3000` (shows "Not secure" - normal for HTTP)
- Backend: `https://localhost:8000` (secure)
- API communication: HTTPS via proxy

### Run Frontend on HTTPS
```powershell
cd frontend
npm run dev:https
```
- Frontend: `https://localhost:3000` (secure - uses backend certificate)
- Backend: `https://localhost:8000` (secure)
- API communication: HTTPS via proxy

## Certificate

The frontend automatically uses the same certificate files from the backend:
- `backend/cert.pem`
- `backend/key.pem`

Since you've already trusted this certificate, the frontend will also show as secure when running on HTTPS.

## Browser Access

When running `npm run dev:https`:
1. Visit: `https://localhost:3000`
2. Should show **green lock** (secure connection)
3. No certificate warnings (if certificate is trusted)

## Notes

- The certificate is shared between frontend and backend
- If you trusted the certificate for the backend, it works for the frontend too
- Both use the same `localhost` certificate, so no additional trust needed

---

## Summary

- **404 for favicon.ico:** Normal, harmless, can be ignored
- **"Not secure" on frontend:** Normal for HTTP dev server, API communication is secure
- **Backend HTTPS:** Working correctly with trusted certificate

Everything is working as expected! 🎉

