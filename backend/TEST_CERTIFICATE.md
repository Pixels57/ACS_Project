# Testing the Trusted Certificate

After trusting the certificate, use these methods to verify it's working:

## Method 1: Browser Test (Easiest)

1. **Start the backend server:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Open your browser** and visit:
   ```
   https://localhost:8000
   ```

3. **Expected Result:**
   - ✅ **Secure connection** (green lock icon)
   - ✅ **No certificate warnings**
   - ✅ URL shows "Secure" or padlock icon
   - ✅ Can access the API documentation at `https://localhost:8000/docs`

4. **If you see warnings:**
   - Certificate may not be fully trusted yet
   - Try restarting your browser
   - Check that you imported to "Trusted Root Certification Authorities"

---

## Method 2: Python Test Script

Run the automated test:

```powershell
cd backend
python test_certificate_trust.py
```

**Expected Output:**
- `[OK] Certificate is currently valid`
- `[OK] Common Name is correct (localhost)`
- `[OK] SSL handshake successful!`

---

## Method 3: Command Line (curl)

If you have curl installed:

```powershell
# Should work without -k flag if certificate is trusted
curl https://localhost:8000

# If it fails, try with verbose output:
curl -v https://localhost:8000
```

**Expected:** Connection successful without SSL errors

---

## Method 4: Python Requests Test

Test with Python requests library:

```python
import requests

# Should work if certificate is trusted
try:
    response = requests.get('https://localhost:8000')
    print(f"Success! Status: {response.status_code}")
    print("Certificate is trusted!")
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
    print("Certificate may not be trusted in Python's certificate store")
except requests.exceptions.ConnectionError:
    print("Connection refused - Start the backend server first")
```

**Note:** Python requests may use a different certificate store than the system. If it fails, you can:
- Use `verify='backend/cert.pem'` parameter
- Or install certifi and add the certificate

---

## Method 5: Full Application Test

1. **Start backend:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Start frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Test the application:**
   - Visit `http://localhost:3000`
   - Login and use the application
   - Check browser DevTools → Network tab
   - All requests to `/api/*` should go through HTTPS
   - No certificate warnings in console

---

## Verification Checklist

- [ ] Browser shows secure connection (green lock) at `https://localhost:8000`
- [ ] No certificate warnings in browser
- [ ] Backend starts without SSL errors
- [ ] Frontend can connect to backend via proxy
- [ ] API endpoints respond correctly
- [ ] DevTools shows HTTPS connections

---

## Troubleshooting

### Browser Still Shows Warning

1. **Clear browser cache** and restart
2. **Check certificate store:**
   - Open `certmgr.msc`
   - Verify certificate is in "Trusted Root Certification Authorities"
3. **Try different browser** to isolate the issue

### Python Requests Fails

Python may use a different certificate store. Options:

1. **Use verify parameter:**
   ```python
   requests.get('https://localhost:8000', verify='backend/cert.pem')
   ```

2. **Or trust in Python's store:**
   ```python
   import certifi
   import ssl
   # Add custom CA bundle
   ```

### Connection Refused

- Make sure backend is running: `python backend/main.py`
- Check port 8000 is not in use
- Verify firewall isn't blocking

---

## Success Indicators

✅ **Certificate is working correctly if:**
- Browser shows green lock (secure connection)
- No SSL errors in console
- Backend starts successfully
- Frontend can communicate with backend
- All HTTPS requests succeed


